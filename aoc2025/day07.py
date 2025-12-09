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


@timer_func
def solve1(data):
    """Solves part 1."""
    counter = 0
    lines = [list(line.strip()) for line in data.splitlines()]
    for y in range(1, len(lines)):
        for x, c in enumerate(lines[y]):
            if lines[y - 1][x] == "S" or lines[y - 1][x] == "|":
                if c == "^":
                    counter += 1
                    if (x - 1) >= 0:
                        lines[y][x - 1] = "|"
                    if (x + 1) < len(lines[y]):
                        lines[y][x + 1] = "|"
                elif c == ".":
                    lines[y][x] = "|"

    return counter


@timer_func
def solve2_old(data):
    """Solves part2."""
    lines = [list(line.strip()) for line in data.splitlines()]

    # build graph
    G = nx.DiGraph()

    for y in range(0, len(lines)):
        for x, c in enumerate(lines[y]):
            if y == 0:
                if c == "S":
                    S = (x, y)
                    G.add_node((x, y))
            else:
                if lines[y - 1][x] == "S" or lines[y - 1][x] == "|":
                    if c == "^":
                        G.add_node((x, y))

                        if len(G.nodes) == 2 and x == S[0]:
                            G.add_edge(S, (x, y))
                            logger.info(f"added edge from S to {x, y}")

                        # find predecessors
                        yp = y - 1
                        while lines[yp][x] == "|":
                            if (x - 1) >= 0 and lines[yp][x - 1] == "^":
                                G.add_edge((x - 1, yp), (x, y))
                                logger.info(
                                    f"found predecessor on the left at {x - 1, yp} for {x, y}"
                                )
                            if (x + 1) < len(lines[yp]) and lines[yp][x + 1] == "^":
                                G.add_edge((x + 1, yp), (x, y))
                                logger.info(
                                    f"found predecessor on the right at {x + 1, yp} for {x, y}"
                                )
                            yp -= 1

                        if (x - 1) >= 0:
                            lines[y][x - 1] = "|"
                        if (x + 1) < len(lines[y]):
                            lines[y][x + 1] = "|"
                    elif c == ".":
                        lines[y][x] = "|"

    # add end node
    last_y = len(lines) - 1
    for x, c in enumerate(lines[last_y]):
        if c == "|":
            G.add_node((x, last_y))
            # find predecessors
            yp = last_y - 1
            while lines[yp][x] == "|":
                if (x - 1) >= 0 and lines[yp][x - 1] == "^":
                    G.add_edge((x - 1, yp), (x, last_y))
                    logger.info(
                        f"found predecessor on the left at {x - 1, yp} for {x, last_y}"
                    )
                if (x + 1) < len(lines[yp]) and lines[yp][x + 1] == "^":
                    G.add_edge((x + 1, yp), (x, last_y))
                    logger.info(
                        f"found predecessor on the right at {x + 1, yp} for {x, last_y}"
                    )
                yp -= 1

            G.add_edge((x, last_y), "E")

    logger.info(f"There are {len(G.nodes)}, nodes are {G.nodes()}")
    logger.info(f"edges are {G.edges()}")
    logger.info("all simple edge paths from S to E are :")
    for path in nx.all_simple_paths(G, S, "E"):
        logger.info(f"  - {path}")
    return len(list(nx.all_simple_paths(G, S, "E")))


@timer_func
def solve2(data):
    """Solves part 2."""
    lines = [list(line.strip()) for line in data.splitlines()]
    timelines = [0 for _ in range(len(lines[0]))]
    for x, c in enumerate(lines[0]):
        if c == "S":
            timelines[x] = 1

    for y in range(1, len(lines)):
        new_timelines = timelines.copy()
        for x, c in enumerate(lines[y]):
            if lines[y - 1][x] == "S" or lines[y - 1][x] == "|":
                if c == "^":
                    if (x - 1) >= 0:
                        lines[y][x - 1] = "|"
                        new_timelines[x - 1] += timelines[x]
                        new_timelines[x] = 0
                    if (x + 1) < len(lines[y]):
                        lines[y][x + 1] = "|"
                        new_timelines[x + 1] += timelines[x]
                        new_timelines[x] = 0
                elif c == ".":
                    lines[y][x] = "|"
        logger.info(f"timelines are {timelines}")
        timelines = new_timelines

    return sum(timelines)


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
        expected = 21  # TODO: replace with expected value
        assert res == expected, f"Expected {expected}, got {res}"
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "1":
        logger.setLevel(logging.WARNING)
        res = solve1(Input(DAY).read())
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2t":
        logger.setLevel(logging.INFO)
        res = solve2(test_input(DAY).read())
        expected = 40  # TODO: replace with expected value
        assert res == expected, f"Expected {expected}, got {res}"
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        logger.setLevel(logging.WARNING)
        res = solve2(Input(DAY).read())
        print(res)
