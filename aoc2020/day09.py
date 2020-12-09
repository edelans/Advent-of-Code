#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input
# import re
# import itertools

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def is_valid(preamble, nb):
    for i in range(0, len(preamble) - 1):
        for j in range(i + 1, len(preamble)):
            if preamble[i] + preamble[j] == nb:
                return True
    return False


def solve1(data, size):
    """Solves part 1."""
    data = [int(x) for x in data]
    k = 0
    while True:
        if not is_valid(data[k:k + size], data[k + size]):
            return data[k + size]
        k += 1


def solve2(data, size):
    """Solves part2."""
    target = solve1(data, size)
    data = [int(x) for x in data]
    for i in range(0, len(data)):
        dsum = 0
        subset = []
        for j in range(i, len(data)):
            dsum += data[j]
            subset.append(data[j])
            if len(subset) == 1:
                continue
            if dsum > target:
                break
            if dsum == target:
                return min(subset) + max(subset)


"""
Use script args to execute the right function.
"""
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '1':
        res = solve1((Input(DAY).readlines()), 25)
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '1t':
        res = solve1((test_input(DAY).readlines()), 5)
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        res = solve2((Input(DAY).readlines()), 25)
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '2t':
        res = solve2((test_input(DAY).readlines()), 5)
        print(res)
