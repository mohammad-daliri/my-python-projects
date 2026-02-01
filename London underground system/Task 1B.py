"""
Task 1b: Empirical Performance Measurement and London Underground Application
Using CLRS ChainedHashTable
"""

import time
import random
import matplotlib.pyplot as plt
from chained_hashtable import ChainedHashTable


# Part 1: Empirical Performance Measurement

def generate_dataset(n):
    """Generate n unique station IDs as integers from 0 to n-1"""
    return list(range(n))


def measure_average_search_time(dataset_size, num_queries=10000):
    """Measure average time per search in microseconds"""

    # Generate dataset
    dataset = generate_dataset(dataset_size)

    # Build hash table
    ht = ChainedHashTable(m=dataset_size)
    for station in dataset:
        ht.insert(station)

    # Prepare queries (50% hits, 50% misses)
    queries = []
    for _ in range(num_queries):
        if random.random() < 0.5:
            queries.append(random.choice(dataset))
        else:
            queries.append(dataset_size + random.randint(1, dataset_size))

    # Measure time
    start_time = time.perf_counter()
    for query in queries:
        result = ht.search(query)
    end_time = time.perf_counter()

    # Calculate average in microseconds
    total_time_us = (end_time - start_time) * 1_000_000
    avg_time_us = total_time_us / num_queries

    return avg_time_us


def run_empirical_analysis():
    """Run performance measurement and generate graph"""

    print("=" * 70)
    print("TASK 1b - EMPIRICAL PERFORMANCE MEASUREMENT")
    print("=" * 70)

    sizes = [1000, 5000, 10000, 25000, 50000]
    avg_times = []

    print("\nMeasuring average search time...")
    print("\n{:<15} {:<20}".format("Dataset Size", "Avg Time (us)"))
    print("-" * 40)

    for n in sizes:
        print("Testing n = {:>6}...".format(n), end=" ", flush=True)
        avg_time = measure_average_search_time(n, num_queries=10000)
        avg_times.append(avg_time)
        print("{:>8.6f} us".format(avg_time))

    print("-" * 40)

    # Calculate statistics
    mean_time = sum(avg_times) / len(avg_times)
    variance = sum((x - mean_time) ** 2 for x in avg_times) / len(avg_times)
    std_dev = variance ** 0.5

    print("\nStatistical Summary:")
    print("  Mean:               {:.6f} us".format(mean_time))
    print("  Standard Deviation: {:.6f} us".format(std_dev))
    print("  Min:                {:.6f} us".format(min(avg_times)))
    print("  Max:                {:.6f} us".format(max(avg_times)))
    print("  Range:              {:.6f} us".format(max(avg_times) - min(avg_times)))
    print("  Coefficient of Var: {:.2f}%".format((std_dev / mean_time) * 100))

    # Generate graph
    print("\nGenerating performance graph...")

    plt.figure(figsize=(12, 7))
    plt.plot(sizes, avg_times, 'bo-', linewidth=2, markersize=10,
             label='Empirical Search Time', markerfacecolor='lightblue')
    plt.axhline(y=mean_time, color='r', linestyle='--', linewidth=2,
                label='Average ({:.4f} us) - O(1) Expected'.format(mean_time))
    plt.fill_between(sizes,
                     [mean_time - std_dev] * len(sizes),
                     [mean_time + std_dev] * len(sizes),
                     alpha=0.2, color='red',
                     label='± 1 Standard Deviation')
    plt.xlabel('Dataset Size (n)', fontsize=13, fontweight='bold')
    plt.ylabel('Average Time per Search (us)', fontsize=13, fontweight='bold')
    plt.title('Hash Table Search Performance: Empirical O(1) Verification',
              fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, linestyle=':', linewidth=1)
    plt.legend(fontsize=11, loc='best')
    plt.tight_layout()

    filename = 'task1b_performance_graph.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print("Performance graph saved as '{}'".format(filename))

    print("\n" + "=" * 70)
    print("ANALYSIS")
    print("=" * 70)
    print("\nDataset size increased by {}x ({:,} to {:,})".format(
        int(sizes[-1] / sizes[0]), sizes[0], sizes[-1]))
    print("Search time variation: ±{:.2f}%".format(
        ((max(avg_times) - min(avg_times)) / mean_time) * 100))
    print("Coefficient of variation: {:.2f}%".format((std_dev / mean_time) * 100))
    print("=" * 70)

    return sizes, avg_times


# Part 2: London Underground Application

