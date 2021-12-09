#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def parser(data):
    signal_patterns = []
    four_digits_output_values = []

    for line in data.splitlines():
        sp, fourdov = line.split(" | ")
        sp = [''.join(sorted(s)) for s in sp.split(" ")]
        fourdov = [''.join(sorted(f)) for f in fourdov.split(" ")]
        signal_patterns.append(sp)
        four_digits_output_values.append(fourdov)

    return signal_patterns, four_digits_output_values


def solve1(data):
    """Solves part 1."""
    signal_patterns, four_digits_output_values = parser(data)
    uniq_digit = 0

    for display in four_digits_output_values:
        for digit in display:
            if len(digit) in [2,3,4,7]:
                uniq_digit += 1
    return uniq_digit


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
