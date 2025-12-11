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
    """Draw the graph using pydot and save it to a file.
    can then be used on https://dreampuf.github.io/GraphvizOnline to visualize the graph."""
    PG = nx.nx_pydot.to_pydot(G)
    with open(f"graph_{name}.dot", "w") as f:
        f.write(PG.to_string())
    return


def count_paths_dp(G, source, target):
    """Count paths from source to target using dynamic programming with topological sort.
    Dynamic programming (DP) solves a problem by
      - breaking it into overlapping subproblems (here: How many paths from svr to node X)
      - solving each once, relyng on previous results
      - and storing results to avoid recomputation (here: Store path_counts[node])
    Much faster than nx.all_simple_paths for DAGs (Directed Acyclic Graphs)."""

    # Get topological order
    # which is a *non-unique* list of the nodes of a directed graph
    # such that for any item in the list, all its predecessors are on its left,
    # and all its successors are on its right
    try:
        topo_order = list(nx.topological_sort(G))
    except nx.NetworkXError:
        # Graph has cycles, fall back to slower method
        return len(list(nx.all_simple_paths(G, source, target)))

    # Initialize path counts
    path_counts = dict.fromkeys(G.nodes(), 0)
    path_counts[source] = 1

    # Process nodes in topological order, breadth-first search style
    # we skip source predecessors
    # and we skip target successors
    for node in topo_order:
        if path_counts[node] == 0:
            continue  # skip nodes that can't be reached from the source
        if node == target:
            break  # we've computed path_counts[target], no need to continue
        for successor in G.successors(node):
            path_counts[successor] += path_counts[node]

    return path_counts[target]


@timer_func
def solve2(data):
    """Solves part2."""
    G = parser(data)

    source = "svr"
    target = "out"

    # which intermediary node preceeds the other ?  dac or fft ?
    topo_order = list(nx.topological_sort(G))
    if topo_order.index("dac") < topo_order.index("fft"):
        stop1 = "dac"
        stop2 = "fft"
    else:
        stop1 = "fft"
        stop2 = "dac"

    return (
        count_paths_dp(G, source, stop1)
        * count_paths_dp(G, stop1, stop2)
        * count_paths_dp(G, stop2, target)
    )


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
