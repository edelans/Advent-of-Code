#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
import networkx as nx
from aoc_utilities import Input, test_input
# import re
# import itertools

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def graph(input):
    G = nx.DiGraph()
    for line in input:
        # clear crimson bags contain 3 pale aqua bags, 4 plaid magenta bags, 3 dotted beige bags, 3 dotted black bags.
        node, edges = line.split("contain")
        edges = edges.strip().split(", ")
        node = ' '.join(node.split(' ')[0:2])
        if edges[0] != "no other bags.":
            for e in edges:
                w = e.strip().split(' ')
                G.add_edge(node, ' '.join(w[1:3]), weight=int(w[0]))
    return G


def accumulate_predecessors(G, n, prede):
    for p in G.predecessors(n):
        if p not in prede:
            prede.add(p)
            prede.union(accumulate_predecessors(G, p, prede))
    return prede


def solve1(input):
    """Solves part 1."""
    G = graph(input)
    return len(accumulate_predecessors(G, "shiny gold", set()))


def count_bags_in(G, node):
    bag_count = 0
    for n, val in G[node].items():
        bag_count += val["weight"] * count_bags_in(G, n) + val["weight"]
    return bag_count


def solve2(input):
    """Solves part2."""
    G = graph(input)
    return count_bags_in(G, "shiny gold")


"""
Use script args to execute the right function.
"""
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '1':
        res = solve1((Input(DAY).readlines()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '1t':
        res = solve1((test_input(DAY).readlines()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        res = solve2((Input(DAY).readlines()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '2t':
        res = solve2((test_input(DAY).readlines()))
        print(res)
