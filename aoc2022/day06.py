#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def solve1(data):
    """Solves part 1."""
    for i in range(len(data)):
        if len(set(data[i : i + 4])) == 4:
            return i + 4
    return "no start-of-packet detected"


def solve2(data):
    """Solves part2."""
    for i in range(len(data)):
        if len(set(data[i : i + 14])) == 14:
            return i + 14
    return "no start-of-packet detected"


"""
Use script args to execute the right function.
"""
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "1":
        res = solve1((Input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "1t":
        res = solve1((test_input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        res = solve2((Input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2t":
        res = solve2((test_input(DAY).read()))
        print(res)
