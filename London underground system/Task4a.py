from clrsPython import AdjacencyListGraph, kruskal

# Reuse the same stations and edges as Task 2a
STATIONS = ["A", "B", "C", "D", "E"]

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
    """Same helper as in Task 2a (you can copy-paste or import)."""
    station_to_id = {name: i for i, name in enumerate(stations)}
    id_to_station = {i: name for name, i in station_to_id.items()}

    graph = AdjacencyListGraph(len(stations), directed=False, weighted=True)

    for u_name, v_name, w in edges:
        u = station_to_id[u_name]
        v = station_to_id[v_name]
        graph.insert_edge(u, v, w)

    return graph, station_to_id, id_to_station


def extract_mst_edges(mst_graph):
    """
    Extract undirected edges from the MST graph as a set of
    (min(u, v), max(u, v)) pairs to avoid duplicates.
    """
    mst_edges = set()

    for u in range(mst_graph.get_card_V()):
        for edge in mst_graph.get_adj_list(u):
            v = edge.get_v()
            pair = tuple(sorted((u, v)))
            mst_edges.add(pair)

    return mst_edges


def main():
    graph, station_to_id, id_to_station = build_undirected_graph(
        STATIONS, EDGE_LIST
    )

    # Run Kruskal to get MST
    mst_graph = kruskal(graph)

    # Get MST edges as index pairs
    mst_edges = extract_mst_edges(mst_graph)

    # Original edges as index pairs (undirected)
    original_edges = {
        tuple(sorted((station_to_id[u], station_to_id[v])))
        for (u, v, _) in EDGE_LIST
    }

    # Edges that can be closed without losing connectivity
    closable_edges = original_edges - mst_edges

    print("Core backbone (MST edges):")
    for u, v in sorted(mst_edges):
        print(f"{id_to_station[u]} -- {id_to_station[v]}")

    print("\nClosable (redundant) edges:")
    for u, v in sorted(closable_edges):
        print(f"{id_to_station[u]} -- {id_to_station[v]}")


if __name__ == "__main__":
    main()
