#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
import logging
from aoc_utilities import Input, test_input, neighbors_4
import networkx as nx

"""
Logger config
  use logger.ingo("") instead of print statement
  those messages will be displayed while running the code on testing sets
  but not displayed while running on real puzzle inputs
  note: when you want to avoid logging, 
  be careful to also skip any expensive computation leading to what you want to log
"""
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def get_map(data):
    m = {}
    for j, line in enumerate(data.splitlines()):
        for i, c in enumerate([c for c in line]):
            m[(i, j)] = c
            if c == "S":
                start = (i, j)
            if c == "E":
                end = (i, j)
    return m, start, end


def get_elevation(m, n):
    if m[n] == "S":
        return ord("a")
    elif m[n] == "E":
        return ord("z")
    else:
        return ord(m[n])


def dist(n1, n2):
    """
    return distance bet
    """


def solve1(data):
    """Solves part 1."""
    m, start, end = get_map(data)
    logger.info(f"m is {m}")
    logger.info(f"end is {end}")
    xmax = max([i for (i, j) in m.keys()])
    ymax = max([j for (i, j) in m.keys()])

    # build graph
    G = nx.DiGraph()

    for n in m.keys():
        for v in neighbors_4(n):
            if v[0] >= 0 and v[0] <= xmax and v[1] >= 0 and v[1] <= ymax:
                if get_elevation(m, v) - get_elevation(m, n) <= 1:
                    G.add_edge(n, v)
                    logger.info(
                        f"adding edge from {m[n]} (elevation = {get_elevation(m, n)}) to {m[v]} (elevation = {get_elevation(m, v)})"
                    )
    logger.info(f"graph is {G.edges()}")

    shortest_path = nx.astar_path(G, start, end)
    logger.info(shortest_path)
    return len(shortest_path) - 1


def solve2(data):
    """Solves part2."""
    m, start, end = get_map(data)
    logger.info(f"m is {m}")
    logger.info(f"end is {end}")
    xmax = max([i for (i, j) in m.keys()])
    ymax = max([j for (i, j) in m.keys()])

    # build graph
    G = nx.DiGraph()

    # initialise with a value I'm sure will be bigger than any shortest path
    all_a_shortest_path = G.nodes()

    for n in m.keys():
        for v in neighbors_4(n):
            if v[0] >= 0 and v[0] <= xmax and v[1] >= 0 and v[1] <= ymax:
                if get_elevation(m, v) - get_elevation(m, n) <= 1:
                    G.add_edge(n, v)
                    logger.info(
                        f"adding edge from {m[n]} (elevation = {get_elevation(m, n)}) to {m[v]} (elevation = {get_elevation(m, v)})"
                    )
    for start in [k for k, v in m.items() if v == "a"]:
        try:  # necessary bc in the input there are some "pockets" of "a" inaccessible from other parts of the graph...
            shortest_path = nx.astar_path(G, start, end)
            if len(shortest_path) < len(all_a_shortest_path):
                all_a_shortest_path = shortest_path
        except:
            pass

    return len(all_a_shortest_path) - 1


"""
Use script args to execute the right function solve1 / solve2, with the right logging level (only activated on test inputs)
  - python dayXX.py 1
  - python dayXX.py 1t
  - python dayXX.py 2
  - python dayXX.py 2t 
"""
if __name__ == "__main__":
    """some logger levels : DEBUG, INFO, WARNING, CRITICAL"""
    if len(sys.argv) > 1 and sys.argv[1] == "1":
        logger.setLevel(logging.WARNING)
        res = solve1((Input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "1t":
        logger.setLevel(logging.INFO)
        res = solve1((test_input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        logger.setLevel(logging.WARNING)
        res = solve2((Input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2t":
        logger.setLevel(logging.INFO)
        res = solve2((test_input(DAY).read()))
        print(res)
