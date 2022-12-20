#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
import logging
from aoc_utilities import Input, test_input
from collections import deque


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


def solve1(data):
    """Solves part 1."""
    l = []
    for line in data.splitlines():
        l.append(int(line))
    print(f"input has {len(l)} values, and {len(set(l))} unique values.")
    size = len(l)

    # there a re duplicate values in input, we need to introduce an id for each value
    list_with_ids = [*enumerate(l)]  # l = [1, 2, -3, 3, -2, 0, 4] would yield
    # [(0, 1), (1, 2), (2, -3), (3, 3), (4, -2), (5, 0), (6, 4)]

    original_list_with_ids = (
        list_with_ids.copy()
    )  # storing an independant copy so we can iterate on it while modifying list_with_ids

    for id, i in original_list_with_ids:
        idx = list_with_ids.index((id, i))
        list_with_ids.pop(idx)
        list_with_ids.insert((idx + i) % (size - 1), (id, i))
    res = [x for _, x in list_with_ids]
    return sum([res[(res.index(0) + 1000 * p) % size] for p in [1, 2, 3]])


def solve2(data):
    """Solves part2."""
    l = []
    for line in data.splitlines():
        l.append(int(line) * 811589153)
    print(f"input has {len(l)} values, and {len(set(l))} unique values.")
    size = len(l)

    # there a re duplicate values in input, we need to introduce an id for each value
    list_with_ids = [*enumerate(l)]  # l = [1, 2, -3, 3, -2, 0, 4] would yield
    # [(0, 1), (1, 2), (2, -3), (3, 3), (4, -2), (5, 0), (6, 4)]
    print(list_with_ids)

    original_list_with_ids = (
        list_with_ids.copy()
    )  # storing an independant copy so we can iterate on it while modifying list_with_ids

    for _ in range(10):
        for id, i in original_list_with_ids:
            idx = list_with_ids.index((id, i))
            list_with_ids.pop(idx)
            list_with_ids.insert((idx + i) % (size - 1), (id, i))
    res = [x for _, x in list_with_ids]
    return sum([res[(res.index(0) + 1000 * p) % size] for p in [1, 2, 3]])


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
        res = solve1((test_input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "1":
        logger.setLevel(logging.WARNING)
        res = solve1((Input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2t":
        logger.setLevel(logging.INFO)
        res = solve2((test_input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        logger.setLevel(logging.WARNING)
        res = solve2((Input(DAY).read()))
        print(res)
