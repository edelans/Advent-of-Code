#!/usr/bin/env python3
"""Template file to be used as boilerplate for each day puzzle."""
from aoc_utilities import Input
import aocd
import sys
# import itertools

# day must be 2 digit
DAY = '05'


"""
PART1
"""


def collapse1(input):
    """Takes a string and returns polymer after one iteration of collapsing."""
    minuscul = "abcdefghijklmnopqrstuvwxyz"
    majuscul = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    reactors = [minuscul[i]+majuscul[i] for i in range(0, 26)] + [majuscul[i]+minuscul[i] for i in range(0, 26)]
    res = input
    for r in reactors:
        res = res.replace(r, "")
    return res


def collapseN(input):
    """Takes a string and returns totally collapsed (stable) polymer."""
    old = input
    new = collapse1(old)
    while len(old) > len(new):
        old = new
        new = collapse1(old)
    return new


def solve1(input):
    """Solves part 1."""
    return len(collapseN(input[0].strip()))


"""
PART 2
"""


def solve2(input):
    """Solves part2."""
    l = []  # store fully collapsed polymer length for each unit removed
    minuscul = "abcdefghijklmnopqrstuvwxyz"
    majuscul = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    for i in range(0, 26):
        variant = input[0].strip().replace(minuscul[i], "").replace(majuscul[i], "")
        l.append(len(collapseN(variant)))

    print(l)

    return min(l)


"""
Use script args to execute the right function.
"""
if __name__ == '__main__':
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
    if sys.argv[1] == '3':
        res = collapseN("dabAcCaCBAcCcaDA".replace("a", "").replace("A", ""))
        print(res)
