#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import logging
import os
import sys

from aoc_utilities import Input, neighbors_all, test_input, timer_func

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
    grid = set()
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line.strip()):
            if c == "@":
                grid.add((x, y))
    return grid


@timer_func
def solve1(data):
    """Solves part 1."""
    grid = parser(data)
    logger.info(f"grid: {grid}")
    accessible_rolls = 0
    for roll in grid:
        neighbors = neighbors_all(roll)
        neighboring_roll_count = 0
        for neighbor in neighbors:
            if neighbor in grid:
                logger.info(f"neighboring roll at ({roll})")
                neighboring_roll_count += 1
        if neighboring_roll_count < 4:
            accessible_rolls += 1
            logger.info(f"accessible roll at {roll}")

    return accessible_rolls


@timer_func
def solve2(data):
    """Solves part2."""
    pass


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
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "1":
        logger.setLevel(logging.WARNING)
        res = solve1(Input(DAY).read())
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2t":
        logger.setLevel(logging.INFO)
        res = solve2(test_input(DAY).read())
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        logger.setLevel(logging.WARNING)
        res = solve2(Input(DAY).read())
        print(res)
