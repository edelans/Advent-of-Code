#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input
# import re
# import itertools

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def count_uniq_char(st):
    """count uniq characters in string"""
    return len(set(st))


def solve1(inp):
    """solve part 1"""
    groups = inp.split("\n\n")
    return sum([
        count_uniq_char(g.replace(' ', '').replace('\n', '')) for g in groups
    ])


def count_unanimous_answer(g):
    """Count unanimous answers in a group of answers"""
    chars = set(g.replace('\n', ''))
    ppl = g.splitlines()
    unanimous = 0
    for c in chars:
        if all([c in p for p in ppl]):
            unanimous += 1
    return unanimous


def solve2(inp):
    """Solves part2."""
    groups = inp.split("\n\n")
    return sum(count_unanimous_answer(g) for g in groups)


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
