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

JET_PATTERN = ""
JET_INDEX = 0
CYCLE = 0
YCYCLE = 0

ROCKS = {
    0: {
        "base_coords": [(2, 0), (3, 0), (4, 0), (5, 0)],
        "name": "-",
    },
    1: {
        "base_coords": [(3, 0), (2, 1), (3, 1), (4, 1), (3, 2)],
        "name": "+",
    },
    2: {
        "base_coords": [(2, 0), (3, 0), (4, 0), (4, 1), (4, 2)],
        "name": "_|",
    },
    3: {
        "base_coords": [(2, 0), (2, 1), (2, 2), (2, 3)],
        "name": "|",
    },
    4: {
        "base_coords": [(2, 0), (3, 0), (2, 1), (3, 1)],
        "name": "=",
    },
}

ALL_FIRST_50_LINES = set([(x, y) for x in range(50) for y in range(7)])


def mdump(m):
    """
    Helper function to print a set
    """
    ymin = min([i for (i, j) in m])
    ymax = max([j for (i, j) in m])
    dump = ""
    for y in range(ymax, ymin - 1, -1):
        for x in range(7):
            if (x, y) in m:
                dump += "#"
            else:
                dump += "."
        dump += "\n"
    return dump


def jet_move(rock_coords, next_jet, chamber):
    if next_jet == ">":
        new_rock_coords = [(x + 1, y) for (x, y) in rock_coords]
        for c in new_rock_coords:
            if c in chamber:
                return rock_coords

        if 6 in [x for x, y in rock_coords]:
            return rock_coords

        logger.info("Jet of gas pushes rock right")
        return new_rock_coords

    elif next_jet == "<":

        new_rock_coords = [(x - 1, y) for (x, y) in rock_coords]
        for c in new_rock_coords:
            if c in chamber:
                return rock_coords

        if 0 in [x for x, y in rock_coords]:
            return rock_coords

        logger.info("Jet of gas pushes rock left")
        return new_rock_coords

    return None


def add_rock(i, chamber):
    rock_id = i % 5  # 0 is the horizontal bar ####, 4 is the 2x2 square
    global JET_INDEX, JET_PATTERN, CYCLE, YCYCLE
    """
    Each rock appears so that 
    its left edge is two units away from the left wall 
    and its bottom edge is three units above the highest rock in the room
    """

    skyline = [max([y for (xc, y) in chamber if xc == x]) for x in range(7)]
    # logger.critical(f"skyline different values are  {len(set(skyline))}")

    if i > 0 and len(set(skyline)) == 1:
        logger.critical(f"CYCLE DETECTED for i={i}, y is {skyline[0]}")
        YCYCLE = skyline[0]
        chamber = set([(x, 0) for x in range(7)])
        CYCLE += 1
    logger.info(f"skyline is {skyline}")
    basey = max(skyline) + 4
    rock_coords = [(x, y + basey) for (x, y) in ROCKS[rock_id]["base_coords"]]
    logger.info(f"rocks appears with coords {rock_coords}")

    """
    After a rock appears, it alternates between 
    - being pushed by a jet of hot gas one unit (in the direction indicated by the next symbol in the jet pattern) 
    - and then falling one unit down. 
    If any movement would cause any part of the rock to move into the walls, floor, or a stopped rock, 
      the movement instead does not occur. 
      If a downward movement would have caused a falling rock to move into the floor or an already-fallen rock, 
        the falling rock stops where it is (having landed on something) and a new rock immediately begins falling.
    """
    while True:
        next_jet = JET_PATTERN[JET_INDEX]
        JET_INDEX = JET_INDEX + 1 if JET_INDEX < len(JET_PATTERN) - 1 else 0
        rock_coords = jet_move(rock_coords, next_jet, chamber)
        touch = False
        rock_coords_after_fall = [(x, y - 1) for (x, y) in rock_coords]
        for praf in rock_coords_after_fall:
            # point for rock after fall
            if praf in chamber:
                touch = True
                logger.info(f"rock touches at {praf}")
                break

        if touch:
            logger.debug("Rock comes to rest:")
            break
        else:
            # fall down 1 unit
            rock_coords = [(x, y - 1) for (x, y) in rock_coords]
            logger.debug("Rock falls 1 unit")
            if any([y < 0 for (x, y) in rock_coords]):
                logger.critical(f"oh shit, rock coords are {rock_coords}")
                return
        logger.info(f"rock_coords are {rock_coords}")

    return chamber | set(rock_coords)


def solve1():
    """Solves part 1."""
    chamber = set([(x, 0) for x in range(7)])
    print(chamber)
    for i in range(2022):
        if i % 100 == 0:
            logger.warning(f"reached i = {i}")
            logger.debug(mdump(chamber))

        chamber = add_rock(i, chamber)
        logger.warning(f"chamber has size {len(chamber)}")
        logger.debug(mdump(chamber))
    return max([y for (x, y) in chamber]) + CYCLE * YCYCLE


def solve2(data):
    """Solves part2."""
    global CYCLE, YCYCLE
    chamber = set([(x, 0) for x in range(7)])
    print(chamber)
    print(f"CYCLE is {CYCLE}")
    i = 0
    while CYCLE < 1:
        if i % 100 == 0:
            logger.warning(f"reached i = {i}")
            logger.debug(mdump(chamber))
            logger.warning(f"chamber has size {len(chamber)}")
        chamber = add_rock(i, chamber)
        logger.debug(mdump(chamber))
        i += 1

    cycles_to_res = 1_000_000_000 // YCYCLE
    remaining = 1_000_000_000 % YCYCLE
    for i in range(remaining):
        chamber = add_rock(i, chamber)

    return max([y for (x, y) in chamber]) + cycles_to_res * YCYCLE


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
        logger.setLevel(logging.CRITICAL)
        JET_PATTERN = Input(DAY).read()
        res = solve1()
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "1t":
        logger.setLevel(logging.CRITICAL)
        JET_PATTERN = test_input(DAY).read()
        res = solve1()
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        logger.setLevel(logging.WARNING)
        JET_PATTERN = Input(DAY).read()
        res = solve2((Input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2t":
        logger.setLevel(logging.WARNING)
        JET_PATTERN = test_input(DAY).read()
        res = solve2((test_input(DAY).read()))
        print(res)
