import time

# Generates all unique substrings of the input string
def get_subs(s):
    subs = []
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            sub = s[i:j]
            if sub not in subs:
                subs.append(sub)
    return subs

# Checks if a number is prime
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Finds prime numbers from binary substrings up to the limit
def find_primes(binary, limit):
    subs = get_subs(binary)  # Get all unique substrings
    # Convert substrings to decimal and use a set for uniqueness
    decimal_values = set(int(sub, 2) for sub in subs)
    # Filter for primes less than or equal to the limit
    primes = [n for n in decimal_values if n <= limit and is_prime(n)]
    primes.sort()  # Sort the primes
    count = len(primes)
    if count == 0:
        print("0: ")
    elif count < 6:
        print(f"{count}: {', '.join(map(str, primes))}")
    else:
        print(f"{count}: {', '.join(map(str, primes[:3]))}, ..., {', '.join(map(str, primes[-3:]))}")

# Main program
input_str = input("Enter your binary number and limit: ").strip()
parts = input_str.split(',')
if len(parts) != 2:
    print("Invalid input format. Please use 'binary,integer' (e.g., 101011,99).")
else:
    binary = parts[0].strip()
    limit_str = parts[1].strip()
    if not all(x in '01' for x in binary):
        print("First part must be a binary number.")
    else:
        try:
            limit = int(limit_str)
            start_time = time.perf_counter()
            
            find_primes(binary, limit)
            
            # End timing
            end_time = time.perf_counter()
            
            # Calculate and print the runtime
            runtime = end_time - start_time
            print(f"Runtime: {runtime:.6f} seconds")
        except ValueError:
            print("Second part must be an integer.")



# case  time
# 1 :  0.000405
# 2 : 0.001596
# 3 : 0.000693
# 4 :  0.006709 
# 5 : 0.021200
# 6 : 0.548526 
# 7 :  0.709549
# 8 :  15.886340 
# 9 : 40.844932 
# 10 : 55.698007