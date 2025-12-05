#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import logging
import os
import sys

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


def parser(data: str) -> list[tuple[int, int]]:
    ranges, ingredients = data.strip().split("\n\n")
    ranges = [tuple(map(int, range.split("-"))) for range in ranges.splitlines()]
    ingredients = [int(ingredient) for ingredient in ingredients.splitlines()]
    return ranges, ingredients


def compact_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    ranges.sort(key=lambda x: x[0])
    compacted_ranges = []
    for range in ranges:
        if compacted_ranges and compacted_ranges[-1][1] >= range[0]:
            compacted_ranges[-1] = (
                compacted_ranges[-1][0],
                max(compacted_ranges[-1][1], range[1]),
            )
        else:
            compacted_ranges.append(range)
    return compacted_ranges


@timer_func
def solve1(data):
    """Solves part 1."""
    ranges, ingredients = parser(data)
    logger.info(f"ranges: {ranges}")
    logger.info(f"ingredients: {ingredients}")
    ranges = compact_ranges(ranges)
    logger.info(f"compacted ranges: {ranges}")
    fresh_ingredients = []
    for ingredient in ingredients:
        for range in ranges:
            if range[0] <= ingredient <= range[1]:
                fresh_ingredients.append(ingredient)
                logger.info(f"ingredient {ingredient} is fresh")
    logger.info(f"fresh ingredients: {fresh_ingredients}")
    return len(fresh_ingredients)


@timer_func
def solve2(data):
    """Solves part2."""
    ranges, ingredients = parser(data)
    ranges = compact_ranges(ranges)
    return sum(range[1] - range[0] + 1 for range in ranges)


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
        expected = 3
        assert res == expected, f"Expected {expected}, got {res}"
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "1":
        logger.setLevel(logging.WARNING)
        res = solve1(Input(DAY).read())
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2t":
        logger.setLevel(logging.INFO)
        res = solve2(test_input(DAY).read())
        expected = 14
        assert res == expected, f"Expected {expected}, got {res}"
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        logger.setLevel(logging.WARNING)
        res = solve2(Input(DAY).read())
        print(res)
