import time
import math

def get_unique_substrings(binary_str):
    """Get all unique non-empty substrings from the binary string."""
    return {
        binary_str[i:j]
        for i in range(len(binary_str))
        for j in range(i + 1, len(binary_str) + 1)
    }

def is_prime(n):
    """Quickly check if a number is prime."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    for i in range(5, int(math.sqrt(n)) + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True

def find_primes(binary_str, limit):
    """Find prime numbers in binary string substrings."""
    try:
        decimal_value = int(binary_str, 2)
        print(f"Decimal value: {decimal_value}")
    except ValueError:
        print("Invalid binary string.")
        return []

    # Extract and clean substrings
    numbers = {
        int(sub.lstrip('0'), 2)
        for sub in get_unique_substrings(binary_str)
        if sub.strip('0')  # Skip empty or zero-only substrings
    }

    primes = sorted(n for n in numbers if 1 < n < limit and is_prime(n))

    # Show results clearly
    if primes:
        if len(primes) <= 6:
            print(f"Found {len(primes)} prime(s): {', '.join(map(str, primes))}")
        else:
            print(f"Found {len(primes)} prime(s): {', '.join(map(str, primes[:3]))} ... {', '.join(map(str, primes[-3:]))}")
    else:
        print("No primes found.")

    return primes

if __name__ == "__main__":
    # Handle input
    user_input = input("Enter binary string and limit: ").strip()

    if ',' not in user_input:
        print("Please use this format:binary,limit")
        exit()

    binary_str, limit_str = map(str.strip, user_input.split(',', 1))

    if not all(c in '01' for c in binary_str):
        print("Invalid binary string.")
        exit()

    try:
        limit = int(limit_str)
    except ValueError:
        print("Invalid limit.")
        exit()

    # Start timer
    start_time = time.perf_counter()

    # Main logic
    find_primes(binary_str, limit)

    # Display runtime
    print(f"Finished in {time.perf_counter() - start_time:.4f} seconds.")






# case  time
# 1 : 0.0006              0100001101001111,999999
# 2 : 0.0010              01000011010011110100110101010000,999999
# 3 : 0.0006             1111111111111111111111111111111111111111,999999
# 4 : 0.0026             010000110100111101001101010100000011000100111000,999999999
# 5 :  0.0063            01000011010011110100110101010000001100010011100000110001,123456789012
# 6 : 0.2401             0100001101001111010011010101000000110001001110000011000100111001,123456789012345
# 7 : 0.2279            010000110100111101001101010100000011000100111000001100010011100100100001,123456789012345
# 8 : 6.4825            01000011010011110100110101010000001100010011100000110001001110010010000101000001,1234567890123456789
# 9 : 15.6773            0100001101001111010011010101000000110001001110000011000100111001001000010100000101000100,1234567890123456789
# 10 :   19.0934          010000110100111101001101010100000011000100111000001100010011100100100001010000010100010001010011,12345678901234567890
