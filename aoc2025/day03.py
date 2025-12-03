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


def largest_joltage(bank):
    batt1 = int(bank[0])
    batt2 = int(bank[1])
    logger.debug(f"computing largest joltage for {bank}")
    for i in range(1, len(bank)):
        battery = int(bank[i])
        if battery > batt1 and i < len(bank) - 1:
            batt1 = battery
            batt2 = int(bank[i + 1])
        elif battery > batt2:
            batt2 = battery
    return int(str(batt1) + str(batt2))


def _test_largest_joltage():
    cases = (
        ("987654321111111", 98),
        ("811111111111119", 89),
        ("234234234234278", 78),
        ("818181911112111", 92),
    )
    for digits, expected in cases:
        result = largest_joltage(digits)
        assert result == expected, (
            f"largest_joltage({digits}) -> {result}, expected {expected}"
        )


@timer_func
def solve1(data):
    """Solves part 1."""
    acc = 0
    for bank in data.splitlines():
        acc += largest_joltage(bank)
    return acc


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
        _test_largest_joltage()
        res = solve1(test_input(DAY).read())
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "1":
        logger.setLevel(logging.WARNING)
        res = solve1(Input(DAY).read())
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2t":
        logger.setLevel(logging.INFO)
        _test_largest_joltage12()
        res = solve2(test_input(DAY).read())
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        logger.setLevel(logging.WARNING)
        res = solve2(Input(DAY).read())
        print(res)
