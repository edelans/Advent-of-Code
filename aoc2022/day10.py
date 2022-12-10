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


def solve1(data):
    """Solves part 1."""
    cycles = [0]  # cycles[i] equals the value of the register AT THE END of cycle i
    # storing all cycle values uses more memory,
    # but simpler to troubleshout values during/after cycle...
    register = 1

    for line in data.splitlines():
        line = line.split(" ")
        if line[0] == "noop":
            cycles.append(register)
        else:
            cycles.append(register)
            register += int(line[1])
            cycles.append(register)

    interesting_cycles = [20, 60, 100, 140, 180, 220]
    sum_signal_strength = 0
    for c in interesting_cycles:
        logger.info(
            f"during cycle {c}, register X has the value {cycles[c-1]}, signal strength is {c * cycles[c-1]}"
        )
        sum_signal_strength += c * cycles[c - 1]
    return sum_signal_strength


def solve2(data):
    """Solves part2."""
    cycles = [0]  # cycles[i] equals the value of the register AT THE END of cycle i
    # storing all cycle values uses more memory,
    # but simpler to troubleshout values during/after cycle...
    register = 1

    for line in data.splitlines():
        line = line.split(" ")
        if line[0] == "noop":
            cycles.append(register)
        else:
            cycles.append(register)
            register += int(line[1])
            cycles.append(register)

    for i in range(6):
        CRTRowLetter = "#"
        spacedCRTRow = ""
        CRTRow = ""
        for j in range(1, 40):
            cycle = 40 * i + j
            CRTindex = j - 1
            register_index = cycles[cycle - 1]
            if abs(register_index - CRTindex) <= 1:
                CRTRowLetter += "#"
                CRTRow += "#"
            else:
                CRTRowLetter += "."
                CRTRow += "."
            if len(CRTRowLetter) == 5:
                spacedCRTRow += CRTRowLetter + "   "
                CRTRowLetter = ""
            logger.info(
                f"during cycle {cycle}, CRT draws pixel in position {CRTindex}, register is at {register_index}"
            )

            logger.info(CRTRow)
        print(spacedCRTRow)
    return


"""
Use script args to execute the right function solve1 / solve2, with the right logging level (only activated on test inputs)
  - python dayXX.py 1
  - python dayXX.py 1t
  - python dayXX.py 2
  - python dayXX.py 2t 
"""
if __name__ == "__main__":
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
