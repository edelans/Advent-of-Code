#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def parser(data):
    header, body = data.split("\n\n")
    header = header.splitlines()
    nb_of_stacks = int(header.pop().split(" ")[-1])
    # print("there are {} stacks".format(nb_of_stacks))
    stacks = []
    moves = []
    for i in range(nb_of_stacks):
        stacks.append([])

    while header:
        line = header.pop()
        for i in range(nb_of_stacks):
            if 4 * i < len(line) and line[4 * i] != " ":
                stacks[i].append(line[4 * i + 1])

    for move in body.splitlines():
        move = move.split(" ")
        moves.append((int(move[1]), int(move[3]), int(move[5])))

    return stacks, moves


def solve1(data):
    """Solves part 1."""
    stacks, moves = parser(data)

    for move in moves:
        for i in range(move[0]):
            stacks[move[2] - 1].append(stacks[move[1] - 1].pop())
    return "".join([s[-1] for s in stacks])


def solve2(data):
    """Solves part2."""
    stacks, moves = parser(data)

    for move in moves:
        stacks[move[1] - 1], to_move = (
            stacks[move[1] - 1][: len(stacks[move[1] - 1]) - move[0]],
            stacks[move[1] - 1][len(stacks[move[1] - 1]) - move[0] :],
        )
        stacks[move[2] - 1].extend(to_move)
    return "".join([s[-1] for s in stacks])


"""
Use script args to execute the right function.
"""
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "1":
        res = solve1((Input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "1t":
        res = solve1((test_input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        res = solve2((Input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2t":
        res = solve2((test_input(DAY).read()))
        print(res)
