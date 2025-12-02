#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import logging
import os
import sys

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
    invalid_sum = 0
    for r in data.split(","):
        left, right = int(r.split("-")[0]), int(r.split("-")[1])
        logger.info(f"Checking range: {left} to {right}")
        for id in range(left, right + 1):
            logger.info(f"Checking id: {id}")
            if str(id)[0 : len(str(id)) // 2] == str(id)[len(str(id)) // 2 :]:
                invalid_sum += id
                logger.info(f"Invalid id: {id}")
    return invalid_sum


def chunksize(n: int) -> list[int]:
    cs = set()
    l = len(str(n))
    for i in range(1, l // 2 + 1):
        if l % i == 0:
            cs.add(i)
    return cs


def chunks(s: str, size: int) -> list[str]:
    return [s[i : i + size] for i in range(0, len(s), size)]


def solve2(data):
    """Solves part2."""
    invalid_sum = 0
    for r in data.split(","):
        left, right = int(r.split("-")[0]), int(r.split("-")[1])
        logger.info(f"\nChecking range: {left} to {right}")
        for id in range(left, right + 1):
            logger.info(f"Checking id: {id}")
            cs = chunksize(id)
            logger.info(f"chunksize: {cs}")
            if cs:
                for l in cs:
                    logger.info(
                        f"Checking chunk size: {l}, set of chunks is {set(chunks(str(id), l))}"
                    )
                    if len(set(chunks(str(id), l))) == 1:
                        logger.info(f"❌ Invalid id: {id}")
                        invalid_sum += id
                        break
    return invalid_sum


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
