#!/usr/bin/env python3
"""Template file to be used as boilerplate for each day puzzle."""
from aoc_utilities import Input
import aocd
from copy import deepcopy
import os
import re
import sys
# import itertools

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


"""
PART1
"""

def position_increment(point):
    return (point[0] + point[2], point[1] + point[3], point[2], point[3])


def display_points(points):
    xmin = min(p[0] for p in points)
    xmax = max(p[0] for p in points)
    ymin = min(p[1] for p in points)
    ymax = max(p[1] for p in points)

    # mapping[x][y]
    mapping = [[' '] * (xmax - xmin + 1) for j in range((ymax - ymin + 1))]

    for (x, y, vx, vy) in points:
        mapping[y - ymin][x - xmin] = '#'

    for row in mapping:
        print(''.join(row))

def solve1(input):
    """Solves part 1."""
    # position=< 11153,  22033> velocity=<-1, -2>
    points = [[int(i) for i in re.findall(r'-?\d+', l)] for l in input]
    t = 0
    ys = set(v[1] for v in points)
    print("there are {} different ys and {} differnt points".format(len(ys), len(points)))
    min_y = (0, len(ys), points)  # (t, )
    for t in range(1, 20000):
        for k in range(len(points)):
            points[k] = position_increment(points[k])
        ys = set(v[1] for v in points)
        if len(ys) < 20:
            print("new minimum y at t={}. From {} ys to {}".format(t, min_y[1], len(ys)))
            # min_points = points
            min_y = (t, len(ys), deepcopy(points))
    display_points(min_y[2])
    return None


"""
PART 2
"""


def solve2(input):
    """Solves part2."""
    pass


"""
Use script args to execute the right function.
"""
if __name__ == '__main__':
    if len(sys.argv)>1 and sys.argv[1] == '1':
        res = solve1((Input(DAY).readlines()))
        print(res)
        if len(sys.argv) == 3:
            if sys.argv[2] == 's':
                print("attempting to submit the response '{}' to part 1: \n\n".format(res))
                aocd.submit1(res)

    if len(sys.argv)>1 and sys.argv[1] == '2':
        res = solve2((Input(DAY).readlines()))
        print(res)
        if len(sys.argv) == 3:
            if sys.argv[2] == 's':
                print("attempting to submit the response '{}' to part 2: \n\n".format(res))
                aocd.submit2(res)
