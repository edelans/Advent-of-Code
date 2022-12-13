#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
import logging
from aoc_utilities import Input, test_input

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


def left_is_smaller(p1, p2):
    # [1,1,3,1,1]
    # [1,1,5,1,1]
    if p1[0] == p2[0]:
        return left_is_smaller(p1[1:], p2[1:])
    if p1 == None:
        return True
    else:
        logger.info(f"p1[0] is {p1[0]}, p2[0] is {p2[0]}")
        if p1[0].isdigit() and p2[0].isdigit():
            return int(p1[0]) < int(p2[0])
        elif p1[0].isdigit() and not p2[0].isdigit():
            if p2[1:]:
                return left_is_smaller(p1, p2[1:])
            else:
                # Right side ran out of items
                return False
        elif not p1[0].isdigit() and p2[0].isdigit():
            if p1[1:]:
                return left_is_smaller(p1[1:], p2)
            else:
                # Left side ran out of items
                return True
        else:
            if p1[0] == ",":
                return False
            elif p2[0] == ",":
                return True


def solve1(data):
    """Solves part 1."""
    s = 0  # sum of indices

    for i, pairs in enumerate(data.split("\n\n")):
        p1, p2 = pairs.splitlines()
        if left_is_smaller(p1, p2):
            s += i + 1
            logger.info(
                f"for pairs at indice {i + 1}, packet {p1} is smaller than {p2}\ns is {s}\n\n"
            )
        else:
            logger.info(
                f"for pairs at indice {i + 1}, packet {p1} is NOT smaller than {p2}\n\n"
            )

    return s
    # 5382 too high


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
    if len(sys.argv) > 1 and sys.argv[1] == "1":
        logger.setLevel(logging.INFO)
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
