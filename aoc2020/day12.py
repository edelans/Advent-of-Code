#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from math import e, pi
from aoc_utilities import Input, test_input
# import re
# import itertools

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def parser(data):
    res = [(line[0], int(line[1:])) for line in data]
    return res


def solve1(data):
    """Solves part 1."""
    pos = complex(0, 0)
    dir = complex(1, 0)

    instructions = parser(data)
    for move, value in instructions:
        if move == "N":
            pos += value * 1j
        elif move == "S":
            pos += value * (-1j)
        elif move == "E":
            pos += value * 1
        elif move == "W":
            pos += value * (-1)
        elif move == "L":
            dir *= e**(value * pi / 180 * 1j)
        elif move == "R":
            dir *= e**(-1 * value * pi / 180 * 1j)
        elif move == "F":
            pos += value * dir
        # print("moved with dir {} and value {}, arrived at position {}".format(move, value, pos))
    return abs(pos.imag) + abs(pos.real)


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
