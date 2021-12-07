#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
import statistics
from functools import lru_cache


from aoc_utilities import Input, test_input

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def solve1(data):
    """Solves part 1."""
    positions = [int(x) for x in data.split(",")]
    bestpos = statistics.median(positions)
    fuel = 0
    for x in positions:
        fuel += abs(x - bestpos)
    return fuel

@lru_cache(maxsize=None)
def exponentialFuel(origin, target):
    distance = abs(origin - target)
    return (distance + 1) * distance / 2


def totalFuel(origins, target):
    return sum([exponentialFuel(x, target) for x in origins])


def solve2(data):
    """Solves part2."""
    positions = [int(x) for x in data.split(",")]
    positions_to_test = list(range(min(positions), max(positions)+1))

    bestpos = positions_to_test[0]
    bestfuel = totalFuel(positions, bestpos)

    for x in positions_to_test[1:]:
        fuel = totalFuel(positions, x)
        if fuel < bestfuel:
            bestfuel = fuel

    return bestfuel


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