def load_stations():
    """Manually entered list of London Underground stations from Excel file"""
    stations = [
        'Acton Town', 'Aldgate', 'Aldgate East', 'Alperton', 'Angel',
        'Archway', 'Arnos Grove', 'Arsenal', 'Baker Street', 'Balham',
        'Bank', 'Barbican', 'Barking', 'Barkingside', 'Barons Court',
        'Bayswater', 'Becontree', 'Belsize Park', 'Bermondsey', 'Bethnal Green',
        'Blackfriars', 'Blackhorse Road', 'Bond Street', 'Borough', 'Boston Manor',
        'Bounds Green', 'Bow Road', 'Brent Cross', 'Brixton', 'Bromley-by-Bow',
        'Buckhurst Hill', 'Burnt Oak', 'Caledonian Road', 'Camden Town', 'Canada Water',
        'Canary Wharf', 'Canning Town', 'Cannon Street', 'Canons Park', 'Chalfont & Latimer',
        'Chalk Farm', 'Chancery Lane', 'Charing Cross', 'Chesham', 'Chigwell',
        'Chiswick Park', 'Chorleywood', 'Clapham Common', 'Clapham North', 'Clapham South',
        'Cockfosters', 'Colindale', 'Colliers Wood', 'Covent Garden', 'Croxley',
        'Dagenham East', 'Dagenham Heathway', 'Debden', 'Dollis Hill', 'Ealing Broadway',
        'Ealing Common', 'Earl\'s Court', 'East Acton', 'East Finchley', 'East Ham',
        'East Putney', 'Eastcote', 'Edgware', 'Edgware Road', 'Edgware Road (Circle Line)',
        'Elephant & Castle', 'Elm Park', 'Embankment', 'Epping', 'Euston',
        'Euston Square', 'Fairlop', 'Farringdon', 'Finchley Central', 'Finchley Road',
        'Finsbury Park', 'Fulham Broadway', 'Gants Hill', 'Gloucester Road', 'Golders Green',
        'Goldhawk Road', 'Goodge Street', 'Grange Hill', 'Great Portland Street', 'Green Park',
        'Greenford', 'Gunnersbury', 'Hainault', 'Hammersmith', 'Hammersmith (District Line)',
        'Hampstead', 'Hanger Lane', 'Harlesden', 'Harrow & Wealdstone', 'Harrow-on-the-Hill',
        'Hatton Cross', 'Heathrow Terminals 1, 2, 3', 'Heathrow Terminal 4', 'Heathrow Terminal 5',
        'Hendon Central', 'High Barnet', 'High Street Kensington', 'Highbury & Islington', 'Highgate',
        'Hillingdon', 'Holborn', 'Holland Park', 'Holloway Road', 'Hornchurch',
        'Hounslow Central', 'Hounslow East', 'Hounslow West', 'Hyde Park Corner', 'Ickenham',
        'Kennington', 'Kensal Green', 'Kensington (Olympia)', 'Kentish Town', 'Kenton',
        'Kew Gardens', 'Kilburn', 'Kilburn Park', 'King\'s Cross St. Pancras', 'Kingsbury',
        'Knightsbridge', 'Ladbroke Grove', 'Lambeth North', 'Lancaster Gate', 'Latimer Road',
        'Leicester Square', 'Leyton', 'Leytonstone', 'Liverpool Street', 'London Bridge',
        'Loughton', 'Maida Vale', 'Manor House', 'Mansion House', 'Marble Arch',
        'Marylebone', 'Mile End', 'Mill Hill East', 'Monument', 'Moor Park',
        'Moorgate', 'Morden', 'Mornington Crescent', 'Neasden', 'Newbury Park',
        'North Acton', 'North Ealing', 'North Greenwich', 'North Harrow', 'North Wembley',
        'Northfields', 'Northolt', 'Northwick Park', 'Northwood', 'Northwood Hills',
        'Notting Hill Gate', 'Oakwood', 'Old Street', 'Osterley', 'Oval',
        'Oxford Circus', 'Paddington', 'Park Royal', 'Parsons Green', 'Perivale',
        'Piccadilly Circus', 'Pimlico', 'Pinner', 'Plaistow', 'Preston Road',
        'Putney Bridge', 'Queen\'s Park', 'Queensbury', 'Queensway', 'Ravenscourt Park',
        'Rayners Lane', 'Redbridge', 'Regent\'s Park', 'Richmond', 'Rickmansworth',
        'Roding Valley', 'Royal Oak', 'Ruislip', 'Ruislip Gardens', 'Ruislip Manor',
        'Russell Square', 'Seven Sisters', 'Shepherd\'s Bush', 'Shepherd\'s Bush Market', 'Sloane Square',
        'Snaresbrook', 'South Ealing', 'South Harrow', 'South Kensington', 'South Kenton',
        'South Ruislip', 'South Wimbledon', 'South Woodford', 'Southfields', 'Southgate',
        'Southwark', 'St. James\'s Park', 'St. John\'s Wood', 'St. Paul\'s', 'Stamford Brook',
        'Stanmore', 'Stepney Green', 'Stockwell', 'Stonebridge Park', 'Stratford',
        'Sudbury Hill', 'Sudbury Town', 'Swiss Cottage', 'Temple', 'Theydon Bois',
        'Tooting Bec', 'Tooting Broadway', 'Tottenham Court Road', 'Tottenham Hale', 'Totteridge & Whetstone',
        'Tower Hill', 'Tufnell Park', 'Turnham Green', 'Turnpike Lane', 'Upminster',
        'Upminster Bridge', 'Upney', 'Upton Park', 'Uxbridge', 'Vauxhall',
        'Victoria', 'Walthamstow Central', 'Wanstead', 'Warren Street', 'Warwick Avenue',
        'Waterloo', 'Watford', 'Wembley Central', 'Wembley Park', 'West Acton',
        'West Brompton', 'West Finchley', 'West Ham', 'West Hampstead', 'West Harrow',
        'West Kensington', 'West Ruislip', 'Westbourne Park', 'Westminster', 'White City',
        'Whitechapel', 'Willesden Green', 'Willesden Junction', 'Wimbledon', 'Wimbledon Park',
        'Wood Green', 'Wood Lane', 'Woodford', 'Woodside Park'
    ]
    return sorted(stations)


