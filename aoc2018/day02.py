#!/usr/bin/env python3
"""This is a test."""
from aoc_utilities import Input
import aocd
import sys

# day must be 2 digit
DAY = '02'


"""
PART1
"""


def solve1(input):
    """Solves part2."""
    count2, count3 = 0, 0

    for id in input:
        occurences = {}
        for letter in id:
            occurences[letter] = occurences.get(letter, 0) + 1
        values = set(occurences.values())
        if 2 in values:
            count2 += 1
        if 3 in values:
            count3 += 1

    return count2*count3

"""
PART 2
"""


def solve2(input):
    """Solves part2."""
    for i in range(0, len(input)):
        ref = input[i]
        for j in range(i+1, len(input)):
            # previous candidates were tested with previous references before
            candidate = input[j]
            diff_count, index = 0, 0
            for k in range(0, len(ref)):
                if ref[k] != candidate[k]:
                    diff_count += 1
                    index = k
            if diff_count == 1:
                print("the IDs are :\n{}{}{}".format(ref, candidate, (index)*' ' + '^'))
                return ref[:index]+ref[index+1:]

if sys.argv[1] == '1':
    res = solve1((Input(DAY).readlines()))
    print(res)
    if len(sys.argv) == 3:
        if sys.argv[2] == 's':
            print("attempting to submit the response '{}' to part 1: \n\n".format(res))
            aocd.submit1(res)

if sys.argv[1] == '2':
    res = solve2((Input(DAY).readlines()))
    print(res)
    if len(sys.argv) == 3:
        if sys.argv[2] == 's':
            print("attempting to submit the response '{}' to part 2: \n\n".format(res))
            aocd.submit2(res)
