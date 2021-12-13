#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def parser(data):
    """Solves part 1."""
    coords, fold_instructions = data.split("\n\n")
    maping = {}
    for coord in coords.splitlines():
        maping[ (int(coord.split(',')[0]), int(coord.split(',')[1])) ] = 1
    fold_instructions = [x.split(" ")[2] for x in fold_instructions.splitlines()]
    return maping, fold_instructions



def mprint(maping):
    xmax = max([int(i) for (i,j) in maping.keys()])
    ymax = max([int(j) for (i,j) in maping.keys()])
    for y in range(ymax + 1):
        print(''.join([str(maping.get((x,y),".")) for x in range(xmax + 1)]))
    return

def solve1(data):
    """Solves part 1."""
    coords, fold_instructions = parser(data)
    mprint(coords)
    print()

    for f in fold_instructions[:1]:
        new_coords = {}
        fold_line = int(f[2:])
        if f[0] == 'x':
            for coord in coords.keys():
                if coord[0]<fold_line:
                    new_coords[coord] = 1
                if coord[0]>fold_line:
                    new_x = fold_line - (coord[0] - fold_line)
                    new_coords[(new_x, coord[1])] = 1


        if f[0] == 'y':
            for coord in coords.keys():
                if coord[1]<fold_line:
                    new_coords[coord] = 1
                if coord[1]>fold_line:
                    new_y = fold_line - (coord[1] - fold_line)
                    new_coords[(coord[0],new_y)] = 1


    mprint(new_coords)
    return sum([v for v in new_coords.values()])



def solve2(data):
    """Solves part2."""
    coords, fold_instructions = parser(data)
    mprint(coords)
    print()

    for f in fold_instructions:
        new_coords = {}
        fold_line = int(f[2:])
        if f[0] == 'x':
            print(f"folding on {f}")
            for coord in coords.keys():
                if coord[0]<fold_line:
                    new_coords[coord] = 1
                if coord[0]>fold_line:
                    new_x = fold_line - (coord[0] - fold_line)
                    new_coords[(new_x, coord[1])] = 1


        if f[0] == 'y':
            print(f"folding on {f}")
            for coord in coords.keys():
                if coord[1]<fold_line:
                    new_coords[coord] = 1
                if coord[1]>fold_line:
                    new_y = fold_line - (coord[1] - fold_line)
                    new_coords[(coord[0],new_y)] = 1

        coords = new_coords

        mprint(new_coords)
        print()

    return


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
