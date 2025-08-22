import time
def get_substrings(bin_str):
    """Generate all contiguous substrings from a binary string."""
    return {bin_str[i:j] for i in range(len(bin_str)) for j in range(i + 1, len(bin_str) + 1)}

def binary_to_decimal(substrings):
    """Convert binary substrings to decimal values."""
    return {int(sub, 2) for sub in substrings}

def is_prime(num):
    """Check if a number is prime."""
    if num < 2:
        return False
    if num == 2:
        return True  # 2 is the only even prime
    if num % 2 == 0:
        return False
    for i in range(3, int(num**0.5) + 1, 2):  # Check odd numbers only
        if num % i == 0:
            return False
    return True

def find_primes(dec_numbers, limit):
    """Filter and return unique primes below a given limit."""
    return sorted(num for num in dec_numbers if num < limit and is_prime(num))

def find_hidden_primes(bin_str, limit):
    """Identify prime numbers concealed in binary substrings."""
    print(f"Decimal value is: {int(bin_str, 2)}")

    substrings = get_substrings(bin_str)
    dec_numbers = binary_to_decimal(substrings)
    primes = find_primes(dec_numbers, limit)

    if primes:
        if len(primes) < 6:
            print(f"{len(primes)}: {', '.join(map(str, primes))}")
        else:
            print(f"{len(primes)}: {', '.join(map(str, primes[:3]))}, ..., {', '.join(map(str, primes[-3:]))}")
    else:
        print("No primes found.")
    
    return primes

def main():
    """Main execution block for processing user input."""
    input_data = input("Enter a binary number and limit: ").strip()

    if ',' not in input_data:
        print("Invalid input format.")
        return

    bin_str, limit_str = map(str.strip, input_data.split(',', 1))

    if not set(bin_str).issubset({'0', '1'}):
        print("Invalid binary number.")
        return

    try:
        limit = int(limit_str)
    except ValueError:
        print("Invalid limit. Please enter a valid integer.")
        return


     
# Start timing
    start_time = time.perf_counter()

    # Execute the main logic
    find_hidden_primes(bin_str, limit)

    # End timing
    end_time = time.perf_counter()

    # Calculate and print runtime
    runtime = end_time - start_time
    print(f"Runtime: {runtime:.6f} seconds")

if __name__ == "__main__":
    main()





# case  time
# 1 : 0.000703
# 2 : 0.000875
# 3 : 0.000439
# 4 : 0.002276
# 5 : 0.006531
# 6 : 0.278702
# 7 : 0.291054
# 8 : 7.836554
# 9 : 22.065264
# 10 : 26.203811 