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


def decipher(signal_pattern, four_digit_output):
    segments = {}
    segments['one'] = set([x for x in signal_pattern if len(x) == 2])
    segments['four'] = set([x for x in signal_pattern if len(x) == 4])
    segments['seven'] = set([x for x in signal_pattern if len(x) == 3])
    segments['eight'] = set([x for x in signal_pattern if len(x) == 7])


    segments['two'] = set([x for x in signal_pattern if len(x) == 5])
    segments['three'] = set([x for x in signal_pattern if len(x) == 5])
    segments['five'] = set([x for x in signal_pattern if len(x) == 5])

    segments['six'] = set([x for x in signal_pattern if len(x) == 6])
    segments['zero'] = set([x for x in signal_pattern if len(x) == 6])
    segments['nine'] = set([x for x in signal_pattern if len(x) == 6])

    signal_line = {}
    signal_line["top"] = set(segments['seven'][0]) - set(segments['one'][0])
    signal_line["bottom"] = set(segments['six'][0]).intersection(set(segments['six'][1]), set(segments['six'][2])) - set(segments['seven'][0]) - set(segments['four'][0])

    # trouver le 9 en faisant 4 + top + bottom
    # trouver le 0 c'est celui à 6 char qui n'a qu'une linge de différence avec 9
    # en déduire le 6 (le seul restant non identifié des 6 char)

    # en déduire middle (9 - 0)
    # en déduire bottom left (0 - 9)
    # en déduire le 2
    # en déduire le 3 : le seul qui a 1 de diff avec le 2
    # en déduire le 5


    signal_line["top_right"] = set(segments['one'][0])
    signal_line["top_left"] =
    signal_line["middle"] =
    signal_line["bottom_right"] = set(segments['one'][0])
    signal_line["bottom_left"] =



    print(segments["nine"])



def solve2(data):
    """Solves part2."""
    signal_patterns, four_digits_output_values = parser(data)
    decipher(signal_patterns[0], four_digits_output_values[0])

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
