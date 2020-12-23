#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input
from collections import deque

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def move(circle, current_cup):
    max_cup = max(circle)
    min_cup = min(circle)

    while circle[0] != current_cup:
        circle.rotate(-1)

    circle.rotate(-1)
    c1 = circle.popleft()
    c2 = circle.popleft()
    c3 = circle.popleft()

    dest_cup = current_cup - 1
    while dest_cup not in circle:
        dest_cup -= 1
        if dest_cup < min_cup:
            dest_cup = max_cup

    while circle[0] != dest_cup:
        circle.rotate(-1)

    circle.rotate(-1)

    circle.extendleft([c3, c2, c1])

    while circle[0] != current_cup:
        circle.rotate()

    circle.rotate(-1)

    current_cup = circle[0]
    # print(circle)
    return circle, current_cup


def solve1(data):
    """Solves part 1."""
    circle = deque([int(x) for x in data.strip()])
    # print(circle)
    current_cup = circle[0]

    for i in range(100):
        circle, current_cup = move(circle, current_cup)

    while circle[0] != 1:
        circle.rotate(1)

    circle.popleft()

    return ''.join([str(x) for x in circle])


def solve2(data):
    """Solves part2."""
    pass


"""
Use script args to execute the right function.
"""
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '1':
        res = solve1((Input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '1t':
        res = solve1((test_input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        res = solve2((Input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '2t':
        res = solve2((test_input(DAY).read()))
        print(res)
