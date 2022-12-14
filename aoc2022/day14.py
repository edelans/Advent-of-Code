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


def mprint(m):
    """
    Helper function to print a map
    when the map is a dictionary, with keys as tuples of coordinates (1,2)
    no need to have all the coordinates in the keys
    """
    xmin = min([int(i) for (i, j) in m.keys()])
    xmax = max([int(i) for (i, j) in m.keys()])
    ymin = min([int(j) for (i, j) in m.keys()])
    ymax = max([int(j) for (i, j) in m.keys()])
    for y in range(ymin, ymax + 1, 1):
        print("".join([str(m.get((x, y), ".")) for x in range(xmin, xmax + 1)]))
    return


def parser(data):
    """returns the map"""
    m = {}  # coordinates map

    for l in data.splitlines():
        l = l.split(" -> ")
        for i in range(1, len(l)):
            fromx, fromy = map(int, l[i - 1].split(","))
            tox, toy = map(int, l[i].split(","))
            if fromx == tox:
                # vertical line
                (fromy, toy) = (fromy, toy) if fromy < toy else (toy, fromy)
                for y in range(fromy, toy + 1):
                    m[(fromx, y)] = "#"
            elif fromy == toy:
                # horizontal line
                (fromx, tox) = (fromx, tox) if fromx < tox else (tox, fromx)
                for x in range(fromx, tox + 1):
                    m[(x, fromy)] = "#"
    return m


def simulate(source, m):
    """
    source is a tupple of coordinates, where sand originates
    m is a dict mapping the cave
    returns where the sand will stop if it falls from source, or an error if no place to rest
    """
    sx, sy = source
    maxy = max([y for (x, y) in m.keys()])

    while sy < maxy + 1:

        if (sx, sy + 1) not in m.keys():
            logger.info("moving down")
            sy += 1
        elif (sx - 1, sy + 1) not in m.keys():
            logger.info("moving diag left")
            sx -= 1
            sy += 1
        elif (sx + 1, sy + 1) not in m.keys():
            logger.info("moving diag right")
            sx += 1
            sy += 1
        else:
            # can't fall further
            logger.info(f"found a place to rest : {sx},{sy}")
            return (sx, sy)
    logger.info("Sand can't final a place to rest")
    raise AttributeError("Sand can't final a place to rest")


def solve1(data):
    """Solves part 1."""
    m = parser(data)
    source = (500, 0)
    m[source] = "+"

    units = 0

    while True:
        logger.info(f"\nunit of sand {units + 1}")
        try:
            (sx, sy) = simulate(source, m)
            m[(sx, sy)] = "o"
            units += 1
            # mprint(m)
        except AttributeError:
            logger.info("raised exception")
            break

    return units


def simulate2(source, m, floory):
    """
    source is a tupple of coordinates, where sand originates
    m is a dict mapping the cave
    returns where the sand will stop if it falls from source, or an error if no place to rest
    """
    sx, sy = source
    maxy = max([y for (x, y) in m.keys()])

    while sy < maxy + 1:

        if (sx, sy + 1) not in m.keys():
            logger.info("moving down")
            sy += 1
        elif (sx - 1, sy + 1) not in m.keys():
            logger.info("moving diag left")
            sx -= 1
            sy += 1
        elif (sx + 1, sy + 1) not in m.keys():
            logger.info("moving diag right")
            sx += 1
            sy += 1
        else:
            # can't fall further
            logger.info(f"found a place to rest : {sx},{sy}")
            return (sx, sy)
    logger.info("fall on the floor")
    return (sx, floory - 1)


def solve2(data):
    """Solves part2."""
    m = parser(data)
    source = (500, 0)
    m[source] = "+"
    floory = max([y for (x, y) in m.keys()]) + 2
    units = 0

    while True:
        logger.info(f"\nunit of sand {units + 1}")
        (sx, sy) = simulate2(source, m, floory)
        m[(sx, sy)] = "o"
        units += 1
        # mprint(m)
        if (sx, sy) == source:
            return units

    return units


"""
Use script args to execute the right function solve1 / solve2, with the right logging level (only activated on test inputs)
  - python dayXX.py 1
  - python dayXX.py 1t
  - python dayXX.py 2
  - python dayXX.py 2t 
"""
if __name__ == "__main__":
    """some logger levels : DEBUG, INFO, WARNING, CRITICAL"""
    if len(sys.argv) > 1 and sys.argv[1] == "1":
        logger.setLevel(logging.WARNING)
        res = solve1((Input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "1t":
        logger.setLevel(logging.INFO)
        res = solve1((test_input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        logger.setLevel(logging.WARNING)
        res = solve2((Input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2t":
        logger.setLevel(logging.INFO)
        res = solve2((test_input(DAY).read()))
        print(res)
