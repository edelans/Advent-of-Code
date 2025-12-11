#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import logging
import os
import sys

import networkx as nx

from aoc_utilities import Input, test_input, timer_func

"""
Logger config
  use logger.info("") instead of print statement
  those messages will be displayed while running the code on testing sets
  but not displayed while running on real puzzle inputs
"""
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def parser(data):
    G = nx.DiGraph()
    for line in data.splitlines():
        left, right = line.split(":")
        G.add_node(left.strip())
        for neighbour in right.strip().split(" "):
            G.add_node(neighbour.strip())
            G.add_edge(left, neighbour)
    logger.debug(f"graph is {G.edges()}")

    return G


@timer_func
def solve1(data):
    """Solves part 1."""
    G = parser(data)
    return len(list(nx.all_simple_paths(G, "you", "out")))


def simplify_graph(G):
    """Remove nodes with exactly one parent and one child, connecting parent to child directly."""
    G = G.copy()  # work on a copy to avoid modifying original

    changed = True
    while changed:
        changed = False
        nodes_to_remove = []
        edges_to_add = []

        for node in list(G.nodes()):
            predecessors = list(G.predecessors(node))
            successors = list(G.successors(node))

            # Check if node has exactly one parent and one child
            if len(predecessors) == 1 and len(successors) == 1:
                parent = predecessors[0]
                child = successors[0]

                # Don't create self-loops
                if parent != child:
                    edges_to_add.append((parent, child))
                    nodes_to_remove.append(node)
                    changed = True

        # Apply changes
        for parent, child in edges_to_add:
            G.add_edge(parent, child)
        G.remove_nodes_from(nodes_to_remove)

    return G


def draw_graph(G, name):
    PG = nx.nx_pydot.to_pydot(G)
    with open(f"graph_{name}.dot", "w") as f:
        f.write(PG.to_string())
    return


def count_paths_dp(G, source, target):
    """Count paths from source to target using dynamic programming with topological sort.
    Much faster than nx.all_simple_paths for DAGs."""
    # Get topological order
    try:
        topo_order = list(nx.topological_sort(G))
    except nx.NetworkXError:
        # Graph has cycles, fall back to slower method
        return len(list(nx.all_simple_paths(G, source, target)))

    # Initialize path counts
    path_counts = dict.fromkeys(G.nodes(), 0)
    path_counts[source] = 1

    # Process nodes in topological order
    for node in topo_order:
        if path_counts[node] == 0:
            continue
        for successor in G.successors(node):
            path_counts[successor] += path_counts[node]

    return path_counts[target]


def find_articulation_points(G):
    """Find articulation points (nodes whose removal increases number of connected components).
    These are good candidates for 'hubs'."""
    # Convert to undirected for articulation point detection
    G_undirected = G.to_undirected()
    return list(nx.articulation_points(G_undirected))


def find_high_betweenness_nodes(G, top_k=None):
    """Find nodes with high betweenness centrality - nodes on many shortest paths.
    Good candidates for 'hubs'."""
    betweenness = nx.betweenness_centrality(G)
    sorted_nodes = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)
    if top_k:
        return [node for node, _ in sorted_nodes[:top_k]]
    return sorted_nodes


def decompose_by_articulation_points(G, source, target):
    """Decompose graph by removing articulation points, creating subgraphs.
    Returns list of subgraphs and the articulation points."""
    G_undirected = G.to_undirected()
    articulation_points = list(nx.articulation_points(G_undirected))

    # Create subgraphs by removing articulation points
    subgraphs = []
    G_copy = G.copy()
    for ap in articulation_points:
        if ap == source or ap == target:
            continue  # Don't remove source/target
        G_copy.remove_node(ap)
        # Get connected components
        for component in nx.weakly_connected_components(G_copy):
            if len(component) > 1:
                subgraphs.append(G.subgraph(component).copy())
        G_copy = G.copy()  # Reset for next iteration

    return subgraphs, articulation_points


