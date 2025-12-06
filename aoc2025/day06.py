#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import logging
import os
import sys
from math import prod

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
    lines = data.strip().splitlines()
    ops = [op for op in lines[-1].split()]
    lines = lines[:-1]
    numbers = []
    for line in lines:
        numbers.append([int(n) for n in line.split()])

    return numbers, ops


@timer_func
def solve1(data):
    """Solves part 1."""
    numbers, ops = parser(data)
    logger.info(f"numbers: {numbers}, \nops: {ops}")
    acc = 0
    for x, op in enumerate(ops):
        if op == "+":
            acc += sum([n[x] for n in numbers])
        elif op == "*":
            acc += prod([n[x] for n in numbers])

    return acc


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
        expected = 4277556  # TODO: replace with expected value
        assert res == expected, f"Expected {expected}, got {res}"
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "1":
        logger.setLevel(logging.WARNING)
        res = solve1(Input(DAY).read())
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2t":
        logger.setLevel(logging.INFO)
        res = solve2(test_input(DAY).read())
        # expected = XXX  # TODO: replace with expected value
        # assert res == expected, f"Expected {expected}, got {res}"
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        logger.setLevel(logging.WARNING)
        res = solve2(Input(DAY).read())
        print(res)
