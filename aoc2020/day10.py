#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input
# import re
# import itertools

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def solve1(data):
    """Solves part 1."""
    adapters = sorted([0] + [int(x) for x in data])
    print(adapters)
    delta1 = 0
    delta3 = 1  # accoutns for the end of the chain which is always 3 jolts diff
    for i in range(0, len(adapters) - 1):
        if abs(adapters[i + 1] - adapters[i]) == 1:
            delta1 += 1
        if abs(adapters[i + 1] - adapters[i]) == 3:
            delta3 += 1
    return delta1, delta3, delta1 * delta3


def solve2(data):
    """Solves part2."""
    for i in data:
        print(i)
    pass


"""
Use script args to execute the right function.
"""
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '1':
        res = solve1((Input(DAY).readlines()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '1t':
        res = solve1((test_input(DAY).readlines()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        res = solve2((Input(DAY).readlines()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '2t':
        res = solve2((test_input(DAY).readlines()))
        print(res)
