#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input

from functools import reduce
import operator

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def parser(data):
    tiles = {}
    raw_tiles = data.strip().split("\n\n")
    for tile in raw_tiles:
        tile = tile.splitlines()
        tile_id = tile[0].split(' ')[1][:-1]
        tiles[tile_id] = [[char for char in line] for line in tile[1:]]
    return tiles


def borders(tile_content):
    transpose = list(zip(*tile_content))
    # as images can be rotated **or flipped**, we have to consider each border in each direction...
    return [
        tile_content[0], tile_content[0][::-1],
        list(transpose[-1]),
        list(transpose[-1][::-1]), tile_content[-1][::-1], tile_content[-1],
        list(transpose[0][::-1]),
        list(transpose[0])
    ]


def solve1(data):
    """Solves part 1."""
    tiles = parser(data)

    border_count = {}

    for id, content in tiles.items():
        for b in borders(content):
            border_count[str(b)] = border_count.get(str(b), 0) + 1

    # corner tiles are the tiles which sum of border counts is the minimum

    tile_border_count = {}
    for id, content in tiles.items():
        tile_border_count[id] = sum(
            [border_count[str(b)] for b in borders(content)])

    corners = []
    for id in tiles.keys():
        if tile_border_count[id] == min(tile_border_count.values()):
            corners.append(id)

    return reduce(operator.mul, map(int, corners), 1)


def solve2(data):
    """Solves part2."""
    pass


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
