#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input
# import re
# import itertools

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def solve1(input):
    """Solves part 1."""
    l = list(input)
    visited = set()
    i = 0
    acc = 0
    while True:
        if i in visited:
            return acc
        visited.add(i)
        op, nb = l[i].split(' ')
        if op == "acc":
            if nb[0] == "+":
                acc += int(nb[1:])
            else:
                acc -= int(nb[1:])
            i += 1
        elif op == "jmp":
            if nb[0] == "+":
                i += int(nb[1:])
            else:
                i -= int(nb[1:])
        elif op == "nop":
            i += 1


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
    if len(sys.argv) > 1 and sys.argv[1] == '1t':
        res = solve1((test_input(DAY).readlines()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        res = solve2((Input(DAY).readlines()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '2t':
        res = solve2((test_input(DAY).readlines()))
        print(res)
