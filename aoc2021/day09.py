#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input, neighbors_4

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]

def parser(data):
    map = {}
    for i,line in enumerate(data.splitlines()):
        for j,point in enumerate(line):
            map[(i,j)] = int(point)
    return map


def solve1(data):
    """Solves part 1."""
    map = parser(data)
    low_points = []
    for point in map:
        lower_neighbor_exists = False
        for neighbor in neighbors_4(point):
            if neighbor in map:
                if map[neighbor] <= map[point]:
                    lower_neighbor_exists = True
        if not lower_neighbor_exists:
            low_points.append(point)
    print(low_points)

    return sum([x + 1 for x in [map[y] for y in low_points] ])


def take_length(elem):
    return len(elem)


def solve2(data):
    """Solves part2."""
    map = parser(data)
    low_points = []
    for point in map:
        lower_neighbor_exists = False
        for neighbor in neighbors_4(point):
            if neighbor in map:
                if map[neighbor] <= map[point]:
                    lower_neighbor_exists = True
        if not lower_neighbor_exists:
            low_points.append(point)

    basins = []
    for low_point in low_points:
        basin = set([low_point])
        new_points_to_check = set([x for x in neighbors_4(low_point) if (x in map and map[x] != 9 and x not in basin)])
        while len(new_points_to_check) > 0:
            for point_to_check in list(new_points_to_check):
                if point_to_check in basin:
                    new_points_to_check.remove(point_to_check)
                else:
                    basin.add(point_to_check)
                    new_points_to_check.update([x for x in neighbors_4(point_to_check) if (x in map and map[x] != 9 and x not in basin)])
        basins.append(basin)
    sorted_basins = sorted(basins, key=take_length, reverse=True)
    return len(sorted_basins[0]) * len(sorted_basins[1]) * len(sorted_basins[2])

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
