#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
import networkx as nx
from aoc_utilities import Input, test_input

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def solve1(data):
    """Solves part 1."""
    data = data.splitlines()
    G = nx.DiGraph()

    # initialization
    i = 1
    G.add_node("/", size=0, type="dir")
    current_node = "/"

    while i < len(data):
        line = data[i].split(" ")
        if line[0] == "$":
            i += 1
            if line[1] == "cd":
                if line[2] == "..":
                    current_node = list(G.predecessors(current_node))[0]
                else:
                    current_node = current_node + line[2] + "/"
        else:
            if line[0] == "dir":
                new_node = current_node + line[1] + "/"
                G.add_node(new_node, size=0, type="dir")
                G.add_edge(current_node, new_node)
                i += 1
            else:
                # it's a "file line" !
                new_node = current_node + line[1]
                G.add_node(new_node, size=line[0], type="file")
                G.add_edge(current_node, new_node)
                for ancestor in nx.ancestors(G, new_node):
                    G.nodes[ancestor]["size"] += int(line[0])
                i += 1
    return sum(
        [
            G.nodes[n]["size"]
            for n in G
            if (G.nodes[n]["type"] == "dir" and G.nodes[n]["size"] < 100000)
        ]
    )


def solve2(data):
    """Solves part2."""
    data = data.splitlines()
    G = nx.DiGraph()

    # initialization
    i = 1
    G.add_node("/", size=0, type="dir")
    current_node = "/"

    while i < len(data):
        line = data[i].split(" ")
        if line[0] == "$":
            i += 1
            if line[1] == "cd":
                if line[2] == "..":
                    current_node = list(G.predecessors(current_node))[0]
                else:
                    current_node = current_node + line[2] + "/"
        else:
            if line[0] == "dir":
                new_node = current_node + line[1] + "/"
                G.add_node(new_node, size=0, type="dir")
                G.add_edge(current_node, new_node)
                i += 1
            else:
                # it's a "file line" !
                new_node = current_node + line[1]
                G.add_node(new_node, size=line[0], type="file")
                G.add_edge(current_node, new_node)
                for ancestor in nx.ancestors(G, new_node):
                    G.nodes[ancestor]["size"] += int(line[0])
                i += 1

    used_space = G.nodes["/"]["size"]
    min_size_to_free = used_space - 70000000 + 30000000

    # return [G.nodes[n]["size"] for n in G if G.nodes[n]["size"] > min_size_to_free]
    return min(
        [
            G.nodes[n]["size"]
            for n in G
            if (G.nodes[n]["type"] == "dir" and G.nodes[n]["size"] > min_size_to_free)
        ]
    )


"""
Use script args to execute the right function.
"""
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "1":
        res = solve1((Input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "1t":
        res = solve1((test_input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        res = solve2((Input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2t":
        res = solve2((test_input(DAY).read()))
        print(res)
