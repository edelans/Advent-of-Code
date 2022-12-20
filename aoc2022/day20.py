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
    seq = deque([])
    for line in data.splitlines():
        seq.append(int(line))
    iseq = list(seq)  # initial sequence, in an independant copy
    size = len(iseq)

    for i in iseq:
        # print(f"\nmoving {i}:")
        idx = seq.index(i)
        seq.rotate(-idx)
        seq.popleft()
        seq.rotate(-i)
        seq.appendleft(i)
        # print(f"seq is: {list(seq)}")

    seq.rotate(-seq.index(0))
    print(f"seq is: {list(seq)}")
    return (
        seq[1000 % size],
        seq[2000 % size],
        seq[3000 % size],
        seq[1000 % size] + seq[2000 % size] + seq[3000 % size],
    )
    # 11092 too high
    # -16196 no


"""
    >>> from collections import deque
    >>> circle = deque([1,2,3,4])

    >>> circle.rotate(1)
    >>> circle
    deque([4, 1, 2, 3])

    >>> circle.pop()
    3

    >>> circle.append(5)
    >>> circle
    deque([4, 1, 2, 5])
"""


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
