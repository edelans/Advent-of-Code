#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
import re

from aoc_utilities import Input, test_input

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def eval_line(line):
    # resolve parentheses first
    m = re.search(r"\(\d+\s[+*]\s\d+\)", line)
    if m:
        return eval_line(line.replace(m.group(0), str(eval(m.group(0))), 1))

    # then eval the first operation on the left
    m2 = re.search(r"\d+\s[+*]\s\d+", line)
    if m2:
        return eval_line(line.replace(m2.group(0), str(eval(m2.group(0))), 1))

    # when there is no more operation or parenthesis
    return int(line)


def solve1(data):
    """Solves part 1."""
    return sum([eval_line(line) for line in data])


def solve2(data):
    """Solves part2."""
    pass


"""
Use script args to execute the right function.
"""
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '1':
        res = solve1((Input(DAY).readlines()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '1t':
        print(eval_line("1 + 2 * 3 + 4 * 5 + 6"))
        print(eval_line("1 + (2 * 3) + (4 * (5 + 6))"))
        print(eval_line("2 * 3 + (4 * 5)"))
        print(eval_line("5 + (8 * 3 + 9 + 3 * 4 * 3)"))
        print(eval_line("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"))
        print(eval_line("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"))

    if len(sys.argv) > 1 and sys.argv[1] == '2':
        res = solve2((Input(DAY).readlines()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '2t':
        res = solve2((test_input(DAY).readlines()))
        print(res)