def run_london_underground_application():
    """Apply the system to London Underground data"""

    print("\n" + "=" * 70)
    print("TASK 1b - LONDON UNDERGROUND APPLICATION")
    print("=" * 70)


    # Load stations
    stations = load_stations()

    print("Successfully loaded {} unique station names".format(len(stations)))

    # Show sample
    print("\nSample stations (first 10):")
    for station in stations[:10]:
        print("  - {}".format(station))
    if len(stations) > 10:
        print("  ... and {} more".format(len(stations) - 10))

    # Build hash table
    print("\nBuilding ChainedHashTable with {} stations...".format(len(stations)))
    print("Table size (m): {}".format(len(stations)))

    operational_stations = ChainedHashTable(m=len(stations))

    start_time = time.time()
    for station in stations:
        operational_stations.insert(station)
    build_time = time.time() - start_time

    print("Hash table built in {:.4f} seconds".format(build_time))

    # Testing
    print("\n" + "=" * 70)
    print("TESTING: Station Status Checks")
    print("=" * 70)

    test_cases = [
        ('Victoria', 'Valid major station'),
        ('Paddington', 'Valid station'),
        ('King\'s Cross St. Pancras', 'Valid station with special chars'),
        ('Paddinton', 'Misspelled (missing g)'),
        ('Hogwarts', 'Non-existent/Fictional station')
    ]

    print("\n")

    for i, (station_name, description) in enumerate(test_cases, 1):
        print("TEST {}: {}".format(i, description))
        print("-" * 70)
        print("  Input: {}".format(station_name))

        start_search = time.perf_counter()
        result = operational_stations.search(station_name)
        search_time = (time.perf_counter() - start_search) * 1_000_000

        if result is not None:
            print("  Output: OPERATIONAL")
            print("  Status: Station '{}' is in the network".format(station_name))
        else:
            print("  Output: NOT FOUND")
            print("  Status: Station '{}' is not in the network".format(station_name))

        print("  Search time: {:.3f} us".format(search_time))
        print()

# Main execution

def main():
    """Run all Task 1b components"""

    print("\n" + "=" * 70)
    print("COMP1828 - Task 1b")
    print("Empirical Analysis & London Underground Application")
    print("=" * 70 + "\n")

    # Part 1: Empirical Performance Measurement
    sizes, times = run_empirical_analysis()

    # Part 2: London Underground Application
    run_london_underground_application()

    # Summary
    print("\n" + "=" * 70)
    print("TASK 1B COMPLETE")
    print("=" * 70)
    print("\nDeliverables generated:")
    print("  - Performance graph: task1b_performance_graph.png")
    print("  - Empirical timing data")
    print("  - London Underground system with {} stations".format(len(load_stations())))
    print("  - Test case demonstrations")
    print("\nFor your report:")
    print("  1. Insert the generated graph image")
    print("  2. Take screenshots of test outputs")
    print("  3. Update timing numbers in report")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()