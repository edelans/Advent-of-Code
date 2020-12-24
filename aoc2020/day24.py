#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def line_parser(line):
    lline = [x for x in line]
    l = []
    while lline:
        el = lline.pop(0)
        if el == "e" or el == "w":
            l.append(el)
        elif el == "s" or el == "n":
            el2 = lline.pop(0)
            l.append(''.join((el, el2)))
    return l


def solve1(data):
    """Solves part 1."""
    data = data.splitlines()

    blacks = []
    for line in data:
        line = line_parser(line)
        z = complex(0, 0)
        for dir in line:
            if dir == "e":
                z += 2
            elif dir == "se":
                z += 1 - 1j
            elif dir == "sw":
                z += -1 - 1j
            elif dir == "w":
                z += -2
            elif dir == "nw":
                z += -1 + 1j
            elif dir == "ne":
                z += 1 + 1j
        if z in blacks:
            blacks.remove(z)
        else:
            blacks.append(z)
    return len(blacks)


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
