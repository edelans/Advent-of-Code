#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input
# import re
# import itertools

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def count_uniq_char(s):
    return len(set(s))


def solve1(inp):
    groups = inp.split("\n\n")
    return sum([
        count_uniq_char(g.replace(' ', '').replace('\n', '')) for g in groups
    ])


def solve2(inp):
    """Solves part2."""
    pass


"""
Use script args to execute the right function.
"""
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '1':
        res = solve1(Input(DAY).read())
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        res = solve2(Input(DAY).read())
        print(res)
