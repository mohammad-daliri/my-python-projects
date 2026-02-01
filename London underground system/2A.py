from clrsPython import AdjacencyListGraph, dijkstra


STATIONS = ["A", "B", "C", "D", "E"]

#edge list for an undirected weighted graph
#each tuple represents ("station 1", "station 2", travel time )
EDGE_LIST = [
    ("A", "B", 4),
    ("A", "C", 2),
    ("B", "C", 1),
    ("B", "D", 5),
    ("C", "D", 8),
    ("C", "E", 10),
    ("D", "E", 2),
]


def build_undirected_graph(stations, edges):
    """
    Build an undirected, weighted graph using AdjacencyListGraph
    - stations: a list of stations names (A, B, ...)
    - edges: list of (u, v, w)
    """
    station_to_id = {name: i for i, name in enumerate(stations)}     #maps station's label to an index
    id_to_station = {i: name for name, i in station_to_id.items()}   #converts numbers back to letters


    graph = AdjacencyListGraph(len(stations), directed=False, weighted=True)


    for u_name, v_name, w in edges:    #adds each edge to the graph
        u = station_to_id[u_name]
        v = station_to_id[v_name]
        graph.insert_edge(u, v, w)

    return graph, station_to_id, id_to_station


def reconstruct_path(predecessors, start_idx, end_idx):
    """
    It builds the shortest path using the predecessors' list from Dijkstra
    We start in the last station and follow predecessors backward until we reach the first.
    Predecessors help us find the node that comes before chosen station in the shortest path.
    we reverse the order to get the shortest path from start to end
    """
    path_indices = []
    current = end_idx #starting with last station

    while current is not None:
        path_indices.insert(0, current)
        if current == start_idx:
            break
        current = predecessors[current]   #moving backwards

    return path_indices


def main():
    graph, station_to_id, id_to_station = build_undirected_graph(
        STATIONS, EDGE_LIST
    )

    # choosing the start station and final destination
    start_label = "A"
    end_label = "E"

    start_idx = station_to_id[start_label] #converting "A" to 0
    end_idx = station_to_id[end_label]  #converting "E" to 4

    distances, predecessors = dijkstra(graph, start_idx)

    path_indices = reconstruct_path(predecessors, start_idx, end_idx)
    path_labels = [id_to_station[i] for i in path_indices] #converting numbers back to station labels again


    print(f"Shortest path from {start_label} to {end_label}:")
    print(" -> ".join(path_labels))
    print(f"Total journey time: {distances[end_idx]} minutes")


if __name__ == "__main__":
    main()
