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

def trees_with_slope(matrix, slope):
    """
    matrix is an array of lines
    slope is (right, down) : parameters defining the slope
    """
    pos = (0,0)
    trees = 0
    while pos[1]<len(matrix):
        line = matrix[pos[1]].strip()
        print(line)
        if line[pos[0]] == "#":
            trees += 1
        pos = ((pos[0] + slope[0]) % len(line) , pos[1] + slope[1])
    return trees




def solve2(input):
    return trees_with_slope(input, (1,1)) * trees_with_slope(input, (3,1)) * trees_with_slope(input, (5,1)) * trees_with_slope(input, (7,1)) * trees_with_slope(input, (1,2)) 



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
