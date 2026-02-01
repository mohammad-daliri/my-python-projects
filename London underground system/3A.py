# Task 3(a) — Fewest Stops (BFS), Template B (library-only, clean version)

import sys
import os

# Add CLRS Python paths to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'clrsPython', 'Chapter 20'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'clrsPython', 'Utility functions'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'clrsPython', 'Chapter 10'))

# Import CLRS graph and BFS functions
from adjacency_list_graph import AdjacencyListGraph
from bfs import bfs
from print_path import print_path

# 1) Build the undirected subgraph (each edge = 1 stop)
stations = ["Warwick Avenue", "Paddington", "Edgware Road", "Baker Street", 
            "Bond Street", "Regent's Park", "Oxford Circus"]
station_to_index = {station: idx for idx, station in enumerate(stations)}

G = AdjacencyListGraph(len(stations), directed=False)

# Add edges using vertex indices
G.insert_edge(station_to_index["Warwick Avenue"], station_to_index["Paddington"])
G.insert_edge(station_to_index["Paddington"], station_to_index["Edgware Road"])
G.insert_edge(station_to_index["Edgware Road"], station_to_index["Baker Street"])
G.insert_edge(station_to_index["Baker Street"], station_to_index["Bond Street"])
G.insert_edge(station_to_index["Baker Street"], station_to_index["Regent's Park"])
G.insert_edge(station_to_index["Bond Street"], station_to_index["Oxford Circus"])
G.insert_edge(station_to_index["Regent's Park"], station_to_index["Oxford Circus"])

# 2) Choose start/target
s_name = "Warwick Avenue"
t_name = "Oxford Circus"
s = station_to_index[s_name]
t = station_to_index[t_name]
print("Input stations:", s_name, "->", t_name)

# 3) Run CLRS BFS (returns dist and pi arrays)
dist, pi = bfs(G, s)

# Print the path and distance
path = print_path(pi, s, t, lambda i: stations[i])
if path:
    print("Path:", " -> ".join(path))
    print("Stops:", dist[t])
else:
    print("No path found")
