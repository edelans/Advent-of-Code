#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]

# global variable for translating directions in complexe vectors
dz = {
    "e": 2 + 0j,
    "se": 1 - 1j,
    "sw": -1 - 1j,
    "w": -2 + 0j,
    "nw": -1 + 1j,
    "ne": 1 + 1j
}


def line_parser(line):
    """parse a line of moves, returns a list of directions"""
    lline = list(line)
    directions = []
    while lline:
        elem = lline.pop(0)
        if elem in ("e", "w"):
            directions.append(elem)
        elif elem in ("s", "n"):
            elem2 = lline.pop(0)
            directions.append(''.join((elem, elem2)))
    return directions


def build_grid(data):
    """return a list of black tiles positions (as complex numbers)"""
    data = data.splitlines()
    blacks = []
    for line in data:
        line = line_parser(line)
        tile = complex(0, 0)
        for direction in line:
            tile += dz[direction]
        blacks.remove(tile) if tile in blacks else blacks.append(tile)
    return blacks


def solve1(data):
    """solves part1"""
    return len(build_grid(data))


def neighbors(tile):
    """return a list of the positions of the 6 hexagons (as complexe numbers)
    adjacent to the cell in input"""
    neighbor = []
    for vector in dz.values():
        neighbor.append(tile + vector)
    return neighbor


def evolve(grid):
    """takes the list of black tiles position on one day
    returns the list of black tiles position the day after"""
    new_grid = set()
    for black in grid:
        count = 0
        for n in neighbors(black):
            if n in grid:
                count += 1
            else:
                # n is a white tile that has at least 1 black neighbor, let's count them all :
                count2 = 0
                for n2 in neighbors(n):
                    if n2 in grid:
                        count2 += 1
                if count2 == 2:
                    new_grid.add(n)
        if count in (1, 2):
            new_grid.add(black)
    return new_grid


def solve2(data):
    """Solves part2."""
    grid = build_grid(data)

    for _ in range(100):
        grid = evolve(grid)

    return len(grid)


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
