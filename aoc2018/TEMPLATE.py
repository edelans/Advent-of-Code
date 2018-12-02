#!/usr/bin/env python3
"""Template file to be used as boilerplate for each day puzzle."""
from aoc_utilities import Input
import aocd
import sys
# import itertools

# day must be 2 digit
DAY = '01'


"""
PART1
"""


def solve1(input):
    """Solves part 1."""
    pass


"""
PART 2
"""


def solve2(input):
    """Solves part2."""
    pass


if sys.argv[1] == '1':
    res = solve1((Input(DAY).readlines()))
    print(res)
    if len(sys.argv) == 3:
        if sys.argv[2] == 's':
            aocd.submit1(res)

if sys.argv[1] == '2':
    res = solve2((Input(DAY).readlines()))
    print(res)
    if len(sys.argv) == 3:
        if sys.argv[2] == 's':
            aocd.submit2(res)
