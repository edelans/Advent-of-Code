#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
import math
import operator
import logging
from aoc_utilities import Input, test_input

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def parser(data):
    instructions = []
    for line in data.splitlines():
        direction, steps = line.split(" ")
        instructions.append((direction, int(steps)))
    return instructions


def vsum(a, b):
    """
    vector sum, both vectors must be the same size
    """
    return tuple(map(operator.add, a, b))


def solve1(data):
    """Solves part 1."""
    instructions = parser(data)
    hp = (0, 0)  # head position
    tp = (0, 0)  # tail position
    dir_vect = {
        "R": (1, 0),
        "L": (-1, 0),
        "U": (0, 1),
        "D": (0, -1),
    }
    tail_positions = set([])

    for ins in instructions:
        for s in range(ins[1]):
            hp = vsum(hp, dir_vect[ins[0]])
            logger.info(f"distance is now {math.dist(hp, tp)}")
            if math.dist(hp, tp) > 1.5 and (hp[0] == tp[0] or hp[1] == tp[1]):
                tp = vsum(tp, dir_vect[ins[0]])
            elif math.dist(hp, tp) > 1.5 and (hp[0] != tp[0] and hp[1] != tp[1]):
                move = (
                    int(math.copysign(1, hp[0] - tp[0])),
                    int(math.copysign(1, hp[1] - tp[1])),
                )
                tp = vsum(tp, move)
            tail_positions.add(tp)
            logger.info(f"head is at {hp}, while tail is at {tp}")
    return len(tail_positions)


def tprint(positions, logLevel=30):
    """
    print a map of the positions provided as a set
    """
    xmax = max(max([int(i) for (i, j) in positions]), 10)
    xmin = min(min([int(i) for (i, j) in positions]), -10)
    ymax = max(max([int(j) for (i, j) in positions]), 10)
    ymin = min(min([int(j) for (i, j) in positions]), -10)
    for y in range(ymax, ymin - 1, -1):
        line = ""
        for x in range(xmin, xmax + 1):
            if (x, y) == (0, 0):
                line += "s"
            elif (x, y) in positions:
                line += "#"
            else:
                line += "."
        logger.log(logLevel, line)
    logger.log(logLevel, "\n")
    return


def rope_print(rope, logLevel=10):
    """
    print a map of the rope, provided as a list of position for each of his knots : [ (1,2), (0,0), ...]
    logLevel is an int, 10 is for debug, 20 is for info
    """

    xmax = max(max([int(i) for (i, j) in rope]), 10)
    xmin = min(min([int(i) for (i, j) in rope]), -10)
    ymax = max(max([int(j) for (i, j) in rope]), 10)
    ymin = min(min([int(j) for (i, j) in rope]), -10)
    for y in range(ymax, ymin - 1, -1):
        line = ""
        for x in range(xmin, xmax + 1):
            if (x, y) == (0, 0):
                line += "s"
            elif (x, y) in rope:
                line += str(rope.index((x, y)))
            else:
                line += "."
        logger.log(logLevel, line)
    logger.log(logLevel, "\n")
    return


def solve2(data):
    """Solves part2."""
    instructions = parser(data)
    dir_vect = {
        "R": (1, 0),
        "L": (-1, 0),
        "U": (0, 1),
        "D": (0, -1),
    }
    rope = [(0, 0) for _ in range(10)]
    tail_positions = set([])

    for ins in instructions:
        for s in range(ins[1]):
            logger.debug(f"\nrunning step {s+1} from instruction {ins[0]} {ins[1]}")
            rope[0] = (
                rope[0][0] + dir_vect[ins[0]][0],
                rope[0][1] + dir_vect[ins[0]][1],
            )
            for i in range(1, len(rope)):
                # reuse var names from solve1 so I can copy paste bc I'm lazy
                hp = rope[i - 1]
                tp = rope[i]

                if math.dist(hp, tp) > 1.5:
                    move = (
                        int(math.copysign(1, hp[0] - tp[0])) if hp[0] != tp[0] else 0,
                        int(math.copysign(1, hp[1] - tp[1])) if hp[1] != tp[1] else 0,
                    )
                    rope[i] = (
                        rope[i][0] + move[0],
                        rope[i][1] + move[1],
                    )
                tail_positions.add(rope[9])
                if logger.getEffectiveLevel() < 15:
                    rope_print(rope, 10)
        if logger.getEffectiveLevel() < 25:
            rope_print(rope, 20)

    tprint(tail_positions, 20)
    return len(tail_positions)
    # 2595 is too high :/


"""
Use script args to execute the right function.
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
        logger.setLevel(logging.CRITICAL + 1)  # will basically disable logging
        res = solve2((Input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2t":
        logger.setLevel(logging.INFO)
        res = solve2((test_input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2t2":
        logger.setLevel(logging.DEBUG)
        data = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""
        res = solve2(data)
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "rp":
        logger.setLevel(logging.INFO)
        rope_print([(3, 1), (2, 0), (1, 0), (0, 0)])
