#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
import logging
import math
from aoc_utilities import Input, test_input, neighbors_4

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

file_handler = logging.FileHandler("day" + DAY + ".log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


CURRENT_MIN = 10000
CACHE = set()


def parser(data):
    up, down, left, right = set(), set(), set(), set()
    lines = data.splitlines()
    max_y = len(lines) - 2
    max_x = len(lines[0]) - 2
    for y, line in enumerate(lines):
        # careful : y increases as you move down the map
        for x, c in enumerate([i for i in line]):
            if c == "^":
                up.add((x, y))
            elif c == ">":
                right.add((x, y))
            elif c == "v":
                down.add((x, y))
            elif c == "<":
                left.add((x, y))
            elif y == 0 and c == ".":
                start = (x, y)
            elif y == len(lines) - 1 and c == ".":
                end = (x, y)

    return start, end, max_x, max_y, up, down, left, right


def dump(max_x, max_y, up, down, left, right, pos):
    xmin = 1
    xmax = max_x
    ymin = 1
    ymax = max_y
    dump = ""
    for y in range(ymin, ymax + 1, 1):
        dump += "  "
        for x in range(xmin, xmax + 1):
            count = sum([(x, y) in s for s in [up, down, left, right]])
            if (x, y) == pos:
                dump += "E"
            elif count > 1:
                dump += str(count)
            elif count == 0:
                dump += "."
            elif (x, y) in up:
                dump += "^"
            elif (x, y) in down:
                dump += "v"
            elif (x, y) in left:
                dump += "<"
            elif (x, y) in right:
                dump += ">"
        dump += "\n"
    return dump


def next_blizzards(max_x, max_y, up, down, left, right):
    new_up, new_down, new_left, new_right = set(), set(), set(), set()
    for (i, j) in up:
        new_up.add((i, j - 1)) if j - 1 >= 1 else new_up.add((i, max_y))
    for (i, j) in down:
        new_down.add((i, j + 1)) if j + 1 <= max_y else new_down.add((i, 1))
    for (i, j) in left:
        new_left.add((i - 1, j)) if i - 1 >= 1 else new_left.add((max_x, j))
    for (i, j) in right:
        new_right.add((i + 1, j)) if i + 1 <= max_x else new_right.add((1, j))
    return new_up, new_down, new_left, new_right


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def iterate(minutes, pos, up, down, left, right, end, max_x, max_y):
    global CURRENT_MIN
    global CACHE
    logger.info(f"after minute {minutes}, E is at pos {pos}")
    if pos == end:
        logger.warning(f"  we found a path in {minutes+1}min!")
        if minutes < CURRENT_MIN:
            CURRENT_MIN = minutes
        up, down, left, right = next_blizzards(max_x, max_y, up, down, left, right)
        return minutes + 1, up, down, left, right

    if minutes + manhattan(pos, end) >= CURRENT_MIN:
        logger.info(
            "  This path will take longer than our current solution, let's kill it"
        )
        return float("inf"), up, down, left, right

    key = (
        pos,
        tuple(sorted(list(up))),
        tuple(sorted(list(down))),
        tuple(sorted(list(right))),
        tuple(sorted(list(left))),
    )
    if key in CACHE:
        # we are in a circle
        logger.info(f"  we found a circle!")
        return float("inf"), up, down, left, right
    else:
        logger.debug(f"  add new key to cache at minute {minutes}: {key}")
        CACHE.add(key)

    minutes += 1

    # logger.debug(dump(max_x, max_y, up, down, left, right, pos))

    up, down, left, right = next_blizzards(max_x, max_y, up, down, left, right)
    all_blizzards = up.union(down, left, right)

    options = []

    for n in neighbors_4(pos):

        if 1 <= n[0] <= max_x and 1 <= n[1] <= max_y:
            if n not in all_blizzards:
                logger.info(f"  E can move from {pos} to {n}")
                options.append((minutes, n, up, down, left, right, end, max_x, max_y))

    # add wait option
    if pos not in all_blizzards:
        logger.info(f"  E can stay at {pos}")
        options.append((minutes, pos, up, down, left, right, end, max_x, max_y))

    # add simple heuristic to investigate first the path that minimize the distance to the end
    options = sorted(options, key=lambda x: manhattan(x[1], x[6]))

    if len(options) > 0:
        return min([iterate(*option) for option in options], key=lambda x: x[0])
    else:
        # this is a dead end
        logger.info(
            f"  dead end: there is no options for position {pos} at minute {minutes}"
        )
        return float("inf"), up, down, left, right


def solve1(data):
    """Solves part 1."""
    start, end, max_x, max_y, up, down, left, right = parser(data)
    up, down, left, right = next_blizzards(max_x, max_y, up, down, left, right)
    return iterate(
        1,
        (start[0], start[1] + 1),
        up,
        down,
        left,
        right,
        (end[0], end[1] - 1),
        max_x,
        max_y,
    )[0]


def solve2(data):
    """Solves part2."""
    start, end, max_x, max_y, up, down, left, right = parser(data)
    global CACHE, CURRENT_MIN

    up, down, left, right = next_blizzards(max_x, max_y, up, down, left, right)

    min1, up, down, left, right = iterate(
        1,
        (start[0], start[1] + 1),
        up,
        down,
        left,
        right,
        (end[0], end[1] - 1),
        max_x,
        max_y,
    )
    logger.warning(f"part 1 took {min1}")
    print(dump(max_x, max_y, up, down, left, right, end))

    # TODO : assumption that I can do the first move right at the first minute is not good. Sometimes I need to wait in initial position (on the edge)...

    up, down, left, right = next_blizzards(max_x, max_y, up, down, left, right)
    print(dump(max_x, max_y, up, down, left, right, (end[0], end[1] - 1)))
    CACHE = set()
    CURRENT_MIN = float("inf")
    min2, up, down, left, right = iterate(
        1,
        (end[0], end[1] - 1),
        up,
        down,
        left,
        right,
        (start[0], start[1] + 1),
        max_x,
        max_y,
    )
    logger.warning(f"part 2 took {min2}")

    up, down, left, right = next_blizzards(max_x, max_y, up, down, left, right)
    CACHE = set()
    CURRENT_MIN = float("inf")
    min3, up, down, left, right = iterate(
        1,
        (start[0], start[1] + 1),
        up,
        down,
        left,
        right,
        (end[0], end[1] - 1),
        max_x,
        max_y,
    )
    logger.warning(f"part 3 took {min3}")

    return min1 + min2 + min3


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
        logger.setLevel(logging.WARNING)
        res = solve2((test_input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        logger.setLevel(logging.WARNING)
        res = solve2((Input(DAY).read()))
        print(res)
