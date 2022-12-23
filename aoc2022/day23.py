#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
import logging
from aoc_utilities import Input, test_input, neighbors_all

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


def parser(data):
    ground = set()
    y = 0
    for line in data.splitlines():
        for x, c in enumerate([i for i in line]):
            if c == "#":
                ground.add((x, y))
        y -= 1
    return ground


def delta_dir(d):
    """returns dx,dy according to direction"""
    if d == "N":
        return 0, +1
    if d == "S":
        return 0, -1
    if d == "E":
        return 1, 0
    if d == "W":
        return -1, 0


def move_check(x, y, d):
    if d == "N":
        return (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)
    if d == "S":
        return (x - 1, y - 1), (x, y - 1), (x + 1, y - 1)
    if d == "E":
        return (x + 1, y + 1), (x + 1, y), (x + 1, y - 1)
    if d == "W":
        return (x - 1, y + 1), (x - 1, y), (x - 1, y - 1)


def mdump(ground):
    """
    Helper function to print a map
    when the map is a set,
    """
    xmin = min([int(i) for (i, j) in ground])
    xmax = max([int(i) for (i, j) in ground])
    ymin = min([int(j) for (i, j) in ground])
    ymax = max([int(j) for (i, j) in ground])
    dump = ""
    for y in range(ymax, ymin - 1, -1):
        for x in range(xmin, xmax + 1):
            if (x, y) in ground:
                dump += "#"
            else:
                dump += "."
        dump += "\n"
    return dump


def solve1(data):
    """Solves part 1."""
    ground = parser(data)
    directions = ["N", "S", "W", "E"]
    d = 0

    print("initial state: ")
    print(mdump(ground))
    print()

    # first half
    # each Elf considers the eight positions adjacent to themself.
    #   - If no other Elves are in one of those eight positions, the Elf does not do anything during this round
    #   - Otherwise, the Elf looks in each of four directions in the following order and proposes moving one step in the first valid direction:

    for r in range(1, 11):
        moves = {}
        for e in ground:
            neighbors = neighbors_all(e)
            if any(n in ground for n in neighbors):
                # there is at least one elf around, add a suggested move
                for i in range(4):
                    dx, dy = delta_dir(directions[(d + i) % 4])
                    if not any(
                        [
                            x in ground
                            for x in move_check(e[0], e[1], directions[(d + i) % 4])
                        ]
                    ):
                        moves[e] = e[0] + dx, e[1] + dy
                        break

        # second half
        # Simultaneously, each Elf moves to their proposed destination tile if they were the only Elf to propose moving to that position.
        # If two or more Elves propose moving to the same position, none of those Elves move.
        for source, target in moves.items():
            if len(set([k for k, v in moves.items() if v == target])) == 1:
                ground.remove(source)
                ground.add(target)

        # the first direction the Elves considered is moved to the end of the list of directions.
        d = (d + 1) % 4

        print(f"after round {r}:")
        print(mdump(ground))
        print()

    return mdump(ground).count(".")


def solve2(data):
    """Solves part2."""

    ground = parser(data)
    directions = ["N", "S", "W", "E"]
    d = 0

    print("initial state: ")
    print(mdump(ground))
    print()

    # first half
    # each Elf considers the eight positions adjacent to themself.
    #   - If no other Elves are in one of those eight positions, the Elf does not do anything during this round
    #   - Otherwise, the Elf looks in each of four directions in the following order and proposes moving one step in the first valid direction:

    for r in range(100_000_000_000):
        moving = False
        moves = {}
        for e in ground:
            neighbors = neighbors_all(e)
            if any(n in ground for n in neighbors):
                # there is at least one elf around, add a suggested move
                for i in range(4):
                    dx, dy = delta_dir(directions[(d + i) % 4])
                    if not any(
                        [
                            x in ground
                            for x in move_check(e[0], e[1], directions[(d + i) % 4])
                        ]
                    ):
                        moves[e] = e[0] + dx, e[1] + dy
                        break

        # second half
        # Simultaneously, each Elf moves to their proposed destination tile if they were the only Elf to propose moving to that position.
        # If two or more Elves propose moving to the same position, none of those Elves move.
        for source, target in moves.items():
            if len(set([k for k, v in moves.items() if v == target])) == 1:
                ground.remove(source)
                ground.add(target)
                moving = True

        # the first direction the Elves considered is moved to the end of the list of directions.
        d = (d + 1) % 4

        # print(mdump(ground))
        # print()

        if not moving:
            print(f"the first round where no Elf moved was round {r + 1}:")
            return f"no more moves after {r}"


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
