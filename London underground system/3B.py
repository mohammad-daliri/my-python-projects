"""
Task 3B: Journey Planner Based on Number of Stops

This script covers the two parts of subtask (3b):

1) Empirical performance measurement on artificial unweighted networks:

2) Application with London Underground data:
"""
import sys
import os
import time
import random
import statistics
from typing import List, Tuple, Optional

import matplotlib.pyplot as plt
import pandas as pd

HERE = os.path.dirname(__file__)
CLRS_DIR = os.path.join(HERE, "clrsPython")

if CLRS_DIR not in sys.path:
    sys.path.append(CLRS_DIR)

from adjacency_list_graph import AdjacencyListGraph
from bfs import bfs

# ===========================================================================
# Part 1: Empirical performance measurement on artificial networks (3B)
# ===========================================================================

def build_random_unweighted_graph(
    n: int,
    edge_prob: float = 0.05
) -> AdjacencyListGraph:
    """
    Build a random unweighted, undirected graph with n vertices.
    This graph represents an artificial "tube network" for the fewest-stops
    scaling experiment.
    """
    G = AdjacencyListGraph(n, directed=False)

    # Ensure connectivity via a chain.
    for u in range(n - 1):
        G.insert_edge(u, u + 1)

    # Track the edges to avoid duplicates as (min, max).
    edges = set((min(u, u + 1), max(u, u + 1)) for u in range(n - 1))

    # Add extra random edges.
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < edge_prob:
                e = (u, v)
                if e in edges:
                    continue
                G.insert_edge(u, v)
                edges.add(e)

    return G


def bfs_shortest_path_indices(
    G: AdjacencyListGraph,
    start_idx: int,
    end_idx: int
) -> Tuple[Optional[int], Optional[List[int]]]:
    """
    Run BFS on an unweighted graph G from start_idx and reconstruct the
    path to end_idx.
    """
    dist, pi = bfs(G, start_idx)

    # In the CLRS BFS implementation, unreachable vertices have dist[v] = None.
    if dist[end_idx] is None:
        return None, None

    path: List[int] = []
    v = end_idx
    while v is not None:
        path.insert(0, v)
        v = pi[v]

    # dist[end_idx] is the number of edges on the shortest path (fewest stops).
    return dist[end_idx], path


def average_bfs_time(
    n: int,
    num_pairs: int = 50,
    edge_prob: float = 0.05
) -> float:
    """
    For a random graph with n vertices:

      - Build a random unweighted graph using build_random_unweighted_graph.
      - Returns the average time per BFS-based shortest-path calculation.
    """
    G = build_random_unweighted_graph(n, edge_prob=edge_prob)
    times: List[float] = []

    for _ in range(num_pairs):
        start_idx, end_idx = random.sample(range(n), 2)

        t0 = time.perf_counter()
        stops, path = bfs_shortest_path_indices(G, start_idx, end_idx)
        t1 = time.perf_counter()

        # Ensure a path is found (should always be the case in connected graph).
        if stops is None or path is None:
            continue

        times.append(t1 - t0)

    # In practice times should be non-empty because the graph is connected.
    return statistics.mean(times) if times else 0.0


def run_experiment_3B(
    sizes: Optional[List[int]] = None,
    num_pairs_per_n: int = 50,
    edge_prob: float = 0.05,
    seed: Optional[int] = 123) -> pd.DataFrame:
    """
    Run the scaling experiment on artificial networks.

    For each n in 'sizes' (100, 200, ..., 1000):
      - Build a random graph with n stations.
      - Measure the average time per BFS "fewest stops" calculation.
      - Record (n, average_time_seconds) in a DataFrame.

    Returns:
        A DataFrame with columns ['n', 'average_time_seconds'].
    """
    if sizes is None:
        sizes = list(range(100, 1100, 100))  # 100, 200, ..., 1000

    if seed is not None:
        random.seed(seed)

    records = []

    print("\n=== Task 3B: Empirical BFS scaling on artificial unweighted networks ===")
    print(f"Running BFS experiments for n in {sizes}, "
          f"{num_pairs_per_n} random pairs per n, edge_prob={edge_prob}.")

    for n in sizes:
        avg_time = average_bfs_time(n, num_pairs=num_pairs_per_n, edge_prob=edge_prob)
        print(f"Average BFS time for n={n}: {avg_time:.8f} seconds")

        records.append({"n": n, "average_time_seconds": avg_time})

    df = pd.DataFrame.from_records(records)
    return df


def plot_experiment_3B(df: pd.DataFrame, output_path: Optional[str] = None) -> None:
    """
    Plot average BFS time against network size n for the artificial networks.
    """
    if df.empty:
        print("No data to plot for 3B.")
        return

    plt.figure()
    plt.plot(df["n"], df["average_time_seconds"], marker="o", linestyle="-")
    plt.xlabel("Number of stations (n)")
    plt.ylabel("Average BFS time (seconds)")
    plt.title("Task 3B: Average BFS time vs network size n (artificial networks)")
    plt.tight_layout()

    if output_path is not None:
        plt.savefig(output_path)
        print(f"3B empirical scaling plot saved to {output_path}")
    else:
        plt.show()


