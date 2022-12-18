#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
import logging
from aoc_utilities import Input, test_input

"""
Logger config
  use logger.ingo("") instead of print statement
  those messages will be displayed while running the code on testing sets
  but not displayed while running on real puzzle inputs
  note: when you want to avoid logging, 
  be careful to also skip any expensive computation leading to what you want to log
"""
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def get_all_faces(point):
    (x,y,z) = point
    all_faces = set()
    faces = [
        [(x, y, z), (x, y, z+1), (x, y+1, z), (x, y+1, z+1)],
        [(x+1, y, z), (x+1, y, z+1), (x+1, y+1, z), (x+1, y+1, z+1)],
        [(x, y, z),(x+1, y, z),(x, y, z+1),(x+1, y, z+1)],
        [(x, y+1, z),(x+1, y+1, z),(x, y+1, z+1),(x+1, y+1, z+1)],
        [(x, y, z), (x + 1, y, z), (x, y + 1, z), (x + 1, y + 1, z)],
        [(x, y, z+1), (x + 1, y, z+1), (x, y + 1, z+1), (x + 1, y + 1, z+1)],
    ]
    for f in faces:
        all_faces.add(tuple(sorted(f)))

    return all_faces



def solve1(data):
    """Solves part 1."""
    free_sides = set()
    k=0

    for line in data.splitlines():
        x,y,z = map(int, line.split(","))
        for side in get_all_faces((x,y,z)):
            if side not in free_sides:
                free_sides.add(side)
            else:
                free_sides.remove(side)
    return len(free_sides)





def solve2(data):
    """Solves part2."""
    free_sides = set()
    k=0

    for line in data.splitlines():
        x,y,z = map(int, line.split(","))
        for side in get_all_faces((x,y,z)):
            if side not in free_sides:
                free_sides.add(side)
            else:
                free_sides.remove(side)


    # in those free sides, some are external, some are internal
    # we want to count the external
    # one is external if one of its edges belong to the largest set of connecting edges

    # start from one edge
    result = {}
    while free_sides:
        surface = set()
        side = free_sides.pop()
        surface.add(side)
        edges = set([edge for edge in side])
        intersect = True
        while intersect:
            print(f"free_sides size is {len(free_sides)}")
            fs = free_sides.copy()
            intersect = False
            for s in fs:



                if len(edges & set([si for si in s])) > 0:
                    free_sides.remove(s)
                    edges.update([edge for edge in s])
                    surface.add(s)
                    intersect = True

        result[side] = len(surface)

    return result
    # 4114 too high






"""
Use script args to execute the right function solve1 / solve2, with the right logging level (only activated on test inputs)
  - python dayXX.py 1
  - python dayXX.py 1t
  - python dayXX.py 2
  - python dayXX.py 2t 
"""
if __name__ == "__main__":
    """some logger levels : DEBUG, INFO, WARNING, CRITICAL"""
    if len(sys.argv) > 1 and sys.argv[1] == "1t":
        logger.setLevel(logging.INFO)
        res = solve1((test_input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "1":
        logger.setLevel(logging.WARNING)
        res = solve1((Input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2t":
        logger.setLevel(logging.INFO)
        res = solve2((test_input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        logger.setLevel(logging.WARNING)
        res = solve2((Input(DAY).read()))
        print(res)
