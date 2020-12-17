#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
import json

from aoc_utilities import Input, test_input
from itertools import product

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def neighbors_26(point):
    """returns a set of (x,y,z) positions for the 26 positions around point """
    x = [point[0] - 1, point[0], point[0] + 1]
    y = [point[1] - 1, point[1], point[1] + 1]
    z = [point[2] - 1, point[2], point[2] + 1]
    return set(product(x, y, z)) - set(point)


def parser(data):
    """returns a 3 dimentional grid as a dict"""
    grid = {}
    z = 0
    for y, line in enumerate(data):
        for x, value in enumerate(line.strip()):
            if value == "#":
                print(
                    f'grid is {grid}, x is {x}, y is {y} and value is {value}')
                grid[x] = grid.get(x, {})
                grid[x][y] = grid[x].get(y, {})
                grid[x][y][z] = "#"
    print(json.dumps(grid, indent=4))
    return grid


def bounds(grid):
    """returns min and max index used in each dimention"""
    xlist = grid.keys()
    ylist = set()
    for v in grid.values():
        ylist.update(set(v.keys()))
    zlist = set()
    for v in grid.values():
        for v2 in v.values():
            zlist.update(set(v2.keys()))
    return ((min(xlist), max(xlist)), (min(ylist), max(ylist)), (min(zlist),
                                                                 max(zlist)))


def solve1(data):
    """Solves part 1."""
    return bounds(parser(data))


def solve2(data):
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
