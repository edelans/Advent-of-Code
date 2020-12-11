#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input, neighbors_8
# import re
# import itertools

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def parser(data):
    grid = []
    for line in data:
        grid.append([x for x in line])
    return grid


def gprint(grid):
    for line in grid:
        print(''.join(line))
    return None


def adjacent_seats_values(grid, pos):
    values = []
    for s in neighbors_8(pos):
        if s[0] >= 0 and s[0] < len(
                grid[0]) and s[1] >= 0 and s[1] < len(grid):
            # s is a valid position in the grid
            values.append(grid[s[1]][s[0]])
    return values


def round(grid):
    new_grid = []
    for y, line in enumerate(grid):
        new_line = []
        for x, value in enumerate(line):
            adj_seats_vals = adjacent_seats_values(grid, (x, y))
            if value == 'L':
                if "#" not in adj_seats_vals:
                    new_line.append("#")
                else:
                    new_line.append("L")
            elif value == "#":
                if adj_seats_vals.count("#") >= 4:
                    new_line.append("L")
                else:
                    new_line.append("#")
            elif value == ".":
                new_line.append(".")
        new_grid.append(new_line)
    return new_grid


def solve1(data):
    """Solves part 1."""
    grid = parser(data)
    while grid != round(grid):
        grid = round(grid)
    return [val for line in grid for val in line].count("#")


def is_in_grid(s, grid):
    return s[0] >= 0 and s[0] < len(grid[0]) and s[1] >= 0 and s[1] < len(grid)


def gval(s, grid):
    return grid[s[1]][s[0]]


def adjacent_seats_values2(grid, pos):
    """"returns the values of the first seat pos can see in each of eight directions"""
    values = []

    # up
    s = pos
    while is_in_grid((s[0], s[1] + 1), grid) and grid[s[1] + 1][s[0]] == ".":
        s = (s[0], s[1] + 1)
    adj = (s[0], s[1] + 1)
    if is_in_grid(adj, grid):
        values.append(gval(adj, grid))

    # down
    s = pos
    while is_in_grid((s[0], s[1] - 1), grid) and grid[s[1] - 1][s[0]] == ".":
        s = (s[0], s[1] - 1)
    adj = (s[0], s[1] - 1)
    if is_in_grid(adj, grid):
        values.append(gval(adj, grid))

    # left
    s = pos
    while is_in_grid((s[0] - 1, s[1]), grid) and grid[s[1]][s[0] - 1] == ".":
        s = (s[0] - 1, s[1])
    adj = (s[0] - 1, s[1])
    if is_in_grid(adj, grid):
        values.append(gval(adj, grid))

    # right
    s = pos
    while is_in_grid((s[0] + 1, s[1]), grid) and grid[s[1]][s[0] + 1] == ".":
        s = (s[0] + 1, s[1])
    adj = (s[0] + 1, s[1])
    if is_in_grid(adj, grid):
        values.append(gval(adj, grid))

    # up-left
    s = pos
    while is_in_grid(
        (s[0] - 1, s[1] + 1), grid) and grid[s[1] + 1][s[0] - 1] == ".":
        s = (s[0] - 1, s[1] + 1)
    adj = (s[0] - 1, s[1] + 1)
    if is_in_grid(adj, grid):
        values.append(gval(adj, grid))

    # up-right
    s = pos
    while is_in_grid(
        (s[0] + 1, s[1] + 1), grid) and grid[s[1] + 1][s[0] + 1] == ".":
        s = (s[0] + 1, s[1] + 1)
    adj = (s[0] + 1, s[1] + 1)
    if is_in_grid(adj, grid):
        values.append(gval(adj, grid))

    # down-left
    s = pos
    while is_in_grid(
        (s[0] - 1, s[1] - 1), grid) and grid[s[1] - 1][s[0] - 1] == ".":
        s = (s[0] - 1, s[1] - 1)
    adj = (s[0] - 1, s[1] - 1)
    if is_in_grid(adj, grid):
        values.append(gval(adj, grid))

    # up-right
    s = pos
    while is_in_grid(
        (s[0] + 1, s[1] - 1), grid) and grid[s[1] - 1][s[0] + 1] == ".":
        s = (s[0] + 1, s[1] - 1)
    adj = (s[0] + 1, s[1] - 1)
    if is_in_grid(adj, grid):
        values.append(gval(adj, grid))

    return values


def round2(grid):
    new_grid = []
    for y, line in enumerate(grid):
        new_line = []
        for x, value in enumerate(line):
            adj_seats_vals = adjacent_seats_values2(grid, (x, y))
            if value == 'L':
                if "#" not in adj_seats_vals:
                    new_line.append("#")
                else:
                    new_line.append("L")
            elif value == "#":
                if adj_seats_vals.count("#") >= 5:
                    new_line.append("L")
                else:
                    new_line.append("#")
            elif value == ".":
                new_line.append(".")
        new_grid.append(new_line)
    return new_grid


def solve2(data):
    """Solves part2."""
    grid = parser(data)
    while grid != round2(grid):
        grid = round2(grid)
    return [val for line in grid for val in line].count("#")


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
