#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
import re
from aoc_utilities import Input, test_input

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]

def parser1(data):
    """
    takes in input

    0,9 -> 5,9
    8,0 -> 0,8
    ...

    returns a list of tuple of tuples : [ ((0,9),(5,9)), ((8,0),(0,8)), ...   ]
    """
    horizontals = []
    verticals = []

    lines = data.splitlines()
    for line in lines:
        x1,y1,x2,y2 = [int(x) for x in re.findall(r'\d+', line)]
        if (x1 == x2):
            verticals.append(((x1,y1),(x2,y2))) if y1<=y2 else verticals.append(((x2,y2),(x1,y1)))
        if (y1 == y2):
            horizontals.append(((x1, y1), (x2, y2))) if x1<=x2 else horizontals.append(((x2, y2), (x1, y1)))

    print(f"{len(horizontals)} horizontals are {horizontals}")
    print(f"{len(verticals)} verticals are {verticals}")

    return horizontals, verticals


def solve1(data):
    """Solves part 1."""
    horizontals, verticals = parser1(data)
    vents = {}

    for ((x1, y1), (x2, y2)) in horizontals:
        for x in range(x1,x2+1):
            vents[(x,y1)] = vents.get((x,y1), 0) + 1

    for ((x1, y1), (x2, y2)) in verticals:
        for y in range(y1,y2+1):
            vents[(x1,y)] = vents.get((x1,y), 0) + 1

    return sum([1 for x in vents if vents[x]>=2])


def parser2(data):
    """
    takes in input

    0,9 -> 5,9
    8,0 -> 0,8
    ...

    returns a list of tuple of tuples : [ ((0,9),(5,9)), ((8,0),(0,8)), ...   ]
    including diagonals
    """
    horizontals = []
    verticals = []
    diagonals = []

    lines = data.splitlines()
    for line in lines:
        x1,y1,x2,y2 = [int(x) for x in re.findall(r'\d+', line)]
        if (x1 == x2):
            verticals.append(((x1,y1),(x2,y2))) if y1<=y2 else verticals.append(((x2,y2),(x1,y1)))
        elif (y1 == y2):
            horizontals.append(((x1, y1), (x2, y2))) if x1<=x2 else horizontals.append(((x2, y2), (x1, y1)))
        else:
            diagonals.append(((x1, y1), (x2, y2))) if x1<=x2 else diagonals.append(((x2, y2), (x1, y1)))


    return horizontals, verticals, diagonals

def solve2(data):
    """Solves part2."""
    horizontals, verticals, diagonals = parser2(data)
    vents = {}

    for ((x1, y1), (x2, y2)) in horizontals:
        for x in range(x1,x2+1):
            vents[(x,y1)] = vents.get((x,y1), 0) + 1

    for ((x1, y1), (x2, y2)) in verticals:
        for y in range(y1,y2+1):
            vents[(x1,y)] = vents.get((x1,y), 0) + 1

    print(diagonals)
    for ((x1, y1), (x2, y2)) in diagonals:
        xmin = min(x1, x2)
        xmax = max(x1, x2)
        ymin = min(y1, y2)
        ymax = max(y1, y2)
        if (x1<x2 and y1<y2) or (x1>x2 and y2>y1):
            # diagonal down
            print(f"diag down with {((x1, y1), (x2, y2))}")
            for i in range(xmax + 1 - xmin):
                vents[(xmin+i, ymin+i)] = vents.get((xmin+i, ymin+i), 0) + 1
        else:
            # diagonal up
            print(f"diag up with {((x1, y1), (x2, y2))}")
            for i in range(xmax + 1 - xmin):
                vents[(xmin+i, ymax-i)] = vents.get((xmin+i, ymax-i), 0) + 1

    print(vents)
    return sum([1 for x in vents if vents[x]>=2])


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
