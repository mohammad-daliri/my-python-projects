import random
import time
import matplotlib.pyplot as plt
from clrsPython import AdjacencyListGraph, kruskal


def generate_random_weighted_graph(n, edge_factor=3, max_weight=20):
   
    graph = AdjacencyListGraph(n, directed=False, weighted=True)

    # 1) Build a random spanning tree so the graph is connected
    for v in range(1, n):
        u = random.randrange(0, v)
        w = random.randint(1, max_weight)
        graph.insert_edge(u, v, w)

    # Record existing edges from the spanning tree
    existing = set()
    for u in range(n):
        for edge in graph.get_adj_list(u):
            v = edge.get_v()
            if u < v:
                existing.add((u, v))

    # 2) Add extra random edges
    target_edges = edge_factor * n
    extra_edges = max(0, target_edges - (n - 1))

    while extra_edges > 0:
        u = random.randrange(0, n)
        v = random.randrange(0, n)
        if u == v:
            continue
        a, b = sorted((u, v))
        if (a, b) in existing:
            continue
        w = random.randint(1, max_weight)
        graph.insert_edge(a, b, w)
        existing.add((a, b))
        extra_edges -= 1

    return graph


def measure_mst_time(n, trials=5):
    
    total_time = 0.0
    for _ in range(trials):
        g = generate_random_weighted_graph(n)
        start = time.perf_counter()
        _ = kruskal(g)
        end = time.perf_counter()
        total_time += (end - start)
    return total_time / trials


def main():
    random.seed(42)

    sizes = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000,
         1200, 1400, 1600, 1800, 2000]
    avg_times = []

    for n in sizes:
        avg_t = measure_mst_time(n, trials=5)
        avg_times.append(avg_t)
        print(f"n = {n}, average MST time = {avg_t:.6f} seconds")

    plt.figure()
    plt.plot(sizes, avg_times, marker="o")
    plt.xlabel("Number of stations (n)")
    plt.ylabel("Average time to compute core backbone (seconds)")
    plt.title("Empirical runtime of Kruskal's algorithm")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
