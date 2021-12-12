#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input, neighbors_all

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def parser(data):
    energy_levels = {}
    for row, line in enumerate(data.splitlines()):
        for column, energy_level in enumerate(line):
            energy_levels[(row, column)] = int(energy_level)
    return energy_levels


def evolve(levels):
    flashes = 0

    # part 1
    for k in levels.keys():
        levels[k] += 1

    # part 2
    flashing_points = set([k for k,v in levels.items() if v > 9 ] )
    while len(flashing_points) > 0:
        p = flashing_points.pop()
        for n in neighbors_all(p):
            if n in levels.keys():
                levels[n] += 1

                # add to flashing_points *just* when the energy level go over the threshold
                if levels[n] == 10:
                    flashing_points.add(n)

    # part 3
    for k, v in levels.items():
        if v > 9:
            flashes += 1
            levels[k] = 0

    return levels, flashes


def lprint(levels):
    max_row = max([int(i) for (i,j) in levels.keys()])
    max_col = max([int(j) for (i,j) in levels.keys()])
    for r in range(max_row + 1):
        print(''.join([str(levels[(r,c)]) for c in range(max_col + 1)]))
    return


def solve1(data):
    """Solves part 1."""
    levels = parser(data)
    flashes = 0

    for _ in range(100):
        levels, additional_flashes = evolve(levels)
        flashes += additional_flashes
    lprint(levels)
    return flashes




def solve2(data):
    """Solves part2."""
    levels = parser(data)
    step = 0
    flashes = 0
    levels, additional_flashes = evolve(levels)

    while flashes != 100:
        levels, flashes = evolve(levels)
        step += 1

    return step + 1


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
