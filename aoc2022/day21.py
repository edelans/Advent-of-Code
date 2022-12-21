#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
import logging
from aoc_utilities import Input, test_input, OPS

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
MONKEYS = {}


def load(data):
    global MONKEYS
    for line in data.splitlines():
        line = line.split()
        if len(line) < 3:
            MONKEYS[line[0][0:4]] = {"result": int(line[1])}
        else:
            MONKEYS[line[0][0:4]] = {
                "a": line[1],
                "op": OPS[line[2]],
                "b": line[3],
            }
    return


def monkey_number(monkey_name):
    global MONKEYS
    if "result" in MONKEYS[monkey_name].keys():
        return MONKEYS[monkey_name]["result"]
    else:
        res = MONKEYS[monkey_name]["op"](
            monkey_number(MONKEYS[monkey_name]["a"]),
            monkey_number(MONKEYS[monkey_name]["b"]),
        )
        MONKEYS[monkey_name]["result"] = res
        return res


def solve1(data):
    """Solves part 1."""
    load(data)
    return monkey_number("root")


def solve2(data):
    """Solves part2."""
    global MONKEYS
    load(data)
    MONKEYS[monkey_name]["humn"] = 0
    FRESH_MONKEYS = MONKEYS.copy()
    print(
        f"MONKEYS['root']['a'] is {MONKEYS['root']['a']}, with value {monkey_number(MONKEYS['root']['a'])}"
    )
    while monkey_number(MONKEYS["root"]["a"]) != monkey_number(MONKEYS["root"]["b"]):
        print("test")
        new_humn = MONKEYS[monkey_name]["humn"] + 1
        MONKEYS = FRESH_MONKEYS.copy()
        MONKEYS[monkey_name]["humn"] = new_humn

    return MONKEYS[monkey_name]["humn"]


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
