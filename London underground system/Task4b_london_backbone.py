import pandas as pd
from clrsPython import AdjacencyListGraph, kruskal, dijkstra

# 🔧 update if you move the file
EXCEL_PATH = r"London Underground data.xlsx"

LONG_JOURNEY_START = "Wimbledon"
LONG_JOURNEY_END = "Stratford"


def load_simplified_network(excel_path):
    """
    Load 'London Underground data.xlsx' and produce:
      - stations: list of unique station names
      - edges: list of (u_name, v_name, duration) with one undirected edge
               per pair, using the minimum duration.
    """
    df = pd.read_excel(
        excel_path,
        names=["Line", "Source", "Destination", "Duration (minutes)"]
    )

    # Drop rows where Destination is missing
    df = df.dropna(subset=["Destination"])

    # Canonical undirected endpoints (min, max) so source/dest order doesn't matter
    df["u"] = df[["Source", "Destination"]].min(axis=1)
    df["v"] = df[["Source", "Destination"]].max(axis=1)

    # Keep minimum duration per undirected pair (u, v)
    df_min = (
        df.groupby(["u", "v"])["Duration (minutes)"]
        .min()
        .reset_index()
    )

    # Unique station names
    stations = pd.concat([df_min["u"], df_min["v"]]).unique().tolist()

    # Build edge list (undirected)
    edges = []
    for _, row in df_min.iterrows():
        u_name = row["u"]
        v_name = row["v"]
        w = float(row["Duration (minutes)"])
        edges.append((u_name, v_name, w))

    return stations, edges


def build_undirected_graph(stations, edges):
    """
    Build an AdjacencyListGraph from station names and (u, v, w) edges.
    """
    station_to_id = {name: i for i, name in enumerate(stations)}
    id_to_station = {i: name for name, i in station_to_id.items()}

    g = AdjacencyListGraph(len(stations), directed=False, weighted=True)

    for u_name, v_name, w in edges:
        u = station_to_id[u_name]
        v = station_to_id[v_name]
        g.insert_edge(u, v, w)

    return g, station_to_id, id_to_station


def extract_mst_edges_and_weight(mst_graph, id_to_station):
    """
    Extract MST edges and total MST weight.
    Returns:
      - mst_edges_named: list of (station_u, station_v)
      - total_weight: float
    """
    edge_set = set()
    total_weight = 0.0

    for u in range(mst_graph.get_card_V()):
        for edge in mst_graph.get_adj_list(u):
            v = edge.get_v()
            w = edge.get_weight()

            a, b = sorted((u, v))
            if (a, b) in edge_set:
                continue  # skip duplicate undirected edge
            edge_set.add((a, b))
            total_weight += w

    mst_edges_named = []
    for a, b in edge_set:
        mst_edges_named.append((id_to_station[a], id_to_station[b]))

    return mst_edges_named, total_weight


def shortest_path_dijkstra(graph, station_to_id, id_to_station, start_name, end_name):
    """
    Run Dijkstra using CLRS and reconstruct path and total time
    between start_name and end_name.
    """
    if start_name not in station_to_id or end_name not in station_to_id:
        raise ValueError(f"Start or end station not found: {start_name}, {end_name}")

    start = station_to_id[start_name]
    end = station_to_id[end_name]

    dist, pi = dijkstra(graph, start)

    # Reconstruct path
    path_indices = []
    current = end
    while current is not None:
        path_indices.insert(0, current)
        if current == start:
            break
        current = pi[current]

    path_names = [id_to_station[i] for i in path_indices]
    total_time = dist[end]
    return path_names, total_time


def main():
    # 1) Load and simplify London Underground network
    stations, edges = load_simplified_network(EXCEL_PATH)
    full_graph, station_to_id, id_to_station = build_undirected_graph(stations, edges)

    # 2) Compute MST (core backbone)
    mst_graph = kruskal(full_graph)
    mst_edges_named, total_backbone_time = extract_mst_edges_and_weight(
        mst_graph, id_to_station
    )

    print("Total journey time (weight) of core network backbone:")
    print(total_backbone_time)

    # 3) Compute redundant edges (present in original, not in MST)
    mst_edge_set = {tuple(sorted(pair)) for pair in mst_edges_named}
    original_edge_set = {
        tuple(sorted((u, v))) for (u, v, _) in edges
    }

    redundant_pairs = original_edge_set - mst_edge_set

    print("\nExample redundant connections:")
    for i, (a, b) in enumerate(sorted(redundant_pairs)):
        if i >= 10:
            break
        print(f"{a} -- {b}")

    # 4) Impact analysis on one long journey
    start_station = LONG_JOURNEY_START
    end_station = LONG_JOURNEY_END

    # Shortest path in full network
    full_path, full_time = shortest_path_dijkstra(
        full_graph, station_to_id, id_to_station, start_station, end_station
    )

    print(f"\nOriginal network shortest path from {start_station} to {end_station}:")
    print(" -> ".join(full_path))
    print(f"Total journey time: {full_time} minutes")

    # Build MST-only graph with correct weights
    mst_graph_only = AdjacencyListGraph(len(stations), directed=False, weighted=True)
    # Add MST edges with their weights from the original edges list
    edge_weight_lookup = {}
    for (u_name, v_name, w) in edges:
        a, b = sorted((u_name, v_name))
        edge_weight_lookup[(a, b)] = w

    for (u_name, v_name) in mst_edge_set:
        a, b = sorted((u_name, v_name))
        w = edge_weight_lookup[(a, b)]
        u = station_to_id[u_name]
        v = station_to_id[v_name]
        mst_graph_only.insert_edge(u, v, w)

    # Shortest path on backbone-only network
    backbone_path, backbone_time = shortest_path_dijkstra(
        mst_graph_only, station_to_id, id_to_station, start_station, end_station
    )

    print(f"\nBackbone-only network shortest path from {start_station} to {end_station}:")
    print(" -> ".join(backbone_path))
    print(f"Total journey time on backbone: {backbone_time} minutes")

    print("\nImpact analysis:")
    print(f"Extra journey time when using backbone only: {backbone_time - full_time} minutes")


if __name__ == "__main__":
    main()
