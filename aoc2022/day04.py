#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def solve1(data):
    """Solves part 1."""
    inclusions = 0
    for line in data.splitlines():
        int1, int2 = line.split(",")
        int1 = [int(x) for x in int1.split("-")]
        int2 = [int(x) for x in int2.split("-")]

        if int2[0] < int1[0]:
            int1, int2 = int2, int1

        if int2[0] == int1[0]:
            # if the 2 intervals start on the same index, put the longest one as int1
            if int2[1] > int1[1]:
                int1, int2 = int2, int1

        if int1[1] >= int2[1]:
            inclusions += 1
            print("{} includes {}".format(int1, int2))

    return inclusions


def solve2(data):
    """Solves part2."""
    overlaps = 0
    for line in data.splitlines():
        int1, int2 = line.split(",")
        int1 = [int(x) for x in int1.split("-")]
        int2 = [int(x) for x in int2.split("-")]

        if int2[0] < int1[0]:
            int1, int2 = int2, int1

        if int2[0] == int1[0]:
            # if the 2 intervals start on the same index, put the longest one as int1
            if int2[1] > int1[1]:
                int1, int2 = int2, int1

        if int2[0] <= int1[1]:
            overlaps += 1
        # print("{} overlaps {}".format(int1, int2))

    return overlaps


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
