#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
import logging
import re
import operator
import math
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


OPS = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}


def parser(data):
    res = []
    monkeys = data.split("\n\n")
    for monkey_data in monkeys:
        monkey = {}
        monkey_data = monkey_data.splitlines()
        monkey["starting_items"] = [int(x) for x in re.findall(r"\d+", monkey_data[1])]
        operation = monkey_data[2].split(" ")[-2]
        operand = monkey_data[2].split(" ")[-1]
        if operation == "*" and operand == "old":
            monkey["operation"] = {
                "operator": operator.pow,
                "operand": 2,
            }
        else:
            monkey["operation"] = {
                "operator": OPS[operation],
                "operand": int(operand),
            }
        monkey["test_division"] = int(monkey_data[3].split(" ")[-1])
        monkey["true_recipient"] = int(monkey_data[4].split(" ")[-1])
        monkey["false_recipient"] = int(monkey_data[5].split(" ")[-1])
        res.append(monkey)
    return res


def solve1(data):
    """Solves part 1."""
    monkeys = parser(data)
    monkey_inspections = [0] * len(monkeys)

    for _ in range(20):
        for i, monkey in enumerate(monkeys):
            logger.debug(f"Monkey {i}:")
            starting_items = monkey["starting_items"]
            for item in starting_items:
                monkey_inspections[i] += 1
                logger.debug(f"  Monkey inspects an item with a worry level of {item}.")
                item = monkey["operation"]["operator"](
                    item, monkey["operation"]["operand"]
                )
                logger.debug(f"    Worry level increases to {item}.")
                item = item // 3
                logger.debug(f"    Worry level is divided by 3 to {item}.")
                if item % monkey["test_division"] == 0:
                    logger.debug(
                        f"    Current worry level ({item}) is divisible by {monkey['test_division']}."
                    )
                    recipient = monkey["true_recipient"]
                    logger.debug(
                        f"    Item with worry level {item} is thrown to monkey {recipient}."
                    )
                else:
                    logger.debug(
                        f"    Current worry level ({item}) is NOT divisible by {monkey['test_division']}."
                    )
                    recipient = monkey["false_recipient"]
                    logger.debug(
                        f"    Item with worry level {item} is thrown to monkey {recipient}."
                    )
                monkeys[recipient]["starting_items"].append(item)
            monkey["starting_items"] = []
    for i, m in enumerate(monkeys):
        logger.info(f"Monkey {i}: " + str(m["starting_items"]))
    print(monkey_inspections)
    return math.prod(sorted(monkey_inspections, reverse=True)[:2])


def solve2(data):
    """Solves part2."""
    monkeys = parser(data)
    monkey_inspections = [0] * len(monkeys)

    # worry level ("item" in part 1) will increase to level that can't be handled by the program
    # the only important thing we do with item is to check if it's divisible by monkey["test_division"]
    # instead of keeping track of this number, we are only going to keep track of the reminder of its value divided by
    # the value of the product of all monkey["test_division"]. Thus :
    #   - the number will stay low enough to be tracked,
    #   - and its divisibility by each monkey["test_division"] will remain the same

    common_multiple = math.prod([monkey["test_division"] for monkey in monkeys])

    for _ in range(10000):
        for i, monkey in enumerate(monkeys):
            logger.debug(f"Monkey {i}:")
            starting_items = monkey["starting_items"]
            for item in starting_items:
                monkey_inspections[i] += 1
                logger.debug(f"  Monkey inspects an item with a worry level of {item}.")
                item = (
                    monkey["operation"]["operator"](
                        item, monkey["operation"]["operand"]
                    )
                    % common_multiple
                )
                logger.debug(f"    Worry level reminder is now {item}.")

                if item % monkey["test_division"] == 0:
                    logger.debug(
                        f"    Current worry level ({item}) is divisible by {monkey['test_division']}."
                    )
                    recipient = monkey["true_recipient"]
                    logger.debug(
                        f"    Item with worry level {item} is thrown to monkey {recipient}."
                    )
                else:
                    logger.debug(
                        f"    Current worry level ({item}) is NOT divisible by {monkey['test_division']}."
                    )
                    recipient = monkey["false_recipient"]
                    logger.debug(
                        f"    Item with worry level {item} is thrown to monkey {recipient}."
                    )
                monkeys[recipient]["starting_items"].append(item)
            monkey["starting_items"] = []
    for i, m in enumerate(monkeys):
        logger.info(f"Monkey {i}: " + str(m["starting_items"]))
    print(monkey_inspections)
    return math.prod(sorted(monkey_inspections, reverse=True)[:2])


"""
Use script args to execute the right function solve1 / solve2, with the right logging level (only activated on test inputs)
  - python dayXX.py 1
  - python dayXX.py 1t
  - python dayXX.py 2
  - python dayXX.py 2t 
"""
if __name__ == "__main__":
    """sme logger levels : DEBUG, INFO, WARNING, CRITICAL"""
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
