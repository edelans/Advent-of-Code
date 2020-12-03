#!/usr/bin/env python3
"""Template file to be used as boilerplate for each day puzzle."""
from aoc_utilities import Input
import os
# import re
import sys
# import itertools

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


"""
PART1
"""


def solve1(input):
    """Solves part 1."""
    trees_encountered = 0
    # our position in the line
    pos = 0
    for line in input:
        line = line.strip()
        print(line)
        if line[pos] == "#":
            trees_encountered += 1
            path = line[0:pos] + "X" + line[pos+1:]
            print(path)
        else:
            path = line[0:pos] + "O" + line[pos+1:]
            print(path)
        pos = (pos + 3) % len(line) 
    return trees_encountered



"""
PART 2
"""


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
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        res = solve2((Input(DAY).readlines()))
        print(res)
