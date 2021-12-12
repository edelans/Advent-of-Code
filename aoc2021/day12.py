#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input
import networkx as nx


# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def parser(data):
    G = nx.Graph()
    for line in data.splitlines():
        source,target = line.split("-")
        G.add_edge(source, target)
    return G


def solve1(data):
    """Solves part 1."""
    G = parser(data)
    complete_paths = []
    investigating_paths = [["start"]]

    while len(investigating_paths) > 0:
        p = investigating_paths[0]
        investigating_paths = investigating_paths[1:]

        for neighbor in nx.neighbors(G, p[-1]):
            if neighbor == neighbor.lower() and neighbor in p:
                pass
            elif neighbor == "end":
                np = p + [neighbor]
                complete_paths.append(np)
            else:
                np = p + [neighbor]
                investigating_paths.append(np)

    return print(f"there are {len(complete_paths)} possible paths")


def isALowerValueAlreadyPresentTwice(path):
    for n in path:
        if n == n.lower():
            if path.count(n) > 1:
                return True
    return False

def solve2(data):
    """Solves part2."""
    G = parser(data)
    complete_paths = []
    investigating_paths = [["start"]]

    while len(investigating_paths) > 0:
        p = investigating_paths[0]
        investigating_paths = investigating_paths[1:]

        for neighbor in nx.neighbors(G, p[-1]):
            if neighbor == "start":
                pass
            elif neighbor == neighbor.lower() and neighbor in p:
                if not isALowerValueAlreadyPresentTwice(p):
                    np = p + [neighbor]
                    investigating_paths.append(np)
            elif neighbor == "end":
                np = p + [neighbor]
                complete_paths.append(np)
            else:
                np = p + [neighbor]
                investigating_paths.append(np)

    print(f"there are {len(complete_paths)} possible paths")
    return


"""
Use script args to execute the right function.
"""
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '1':
        res = solve1((Input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '1t':
        res = solve1((test_input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        res = solve2((Input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '2t':
        res = solve2((test_input(DAY).read()))
        print(res)
