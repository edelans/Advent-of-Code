#!/usr/bin/env python3
"""AoC 2020"""

import os
import sys
# import re
# import itertools
from aoc_utilities import Input

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def parser(boarding_pass):
    """Parse input to return tuple (row, column)"""
    return (int(boarding_pass[:7].replace('F', '0').replace('B', '1'), 2),
            int(boarding_pass[7:].replace('L', '0').replace('R', '1'), 2))


def compute_id(seat):
    """returns the id of the boarding pass"""
    return seat[0] * 8 + seat[1]


def solve1(lines):
    """Solves part 1."""
    return max(compute_id(parser(line)) for line in lines)


def reverse_id(bid):
    """
    from boarding pass ID to boarding pass string
    useless : but I thought at first that part 2 required returning the boarding pass code, not ID.
    """
    col = bid % 8
    row = int((bid - col) / 8)
    col_code = bin(col)[2:].zfill(3).replace('0', 'L').replace('1', 'R')
    row_code = bin(row)[2:].zfill(7).replace('0', 'F').replace('1', 'B')
    return row_code + col_code


def solve2(lines):
    """Solves part2."""
    start = min(compute_id(parser(line)) for line in lines)
    end = max(compute_id(parser(line)) for line in lines)
    print("ids range from {} to {}".format(start, end))
    ids = set(i for i in range(start, end + 1))
    for line in lines:
        ids.remove(compute_id(parser(line)))
    return ids.pop()


"""
Use script args to execute the right function.
"""
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '1':
        res = solve1((Input(DAY).readlines()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        res = solve2((Input(DAY).readlines()))
        print(res)
