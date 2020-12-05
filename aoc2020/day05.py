#!/usr/bin/env python3
"""AoC 2020"""

import os
import sys
# import re
# import itertools
from aoc_utilities import Input

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def parser(boarding_pass):
    """Parse input to return tuple (row, column)"""
    return (int(boarding_pass[:7].replace('F', '0').replace('B', '1'), 2),
            int(boarding_pass[7:].replace('L', '0').replace('R', '1'), 2))


def compute_id(seat):
    """returns the id of the boarding pass"""
    return seat[0] * 8 + seat[1]


def solve1(lines):
    """Solves part 1."""
    return max(compute_id(parser(line)) for line in lines)


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
