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


def get_pattern_to_digit_mapping(signal_pattern):

    # pattern to digit mapper: digit[pattern] yields the digit
    digit = {}

    # get all easy mappings
    for p in signal_pattern:
        if len(p) == 2:
            digit[p] = 1
        elif len(p) == 4:
            digit[p] = 4
        elif len(p) == 3:
            digit[p] = 7
        elif len(p) == 7:
            digit[p] = 8

    # digit to pattern mapper: pattern[digit] yields the pattern
    pattern = {v: k for k,v in digit.items()}

    # second run where we are sure to have mapped all easy patterns
    for p in signal_pattern:
        if len(p) == 5:
            # 2, 3 or 5

            # 3 is the only one to "include" the 1
            if set(pattern[1]).issubset(set(p)):
                digit[p] = 3

            # 5 and 4 have 3 common segments, while 2 and 4 have only 2
            elif len(set(p) & set(pattern[4])) == 3:
                digit[p] = 5
            else:
                digit[p] = 2

        if len(p) == 6:
            # 0, 6 or 9

            # 6 is the only one to not include the segments of 1
            if not set(pattern[1]).issubset(set(p)):
                digit[p] = 6

            # 9 is the only one to include the segments of 4
            elif set(pattern[4]).issubset(set(p)):
                digit[p] = 9

            else:
                digit[p] = 0

    return digit



def solve2(data):
    """Solves part2."""
    signal_patterns, four_digits_output_values = parser(data)
    total = 0

    for index, signal_pattern in enumerate(signal_patterns):
        pattern_to_digit = get_pattern_to_digit_mapping(signal_pattern)
        output_value = pattern_to_digit[four_digits_output_values[index][0]] * 1000 \
                        + pattern_to_digit[four_digits_output_values[index][1]] * 100 \
                        + pattern_to_digit[four_digits_output_values[index][2]] * 10 \
                        + pattern_to_digit[four_digits_output_values[index][3]] * 1
        print(f"output value is {output_value}")
        total += output_value

    return total


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
