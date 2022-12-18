#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
import logging
from aoc_utilities import Input, test_input

from operator import itemgetter

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
ICYCLE = 0
YCYCLE = 0
YMAX = 0

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

chamber = set([(x, 0) for x in range(7)])


def mdump(m):
    """
    Helper function to print a set
    """
    dump = ""
    for y in range(YMAX, - 1, -1):
        for x in range(7):
            if (x, y) in m:
                dump += "#"
            else:
                dump += "."
        dump += "\n"
    return dump


def mdump_lasty(m, size):
    """
    Helper function to print a set
    """
    dump = ""
    for y in range(YMAX, YMAX - size - 1, -1):
        for x in range(7):
            if (x, y) in m:
                dump += "#"
            else:
                dump += "."
        dump += "\n"
    return dump

def jet_move(rock_coords, next_jet):
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


def add_rock(i):
    rock_id = i % 5  # 0 is the horizontal bar ####, 4 is the 2x2 square
    global JET_INDEX, JET_PATTERN, chamber, YMAX
    """
    Each rock appears so that 
    its left edge is two units away from the left wall 
    and its bottom edge is three units above the highest rock in the room
    """

    basey = YMAX + 4
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
        rock_coords = jet_move(rock_coords, next_jet)
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
            rock_coords = rock_coords_after_fall
            logger.debug("Rock falls 1 unit")
            if any([y < 0 for (x, y) in rock_coords]):
                logger.critical(f"oh shit, rock coords are {rock_coords}")
                return
        logger.info(f"rock_coords are {rock_coords}")
    chamber.update(set(rock_coords))
    ymax_rock = max(map(itemgetter(1), rock_coords))

    # YMAX = max(map(itemgetter(1), chamber)) makes add_rock in O(1) instead of 0(len(chamber)) !!!
    if ymax_rock > YMAX:
        YMAX = ymax_rock
    return


def solve1():
    """Solves part 1."""
    global chamber
    for i in range(2022):
        if i % 1000 == 0:
            logger.warning(f"reached i = {i}")
        add_rock(i)

    return YMAX


def solve2(data):
    """Solves part2."""
    global YMAX
    cycle = False
    previous = {}
    i = 0
    i_target = 1_000_000_000_000
    sample_size = 100

    while i < i_target:
        if i % 100_000 == 0:
            logger.warning(f"reached i = {i}")
        add_rock(i)
        i += 1

        # CYCLE DETECTOR
        if not cycle:
            if i > sample_size and i % (len(JET_PATTERN) * len(ROCKS)) == 0:
                # cycle length is necessarily a multiple of the size of each problem inputs
                dump = mdump_lasty(chamber, sample_size)
                #logger.warning(dump)
                if dump in previous:
                    print("CYCLE DETECTED")
                    cycle = True
                    i_cycle_start = previous[dump][0]
                    y_cycle_start = previous[dump][1]
                    cycle_length = i - i_cycle_start
                    cycle_y_size = YMAX - y_cycle_start

                    n = (i_target - i) // cycle_length
                    print(f"fast forward {n} cycles of length {cycle_length} and height {cycle_y_size}, adding {n * cycle_length} to i and {n * cycle_y_size} to YMAX")
                    i += n * cycle_length
                    y_cycles = n * cycle_y_size
                else:
                    previous[dump] = i, YMAX
    return YMAX + y_cycles

    # 1514286628
    # 1514285716108
    # 1514285714288
    # 1572093023267
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
        logger.setLevel(logging.WARNING)
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
