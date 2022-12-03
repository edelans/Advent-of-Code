#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]

PRIORITIES = "0abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def solve1(data):
    """Solves part 1."""
    prio_sum = 0
    for line in data.splitlines():
        comp1 = set(line[:len(line)//2])
        comp2 = set(line[len(line)//2:])
        common_item = comp1.intersection(comp2)
        prio_sum += PRIORITIES.index(common_item.pop())

    return prio_sum


def solve2(data):
    """Solves part2."""
    prio_sum = 0
    lines = data.splitlines()
    for n in range(0, len(lines)//3):
        sac1 = set(lines[3*n+0])
        sac2 = set(lines[3*n+1])
        sac3 = set(lines[3*n+2])
        common_item = sac1 & sac2 & sac3
        prio_sum += PRIORITIES.index(common_item.pop())

    return prio_sum


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
