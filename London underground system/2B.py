# Performance analysis of Dijkstra's algorithm on synthetic graphs
# Measures average execution time across varying network sizes

import sys
import os
import time
import random
import math
import matplotlib.pyplot as plt

# Configure module paths
base_path = os.path.dirname(__file__)
sys.path.extend([
    os.path.join(base_path, 'clrsPython', 'Chapter 22'),
    os.path.join(base_path, 'clrsPython', 'Chapter 6'),
    os.path.join(base_path, 'clrsPython', 'Utility functions'),
    os.path.join(base_path, 'clrsPython', 'Chapter 10')
])

from dijkstra import dijkstra
from adjacency_list_graph import AdjacencyListGraph


def create_sparse_graph(num_nodes, rng_seed=7):
    """Generate a sparse connected graph using dictionary representation.
    
    Returns adjacency dictionary mapping nodes to their neighbors with edge weights.
    """
    rng = random.Random(rng_seed)
    adjacency_dict = {i: {} for i in range(num_nodes)}
    
    # Ensure connectivity by creating a spanning tree
    for i in range(1, num_nodes):
        parent = rng.randint(0, i - 1)
        weight = rng.randint(1, 20)
        adjacency_dict[parent][i] = weight
        adjacency_dict[i][parent] = weight
    
    # Add additional random edges to maintain sparsity
    edge_count = num_nodes // 2
    for _ in range(edge_count):
        u = rng.randint(0, num_nodes - 1)
        v = rng.randint(0, num_nodes - 1)
        if u != v and v not in adjacency_dict[u]:
            weight = rng.randint(1, 20)
            adjacency_dict[u][v] = weight
            adjacency_dict[v][u] = weight
    
    return adjacency_dict


def convert_dict_to_graph(adj_dict):
    """Transform adjacency dictionary into AdjacencyListGraph format.
    
    Returns tuple: (graph object, node_index_mapping)
    """
    num_vertices = len(adj_dict)
    graph = AdjacencyListGraph(num_vertices, directed=False, weighted=True)
    index_map = {node: idx for idx, node in enumerate(sorted(adj_dict.keys()))}
    
    # Track inserted edges to avoid duplicates in undirected graph
    inserted_edges = set()
    
    for source_node, neighbors in adj_dict.items():
        source_idx = index_map[source_node]
        for target_node, edge_weight in neighbors.items():
            target_idx = index_map[target_node]
            # For undirected graphs, only insert edge once (smaller index first)
            edge_key = (min(source_idx, target_idx), max(source_idx, target_idx))
            if edge_key not in inserted_edges:
                graph.insert_edge(source_idx, target_idx, edge_weight)
                inserted_edges.add(edge_key)
    
    return graph, index_map


class PerformanceAnalyzer:
    """Encapsulates performance measurement for shortest path algorithms."""
    
    def __init__(self, graph_builder=None, random_seed=7):
        self.graph_builder = graph_builder or create_sparse_graph
        self.rng = random.Random(random_seed)
        self.random_seed = random_seed
    
    def measure_single_run(self, graph_obj, index_mapping, start_node, target_node):
        """Execute Dijkstra's algorithm once and return execution duration."""
        start_idx = index_mapping[start_node]
        target_idx = index_mapping[target_node]
        
        begin_time = time.perf_counter()
        distances, predecessors = dijkstra(graph_obj, start_idx)
        elapsed = time.perf_counter() - begin_time
        
        # Access result to ensure computation completes
        _ = distances[target_idx]
        
        return elapsed
    
    def compute_average_runtime(self, network_size, num_iterations=100):
        """Calculate mean execution time and standard deviation for given graph size over multiple trials.
        
        Returns tuple: (mean_time, std_dev)
        """
        graph_dict = self.graph_builder(network_size, self.random_seed)
        graph_obj, node_map = convert_dict_to_graph(graph_dict)
        
        vertex_list = list(graph_dict.keys())
        execution_times = []
        
        for iteration in range(num_iterations):
            # Select distinct source and destination vertices
            source = self.rng.choice(vertex_list)
            destination = self.rng.choice(vertex_list)
            while destination == source:
                destination = self.rng.choice(vertex_list)
            
            runtime = self.measure_single_run(graph_obj, node_map, source, destination)
            execution_times.append(runtime)
        
        # Calculate mean
        mean_time = sum(execution_times) / len(execution_times)
        
        # Calculate standard deviation
        variance = sum((t - mean_time) ** 2 for t in execution_times) / len(execution_times)
        std_dev = math.sqrt(variance)
        
        return mean_time, std_dev
    
    def compute_statistics(self, execution_times):
        """Calculate mean, standard deviation, and 95% confidence interval."""
        n = len(execution_times)
        mean_time = sum(execution_times) / n
        
        # Standard deviation
        variance = sum((t - mean_time) ** 2 for t in execution_times) / n
        std_dev = math.sqrt(variance)
        
        # 95% CI using standard error (approximate with normal distribution for large n)
        # For n >= 30, t-distribution approximates normal
        std_error = std_dev / math.sqrt(n)
        # Z-score for 95% CI is approximately 1.96
        z_95 = 1.96
        ci_margin = z_95 * std_error
        
        return mean_time, std_dev, ci_margin


def visualize_results(graph_sizes, timing_results, error_bars=None, num_trials=100):
    """Generate visualization of performance measurements with error bars.
    
    Args:
        graph_sizes: List of graph sizes tested
        timing_results: List of mean execution times
        error_bars: List of standard deviations or CI margins (optional)
        num_trials: Number of trials per graph size (for title)
    """
    fig = plt.figure(figsize=(10, 6))
    
    if error_bars:
        plt.errorbar(graph_sizes, timing_results, yerr=error_bars, 
                    marker='o', linestyle='-', linewidth=2, 
                    capsize=5, capthick=2, elinewidth=1.5,
                    label='Mean ± 1 Std Dev')
    else:
        plt.plot(graph_sizes, timing_results, marker='o', linestyle='-', linewidth=2)
    
    plt.xlabel("Network size n (stations)", fontsize=12)
    plt.ylabel("Avg time per shortest-path (s)", fontsize=12)
    plt.title(f"Dijkstra runtime vs n (synthetic networks, K={num_trials} trials)", fontsize=14)
    plt.grid(True, alpha=0.3)
    if error_bars:
        plt.legend(fontsize=10)
    plt.tight_layout()
    plt.show()


def main():
    """Main execution routine."""
    analyzer = PerformanceAnalyzer(random_seed=7)
    test_sizes = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    num_trials = 100
    
    print("Running performance analysis...")
    performance_data = []
    error_data = []
    for size in test_sizes:
        avg_time, std_dev = analyzer.compute_average_runtime(size, num_iterations=num_trials)
        performance_data.append(avg_time)
        error_data.append(std_dev)
        print(f"Size {size}: {avg_time:.6f}s average (±{std_dev:.6f}s std dev)")
    
    visualize_results(test_sizes, performance_data, error_bars=error_data, num_trials=num_trials)


if __name__ == "__main__":
    main()

