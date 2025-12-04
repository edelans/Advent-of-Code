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


def parser(data: str) -> set[tuple[int, int]]:
    grid = set()
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line.strip()):
            if c == "@":
                grid.add((x, y))
    return grid


@timer_func
def solve1(data: str) -> int:
    """Solves part 1."""
    grid = parser(data)
    accessible_rolls = 0
    for roll in grid:
        neighbors = neighbors_all(roll)
        neighboring_rolls = neighbors & grid
        if len(neighboring_rolls) < 4:
            accessible_rolls += 1

    return accessible_rolls


def remove_rolls(grid: set[tuple[int, int]]) -> set[tuple[int, int]]:
    # As it is not allowed to modify a set while iterating on it
    # we iterate on a "list" copy of the set created by list()
    for roll in list(grid):
        neighbors = neighbors_all(roll)
        neighboring_rolls = neighbors & grid
        if len(neighboring_rolls) < 4:
            grid.remove(roll)
    return grid


@timer_func
def solve2(data: str) -> int:
    """Solves part2."""
    grid = parser(data)
    initial_count = len(grid)

    prev_count = initial_count
    while True:
        grid = remove_rolls(grid)
        new_count = len(grid)
        if new_count == prev_count:
            break
        logger.info(f"new iteration removed {prev_count - new_count} rolls")
        prev_count = new_count

    return initial_count - new_count


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
        expected = 13
        assert res == expected, f"Expected {expected}, got {res}"
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "1":
        logger.setLevel(logging.WARNING)
        res = solve1(Input(DAY).read())
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2t":
        logger.setLevel(logging.INFO)
        res = solve2(test_input(DAY).read())
        expected = 43
        assert res == expected, f"Expected {expected}, got {res}"
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        logger.setLevel(logging.WARNING)
        res = solve2(Input(DAY).read())
        print(res)
