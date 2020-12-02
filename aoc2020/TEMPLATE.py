#!/usr/bin/env python3
"""Template file to be used as boilerplate for each day puzzle."""
from aoc_utilities import Input
import os
# import re
import sys
# import itertools

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


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


"""
Use script args to execute the right function.
"""
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '1':
        res = solve1((Input(DAY).readlines()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        res = solve2((Input(DAY).readlines()))
        print(res)
