#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import logging
import os
import sys
from collections import deque

from aoc_utilities import Input, test_input

"""
Logger config
  use logger.info("") instead of print statement
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


def solve1(data):
    """Solves part 1."""
    circle = deque(range(0, 100))
    circle.rotate(-50)  # rotate to put 50 at the beginning of the circle
    logger.info(f"The dial points at {circle[0]}.")
    counter = 0
    for line in data.splitlines():
        (d, nb) = (line[0], int(line[1:]))
        logger.info(f"The dial points at {circle[0]}. Will rotate to the {d} by {nb}")
        if d == "R":
            circle.rotate(-nb)
        if d == "L":
            circle.rotate(+nb)
        if circle[0] == 0:
            counter += 1
    logger.info(
        f"The dial points at {circle[0]}. We have seen {counter} times the number 0."
    )
    return counter


def solve2(data):
    """Solves part2."""
    circle = deque(range(0, 100))
    circle.rotate(-50)  # rotate to put 50 at the beginning of the circle
    logger.info(f"The dial points at {circle[0]}.")
    counter = 0
    for line in data.splitlines():
        (d, nb) = (line[0], int(line[1:]))
        logger.info(f"The dial points at {circle[0]}. Will rotate to the {d} by {nb}")
        for i in range(nb):
            if d == "R":
                circle.rotate(-1)
            if d == "L":
                circle.rotate(+1)
            if circle[0] == 0:
                counter += 1
                logger.info("We have seen the number 0!")
    logger.info(
        f"The dial points at {circle[0]}. We have seen {counter} times the number 0."
    )
    return counter


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
        res = solve1(test_input(DAY).read())
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "1":
        logger.setLevel(logging.WARNING)
        res = solve1(Input(DAY).read())
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2t":
        logger.setLevel(logging.INFO)
        res = solve2(test_input(DAY).read())
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        logger.setLevel(logging.WARNING)
        res = solve2(Input(DAY).read())
        print(res)
