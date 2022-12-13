#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
import logging
from aoc_utilities import Input, test_input
from functools import cmp_to_key

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


def compare(p1, p2):
    p1_is_int = type(p1) is int
    p2_is_int = type(p2) is int

    if p1_is_int and p2_is_int:
        return p1 - p2
    elif p1_is_int and not p2_is_int:
        return compare([p1], p2)
    elif not p1_is_int and p2_is_int:
        return compare(p1, [p2])
    else:
        # both are lists
        logger.info(f"p1 is {p1}, p2 is {p2}")
        for x, y in zip(p1, p2):
            res = compare(x, y)
            if res != 0:
                return res

        # zip generates a list of the size of the smallest arg
        # if nothing has been returned yet, we need to compare the size of the lists :
        return len(p1) - len(p2)


def solve1(data):
    """Solves part 1."""
    s = 0  # sum of indices

    for i, pairs in enumerate(data.split("\n\n"), 1):
        # tough luck: input lines are valid python list, let's just eval() them
        p1, p2 = map(eval, pairs.splitlines())
        if compare(p1, p2) < 0:
            s += i
            logger.info(
                f"for pairs at indice {i}, packet {p1} is smaller than {p2}\ns is {s}\n\n"
            )

    return s


def solve2(data):
    """Solves part2."""
    all_packets = [[[2]], [[6]]]

    for pairs in data.split("\n\n"):
        # tough luck: input lines are valid python list, let's just eval() them
        p1, p2 = map(eval, pairs.splitlines())
        all_packets.append(p1)
        all_packets.append(p2)

    sorted_packets = sorted(all_packets, key=cmp_to_key(compare))
    return (sorted_packets.index([[2]]) + 1) * (sorted_packets.index([[6]]) + 1)


"""
Use script args to execute the right function solve1 / solve2, with the right logging level (only activated on test inputs)
  - time python dayXX.py 1
  - time python dayXX.py 1t
  - time python dayXX.py 2
  - time python dayXX.py 2t 
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
