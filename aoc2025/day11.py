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
    logger.info(f"graph is {G.edges()}")
    PG = nx.nx_pydot.to_pydot(G)
    with open(f"graph_{DAY}.dot", "w") as f:
        f.write(PG.to_string())
    return G


@timer_func
def solve1(data):
    """Solves part 1."""
    G = parser(data)
    return len(list(nx.all_simple_paths(G, "you", "out")))


@timer_func
def solve2(data):
    """Solves part2."""
    G = parser(data)
    counter = 0
    possible_paths = list(nx.all_simple_paths(G, "svr", "out"))
    logger.warning(f"graph contains {len(possible_paths)} paths from svr to out")
    for path in possible_paths:
        logger.warning(f"Analysing path {path} from svr to out")
        if "dac" in path and "fft" in path:
            logger.warning(f"path {path} contains dac and fft")
            counter += 1
    return counter


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
        logger.setLevel(logging.DEBUG)
        res = solve2(Input(DAY).read())
        print(res)
