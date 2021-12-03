#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def bitsToInt(listOfBits):
    return int("".join(str(x) for x in listOfBits), 2)

def solve1(data):
    """Solves part 1."""
    lines = [list(line) for line in data.splitlines()]
    columns = [*zip(*lines)]

    gammaBits = []
    epsilonBits = []
    minimumToBeMostCommon = int(len(lines) / 2)

    for col in columns:
        if col.count("1") > minimumToBeMostCommon:
            gammaBits.append("1")
            epsilonBits.append("0")
        else:
            gammaBits.append("0")
            epsilonBits.append("1")

    return bitsToInt(gammaBits) * bitsToInt(epsilonBits)

def solve2(data):
    """Solves part2."""
    pass


"""
Use script args to execute the right function.
"""
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '1':
        res = solve1((Input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '1t':
        res = solve1((test_input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        res = solve2((Input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '2t':
        res = solve2((test_input(DAY).read()))
        print(res)
