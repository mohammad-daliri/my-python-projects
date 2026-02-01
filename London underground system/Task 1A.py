"""
Task 1a: Operational Station Status System - Code Implementation
Using CLRS Python Library ChainedHashTable

This code implements the same data structure and operations that were
traced manually, for verification purposes.
"""

# Import the CLRS library hash table implementation
from chained_hashtable import ChainedHashTable


def simple_string_hash(s):
    """
    Simple hash function for demonstration.
    For a string, sum ASCII values of all characters.
    """
    if isinstance(s, str):
        return sum(ord(c) for c in s)
    return s


def display_hash_table_state(ht):
    """Display the current state of the hash table."""
    print("\nHash Table State:")
    for i in range(ht.m):
        # Get the linked list at this slot
        linked_list = ht.table[i]
        # Display the contents of this slot
        items = []
        current = linked_list.sentinel.next
        while current != linked_list.sentinel:
            items.append(str(current.data))
            current = current.next
        print(f"  Slot [{i}]: {items if items else '[]'}")


def main():
    """
    Build hash table with 5 stations and perform a status check.
    This implements the same operations that were traced manually.
    """

    print("="*60)
    print("TASK 1a: Code Implementation")
    print("="*60)

    # Create hash table with m=7 slots (same as manual trace)
    print("\nCreating ChainedHashTable with m=7 slots")
    print("Using hash function: h(key) = sum(ASCII values) mod 7")

    ht = ChainedHashTable(m=7, hash_func=simple_string_hash)

    # Dataset: 5 stations (same as manual trace)
    stations = ["A", "B", "C", "D", "E"]

    print(f"\nDataset: {stations}")

    # Insert each station
    print("\n--- Inserting Stations ---")
    for station in stations:
        hash_value = simple_string_hash(station) % ht.m
        print(f"Inserting '{station}' at slot {hash_value}")
        ht.insert(station)

    # Display final state
    print("\n--- Final Hash Table State ---")
    display_hash_table_state(ht)

    # Status check for station "C" (same as manual trace)
    print("\n" + "="*60)
    print("STATUS CHECK: Searching for Station 'C'")
    print("="*60)

    test_station = "C"
    print(f"\nSearching for: '{test_station}'")

    # Perform search using CLRS library
    result = ht.search(test_station)

    if result is not None:
        print(f"\n  FOUND: Station '{test_station}' is OPERATIONAL")
        print(f"  Located at: {result}")
    else:
        print(f"\n  NOT FOUND: Station '{test_station}' is NOT OPERATIONAL")

    # Additional test: search for non-existent station
    print("\n" + "="*60)
    print("ADDITIONAL TEST: Searching for Station 'Z'")
    print("="*60)

    test_station2 = "Z"
    print(f"\nSearching for: '{test_station2}'")

    result2 = ht.search(test_station2)

    if result2 is not None:
        print(f"\n  FOUND: Station '{test_station2}' is OPERATIONAL")
    else:
        print(f"\n  NOT FOUND: Station '{test_station2}' is NOT OPERATIONAL")

    print("\n" + "="*60)
    print("Code execution complete")
    print("="*60)


if __name__ == "__main__":
    main()


"""
USAGE INSTRUCTIONS:

1. Ensure you have the CLRS library installed:
   - Download from: https://mitp-content-server.mit.edu/books/content/sectbyfn/books_pres_0/11599/clrsPython.zip
   - Extract and place Chapter11 folder in the same directory

2. Run this script:
   python task1a_code.py

3. Capture screenshot of the output showing:
   - The final hash table state
   - The search result for station 'C'

4. Compare this output with your manual trace to verify:
   - All stations are in the correct slots
   - The search operation finds station 'C'
   - The internal structure matches what you traced by hand
"""