# ===========================================================================
# Part 2: Application with London Underground Data (fewest stops)
# ===========================================================================

def load_tube_data() -> pd.DataFrame:

    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "London Underground data.xlsx")
    df = pd.read_excel(file_path)
    return df


def build_tube_graph(df: pd.DataFrame):
    """
    Build an unweightwed undirected graph for the full London Underground
    network.

    Returns:
        - The built AdjacencyListGraph (undirected, unweighted).
        - A dict mapping station name -> station ID.
        - A dict mapping station ID -> station name.
    
    """
    station_to_id: dict[str, int] = {}
    id_to_station: dict[int, str] = {}
    next_id = 0

    # A set is used to avoid duplicate edges.
    edges = set()

    for _, row in df.iterrows():
        # Expected format: [0: line, 1: from, 2: to, 3: time]
        station_a = row.iloc[1]
        station_b = row.iloc[2]
        t = row.iloc[3]

        if pd.isna(station_a) or pd.isna(station_b) or pd.isna(t):
            continue

        station_a = str(station_a).strip()
        station_b = str(station_b).strip()

        # Assign unique IDs to stations.
        if station_a not in station_to_id:
            station_to_id[station_a] = next_id
            id_to_station[next_id] = station_a
            next_id += 1

        if station_b not in station_to_id:
            station_to_id[station_b] = next_id
            id_to_station[next_id] = station_b
            next_id += 1

        id_a = station_to_id[station_a]
        id_b = station_to_id[station_b]

        # Add edge if not a loop.
        if id_a != id_b:
            e = (min(id_a, id_b), max(id_a, id_b))
            edges.add(e)

    n = next_id
    graph = AdjacencyListGraph(n, directed=False)  # Unweighted for BFS

    for id_a, id_b in edges:
        graph.insert_edge(id_a, id_b)

    return graph, station_to_id, id_to_station


def print_real_route(
    graph: AdjacencyListGraph,
    station_to_id: dict,
    id_to_station: dict,
    start_label: str,
    end_label: str
) -> None:
    """
    Print the path with the fewest stops between two real stations
    using BFS on the unweighted graph built from the Excel data.
    """
    # Ensure correct formatting.
    start_label_str = start_label.strip()
    end_label_str = end_label.strip()

    # Validate stations exist.
    if start_label_str not in station_to_id or end_label_str not in station_to_id:
        print(f"One of the stations '{start_label}' or '{end_label}' "
              f"is not in the dataset.")
        return

    start_idx = station_to_id[start_label_str]
    end_idx = station_to_id[end_label_str]

    # Run BFS to find the path with fewest stops.
    stops, path_indices = bfs_shortest_path_indices(graph, start_idx, end_idx)

    if stops is None or path_indices is None:
        print(f"No path found from {start_label} to {end_label}.")
        return

    path_labels = [id_to_station[i] for i in path_indices]

    print(f"Path with fewest stops from {start_label} to {end_label}:")
    print(" -> ".join(path_labels))
    print(f"Total number of stops: {stops}")


def run_london_application() -> None:
    """
    Application with London Underground Data (fewest stops).

    Uses BFS on the full London Underground graph to compute journeys with the
    fewest stops for the two required tests.
    """
    print("\n=== Task 3B: Application with London Underground Data (fewest stops) ===")

    df = load_tube_data()
    graph, station_to_id, id_to_station = build_tube_graph(df)

    test_routes = [
        ("Covent Garden", "Leicester Square"),
        ("Wimbledon", "Stratford"),
    ]

    for start_label, end_label in test_routes:
        print("\n----------------------------------------")
        print_real_route(graph, station_to_id, id_to_station, start_label, end_label)


def main() -> None:
    # Part 1 – Empirical performance measurement on artificial unweighted networks
    SCALING_CSV_PATH = "3B_bfs_scaling_experiments.csv"
    SCALING_PLOT_PATH = "3B_bfs_scaling_times_vs_n.png"

    df_scaling = run_experiment_3B(
        sizes=list(range(100, 1100, 100)),
        num_pairs_per_n=50,
        edge_prob=0.05,
        seed=123,
    )
    df_scaling.to_csv(SCALING_CSV_PATH, index=False)
    print(f"\n3B scaling experiment data saved to {SCALING_CSV_PATH}")

    plot_experiment_3B(df_scaling, output_path=SCALING_PLOT_PATH)

    # Part 2 – Application with London Underground data (fewest stops)
    run_london_application()

if __name__ == "__main__":
    main()
