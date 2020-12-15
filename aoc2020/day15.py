#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input
from collections import defaultdict
# import re
# import itertools

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def next_number(numbers):
    last = numbers[-1]
    predecessors = numbers[0:-1]
    try:
        age = predecessors[::-1].index(last) + 1
        return age
    except ValueError as e:
        return 0


def solve1(data):
    """Solves part 1."""
    numbers = [int(x) for x in data[0].strip().split(',')]
    while len(numbers) < 2020:
        numbers.append(next_number(numbers))
    return numbers[-1]


def solve2_dumb(data):
    """Solves part 1."""
    numbers = [int(x) for x in data[0].strip().split(',')]
    while len(numbers) < 30000000:
        numbers.append(next_number(numbers))
    return numbers[-1]


def solve2(data):
    """Solves part 2."""
    numbers = [int(x) for x in data[0].strip().split(',')]

    # initialize
    last_index = {}
    last_nb = numbers[-1]
    for i, v in enumerate(numbers[0:-1]):
        last_index[v] = i

    # build
    for i in range(len(numbers), 30000000):
        previous_last_nb = last_nb
        if last_nb in last_index:
            last_nb = i - last_index[previous_last_nb] - 1
        else:
            last_nb = 0
        last_index[previous_last_nb] = i - 1

    return last_nb


"""
Use script args to execute the right function.
"""
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '1':
        res = solve1((Input(DAY).readlines()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '1t':
        res = solve1((test_input(DAY).readlines()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        res = solve2((Input(DAY).readlines()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '2t':
        res = solve2((test_input(DAY).readlines()))
        print(res)