def find_biconnected_components(G):
    """Find biconnected components - maximal sets of nodes where removal of any single node
    doesn't disconnect the component. Useful for graph decomposition."""
    G_undirected = G.to_undirected()
    return list(nx.biconnected_components(G_undirected))


def auto_identify_layers(G, source, target):
    """Automatically identify layers/hubs using BFS from source.
    Returns list of layers, where each layer contains nodes at the same distance from source."""
    # BFS to find distances from source
    distances = nx.single_source_shortest_path_length(G, source)
    target_dist = distances.get(target)
    if target_dist is None:
        return []

    # Group nodes by distance
    layers = [[] for _ in range(target_dist + 1)]
    for node, dist in distances.items():
        if dist <= target_dist:
            layers[dist].append(node)

    return layers


@timer_func
def solve2(data):
    """Solves part2."""
    G = parser(data)

    source = "svr"
    target = "out"

    # Option 1: Use DP with topological sort (fastest, no decomposition needed)
    return count_paths_dp(G, source, target)

    # Option 2: Auto-identify layers and use DP between layers
    # layers = auto_identify_layers(G, source, target)
    # if not layers:
    #     return 0
    #
    # path_counts = {source: 1}
    # for layer in layers[1:]:
    #     new_path_counts = {}
    #     for node in layer:
    #         count = 0
    #         for pred in G.predecessors(node):
    #             if pred in path_counts:
    #                 # Count paths from pred to node using DP on subgraph
    #                 # For efficiency, we can use the fact that path_counts[pred] already
    #                 # contains the count from source to pred
    #                 subgraph_paths = count_paths_dp(G, pred, node)
    #                 count += path_counts[pred] * subgraph_paths
    #         new_path_counts[node] = count
    #     path_counts = new_path_counts
    #
    # return path_counts.get(target, 0)

    # Option 3: Use manual hubs (your original approach, but with DP instead of all_simple_paths)
    # hubs = [
    #     ["svr"],
    #     ["ekx", "hmh", "qwm"],
    #     ["kox", "pwk", "ehb", "uvj"],
    #     ["iza", "tup", "qlh"],
    #     ["oas", "vwj", "tui"],
    #     ["eyi", "fmj", "gnu", "ugv", "mha"],
    #     ["you", "heu", "cgh"],
    #     ["out"],
    # ]
    #
    # path_counts = {"svr": 1}
    # for i, hub in enumerate(hubs[1:], start=1):
    #     previous_hub_nodes = hubs[i - 1]
    #     new_path_counts = {}
    #     for node in hub:
    #         total = 0
    #         for predecessor in previous_hub_nodes:
    #             if predecessor in path_counts:
    #                 # Use DP instead of all_simple_paths
    #                 incoming_paths = count_paths_dp(G, predecessor, node)
    #                 total += incoming_paths * path_counts[predecessor]
    #         new_path_counts[node] = total
    #     path_counts = new_path_counts
    #
    # return path_counts.get("out", 0)


"""
Use script args to execute the right function solve1 / solve2, with the right logging level (only activated on test inputs)
  - python dayXX.py 1
  - python dayXX.py 1t
  - python dayXX.py 2
  - python dayXX.py 2t
"""
if __name__ == "__main__":
    """some logger levels : DEBUG, INFO, WARNING, CRITICAL"""
    if len(sys.argv) > 1 and sys.argv[1] == "1t":
        logger.setLevel(logging.INFO)
        res = solve1(test_input(DAY).read())
        expected = 5  # TODO: replace with expected value
        assert res == expected, f"Expected {expected}, got {res}"
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "1":
        logger.setLevel(logging.WARNING)
        res = solve1(Input(DAY).read())
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2t":
        logger.setLevel(logging.INFO)
        res = solve2("""svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out""")
        expected = 2  # TODO: replace with expected value
        assert res == expected, f"Expected {expected}, got {res}"
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        logger.setLevel(logging.WARNING)
        res = solve2(Input(DAY).read())
        print(res)
