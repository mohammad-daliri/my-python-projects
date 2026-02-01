# 2(b) — London Underground shortest-time paths (CLRS Dijkstra)
# - Loads network from Excel
# - Cleans & deduplicates edges (keep MIN time per station pair)
# - Runs two tests: short and long journey
# - Uses ONLY CLRS library functions for the algorithm & path printing

import os
import sys
import pandas as pd

# ---------- Locate this script's folder ----------
if '__file__' in globals():
    BASE = os.path.dirname(os.path.abspath(__file__))
else:
    BASE = os.getcwd()

# ---------- Add CLRS library folders to path (adjust only if your layout differs) ----------
sys.path.extend([
    os.path.join(BASE, 'clrsPython', 'Chapter 22'),
    os.path.join(BASE, 'clrsPython', 'Chapter 20'),
    os.path.join(BASE, 'clrsPython', 'Chapter 10'),
    os.path.join(BASE, 'clrsPython', 'Chapter 6'),
    os.path.join(BASE, 'clrsPython', 'Utility functions'),
])

# ---------- CLRS imports (algorithm, graph, path printer) ----------
from dijkstra import dijkstra                      # CLRS shortest-time algorithm
from adjacency_list_graph import AdjacencyListGraph
from print_path import print_path                  # CLRS path printer


# ---------- Data loader (robust to 3 or 4 columns, dedup to MIN time) ----------
def load_london_underground_from_excel(excel_file):
    """
    Build a weighted, undirected graph from an LU Excel file.
    Accepts either:
      - 3 columns: From, To, Minutes
      - 4 columns: Line, From, To, Minutes
    Returns: (Graph, station_to_index, index_to_station)
    """
    if not os.path.exists(excel_file):
        raise FileNotFoundError(f"Excel file not found: {excel_file}")

    # Try with a header row first (rename flexibly), else fallback to raw and assign names
    df = None
    try:
        df0 = pd.read_excel(excel_file, header=0)
        cols_lower = [str(c).strip().lower() for c in df0.columns]
        rename_map = {}
        for raw, c in zip(df0.columns, cols_lower):
            if 'from' in c:
                rename_map[raw] = 'From'
            elif c == 'to' or 'to' in c:
                rename_map[raw] = 'To'
            elif 'minute' in c or 'time' in c or 'duration' in c:
                rename_map[raw] = 'Minutes'
            elif 'line' in c:
                rename_map[raw] = 'Line'
        if {'From', 'To', 'Minutes'}.issubset(set(rename_map.values())):
            keep = ['From', 'To', 'Minutes']
            if 'Line' in rename_map.values():
                keep.append('Line')
            df = df0.rename(columns=rename_map)[keep]
    except Exception:
        pass

    if df is None:
        df_raw = pd.read_excel(excel_file, header=None)
        ncols = df_raw.shape[1]
        if ncols == 4:
            df_raw.columns = ['Line', 'From', 'To', 'Minutes']
        elif ncols == 3:
            df_raw.columns = ['From', 'To', 'Minutes']
        else:
            raise ValueError(f"Unexpected number of columns: {ncols} (expected 3 or 4)")
        df = df_raw

    if df.empty:
        raise ValueError("Excel file contains no data rows")

    # Clean names and times; drop heading/blank rows
    df['From'] = df['From'].astype(str).str.strip()
    df['To']   = df['To'].astype(str).str.strip()
    df['Minutes'] = pd.to_numeric(df['Minutes'], errors='coerce')

    df = df[
        (df['From'].ne('')) & (df['From'].str.lower().ne('nan')) &
        (df['To'].ne(''))   & (df['To'].str.lower().ne('nan')) &
        (df['Minutes'].notna())
    ].copy()

    if df.empty:
        raise ValueError("No valid connection rows after cleaning")

    if (df['Minutes'] < 0).any():
        raise ValueError("Found negative durations; please fix the data")

    # Deduplicate: undirected pair -> keep MIN time
    df['u'] = df[['From', 'To']].min(axis=1)
    df['v'] = df[['From', 'To']].max(axis=1)
    df_edges = df.groupby(['u', 'v'], as_index=False)['Minutes'].min()

    # Build station index maps
    stations = sorted(set(df_edges['u']) | set(df_edges['v']))
    to_idx = {s: i for i, s in enumerate(stations)}
    to_name = {i: s for s, i in to_idx.items()}

    # Build weighted, undirected graph
    G = AdjacencyListGraph(len(stations), directed=False, weighted=True)
    for _, r in df_edges.iterrows():
        G.insert_edge(to_idx[r['u']], to_idx[r['v']], float(r['Minutes']))

    print(f"Successfully loaded {len(df_edges)} connections between {len(stations)} stations")
    return G, to_idx, to_name


# ---------- Helpers ----------
def find_station_name(query, to_idx):
    """Case-insensitive, trimmed station lookup."""
    q = query.strip()
    if q in to_idx:
        return q
    ql = q.lower()
    for name in to_idx.keys():
        if name.lower() == ql:
            return name
    return None


def run_test(G, to_idx, to_name, start, end, label):
    print(f"\n=== {label} ===")
    print(f"Input: {start} → {end}")

    s_name = find_station_name(start, to_idx)
    t_name = find_station_name(end, to_idx)
    if s_name is None or t_name is None:
        print("Station name not found in network.")
        return

    s, t = to_idx[s_name], to_idx[t_name]

    # CLRS Dijkstra call (algorithm)
    dist, pred = dijkstra(G, s)

    # CLRS path printer (no custom reconstruction)
    route = print_path(pred, s, t, lambda i: to_name[i])

    if not route:
        print("No route found.")
        return

    print("Route:", " → ".join(route))
    print("Total journey time:", dist[t], "minutes")
    print("Number of stations:", len(route))


# ---------- Main ----------
def main():
    # Try common filenames in the script folder
    candidates = [
        os.path.join(BASE, "London Underground data.xlsx"),
        os.path.join(BASE, "London_Underground.xlsx"),
        os.path.join(BASE, "London Underground.xlsx"),
    ]
    excel_file = next((p for p in candidates if os.path.exists(p)), None)
    if excel_file is None:
        # Let user provide a path if the common names aren't found
        excel_file = input("Excel path: ").strip()

    print(f"Loading London Underground network from '{excel_file}'...")
    try:
        G, to_idx, to_name = load_london_underground_from_excel(excel_file)
        print(f"Network loaded. Stations: {len(to_idx)}")
    except Exception as e:
        print("Error loading Excel:", e)
        print("Ensure the sheet has columns (From, To, Minutes) "
              "or (Line, From, To, Minutes).")
        return

    # Spec asks for TWO tests: one short, one long
    run_test(G, to_idx, to_name, "Covent Garden", "Leicester Square", "SHORT JOURNEY (CLRS Dijkstra)")
    run_test(G, to_idx, to_name, "Wimbledon", "Stratford", "LONG JOURNEY (CLRS Dijkstra)")

    print("\nAll tests complete. Take screenshots of the outputs above for your report.")

if __name__ == "__main__":
    main()
