#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
import logging
from aoc_utilities import Input, test_input, timer_func

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


def toBase10(snafu):

    tot = 0
    decode = {"0": 0, "1": 1, "2": 2, "=": -2, "-": -1}

    for m, c in enumerate(snafu[::-1], 1):
        tot += decode[c] * pow(5, m - 1)

    return tot


def toSnafu(val):
    print(f"converting {val} to SNAFU")

    encode = "012=-"
    rsnafu = ""  # reverse snafu

    while val:
        rsnafu += encode[val % 5]
        val = (val + 2) // 5

    return rsnafu[::-1]


"""
2=-01 

  2 in the 625s place, ->                 (2 times 625)
  = (double-minus) in the 125s place, ->  plus (-2 times 125)
  - (minus) in the 25s place, ->          plus (-1 times 25)
  0 in the 5s place,  ->                  plus (0 times 5)
  1 in the 1s place. ->                   plus (1 times 1)
  
  That's 1250 plus -250 plus -25 plus 0 plus 1. 976!"
"""


@timer_func
def solve1(data):

    tot = 0
    for line in data.splitlines():
        tot += toBase10(line)

    return toSnafu(tot)
    # 32005641587247


def solve2(data):
    """Solves part2."""
    pass


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
