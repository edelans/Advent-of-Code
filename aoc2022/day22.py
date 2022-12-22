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
DIR_FACING = {0: ">", 1: "v", 2: "<", 3: "^"}


def parser(data):
    b, p = data.split("\n\n")
    board = {}
    for y, line in enumerate(b.splitlines(), 1):
        for x, c in enumerate(line, 1):
            if c != " ":
                board[(x, y)] = c

    path = []
    nb = ""
    while len(p) > 0:
        l, p = p[0], p[1:]
        if l.isdigit():
            nb += l
        else:
            path.append(int(nb))
            path.append(l)
            nb = ""
    if len(nb) > 0:
        path.append(int(nb))
    return board, path


def turn(facing, d):
    new_facing = facing + 1 if d == "R" else facing - 1
    new_facing = 0 if new_facing == 4 else new_facing
    new_facing = 3 if new_facing == -1 else new_facing
    return new_facing


def move(board, pos, facing, n):
    x, y = pos
    board[(x, y)] = DIR_FACING[facing]

    if facing == 0:
        dx, dy = 1, 0
    elif facing == 1:
        dx, dy = 0, 1
    elif facing == 2:
        dx, dy = -1, 0
    elif facing == 3:
        dx, dy = 0, -1

    for i in range(n):

        # compute potential new coordinates
        if (x + dx, y + dy) in board.keys():
            new_x, new_y = x + dx, y + dy
        else:
            # wrap around to the other side of the board
            if facing == 0:
                new_x, new_y = min([i for (i, j) in board.keys() if j == y]), y
            elif facing == 1:
                new_x, new_y = x, min([j for (i, j) in board.keys() if i == x])
            elif facing == 2:
                new_x, new_y = max([i for (i, j) in board.keys() if j == y]), y
            elif facing == 3:
                new_x, new_y = x, max([j for (i, j) in board.keys() if i == x])

        if board[(new_x, new_y)] == "#":
            # if we are in a wall, stop moving
            break
        else:
            # keep moving!
            x, y = new_x, new_y
            board[(x, y)] = DIR_FACING[facing]

    return board, (x, y)


def dump(m):
    """
    Helper function to print a map
    when the map is a dictionary, with keys as tuples of coordinates (1,2)
    no need to have all the coordinates in the keys
    """
    xmin = 1
    xmax = max([int(i) for (i, j) in m.keys()])
    ymin = 1
    ymax = max([int(j) for (i, j) in m.keys()])
    dump = ""
    for y in range(ymin, ymax + 1, 1):
        for x in range(xmin, xmax + 1):
            dump += str(m.get((x, y), " "))
        dump += "\n"
    return dump


def solve1(data):
    """Solves part 1."""
    board, path = parser(data)
    pos = (min([x for (x, y) in board.keys() if y == 1]), 1)
    facing = 0
    for ins in path:
        if isinstance(ins, int):
            board, pos = move(board, pos, facing, ins)
        else:
            facing = turn(facing, ins)
        print(f"after move {ins}, position is {pos} with facing {facing}")
    print(dump(board))
    return 1000 * pos[1] + 4 * pos[0] + facing
    # 152 022 too low
    # 34 430 too low


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
