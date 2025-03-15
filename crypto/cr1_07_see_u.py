#!/usr/bin/python3

import string
import base64
import time
import multiprocessing
from itertools import product
import os
from tqdm import tqdm

def encrypt(clear, key):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 128)
        enc.append(enc_c)
    return str(base64.urlsafe_b64encode("".join(enc).encode('ascii')), 'ascii')

def decrypt(enc, key):
    dec = []
    enc = str(base64.urlsafe_b64decode(enc.encode('ascii')), 'ascii')
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((128 + ord(enc[i]) - ord(key_c)) % 128)
        dec.append(dec_c)
    return "".join(dec)

# Known values
m = "See you later in the city center"
c = "QSldSTQ7HkpIJj9cQBY3VUhbQ01HXD9VRBVYSkE6UWRQS0NHRVE3VUQrTDE="

# Generate all possible 4-letter lowercase keys
all_possible_keys = ["".join(p) for p in product(string.ascii_lowercase, repeat=4)]
total_combos = len(all_possible_keys)**2  # Total number of key combinations to check

# For progress tracking across processes
counter = multiprocessing.Value('i', 0)
found = multiprocessing.Value('i', 0)

def check_key_batch(k1_batch):
    """Process a batch of k1 keys with progress tracking"""
    local_counter = 0
    batch_size = len(k1_batch) * len(all_possible_keys)
    pbar = tqdm(total=batch_size, position=0, leave=True, 
                desc=f"Process {multiprocessing.current_process().name}", 
                disable=None)
    
    for k1 in k1_batch:
        # If k1 is correct, encrypting m with k1 should give us d
        try:
            d = encrypt(m, k1)
            # Now try all possible k2 values
            for k2 in all_possible_keys:
                try:
                    if encrypt(d, k2) == c:
                        with found.get_lock():
                            found.value = 1
                        return k1, k2, k1 + k2
                except:
                    pass
                finally:
                    local_counter += 1
                    if local_counter % 100 == 0:  # Update progress every 100 combinations
                        pbar.update(100)
                        with counter.get_lock():
                            counter.value += 100
        except:
            # Account for encrypt failures
            local_counter += len(all_possible_keys)
            pbar.update(len(all_possible_keys))
            with counter.get_lock():
                counter.value += len(all_possible_keys)
            continue
    
    # Update any remaining combinations
    remaining = batch_size - local_counter
    if remaining > 0:
        with counter.get_lock():
            counter.value += remaining
        pbar.update(remaining)
    
    pbar.close()
    return None, None, None

def chunk_list(lst, num_chunks):
    """Split a list into approximately equal chunks"""
    avg = len(lst) // num_chunks
    remainder = len(lst) % num_chunks
    result = []
    i = 0
    for j in range(num_chunks):
        chunk_size = avg + 1 if j < remainder else avg
        result.append(lst[i:i+chunk_size])
        i += chunk_size
    return result

def display_overall_progress(total, counter, found, start_time):
    """Display overall progress in a separate process"""
    pbar = tqdm(total=total, position=1, desc="Overall progress", leave=True)
    last_count = 0
    
    while found.value == 0 and counter.value < total:
        current = counter.value
        pbar.update(current - last_count)
        last_count = current
        
        # Calculate and display stats
        elapsed = time.time() - start_time
        if elapsed > 0 and current > 0:
            combos_per_sec = current / elapsed
            remaining = (total - current) / combos_per_sec if combos_per_sec > 0 else 0
            pbar.set_postfix({
                'tested': f"{current:,}/{total:,}",
                'speed': f"{combos_per_sec:.1f} keys/s",
                'remaining': f"{remaining/60:.1f} mins"
            })
            
        time.sleep(0.5)
    
    # Final update
    pbar.update(total - last_count)
    pbar.close()

if __name__ == "__main__":
    print(f"[2025-03-15 14:42:22] Starting parallel key search...")
    print(f"User: Diebbo")
    start_time = time.time()
    
    # Determine number of processes (use CPU count)
    num_processes = multiprocessing.cpu_count()
    print(f"Using {num_processes} processes to test {total_combos:,} possible key combinations")
    
    # Split k1 search space into chunks for each process
    k1_chunks = chunk_list(all_possible_keys, num_processes)
    
    # Start progress monitor in separate process
    progress_process = multiprocessing.Process(
        target=display_overall_progress,
        args=(total_combos, counter, found, start_time)
    )
    progress_process.start()
    
    # Create a process pool and run the search
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = []
        # Use imap_unordered for better performance and to get results as they complete
        for result in pool.imap_unordered(check_key_batch, k1_chunks):
            k1, k2, full_key = result
            if full_key is not None:
                # Found a match, add to results and terminate early
                results.append((k1, k2, full_key))
                pool.terminate()
                with found.get_lock():
                    found.value = 1
                break
    
    # Wait for progress monitor to finish
    progress_process.join()
    
    elapsed = time.time() - start_time
    
    # Process results
    if results:
        k1, k2, full_key = results[0]
        print(f"\nFound keys in {elapsed:.2f} seconds:")
        print(f"k1: {k1}")
        print(f"k2: {k2}")
        print(f"FLAG: CCIT{{{full_key}}}")
        
        # Verify solution
        d = encrypt(m, k1)
        c_check = encrypt(d, k2)
        print(f"Verification: {'Success!' if c_check == c else 'Failed!'}")
    else:
        print(f"\nNo solution found after {elapsed:.2f} seconds. Check your inputs.")
