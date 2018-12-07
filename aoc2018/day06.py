#!/usr/bin/env python3
"""Template file to be used as boilerplate for each day puzzle."""
from aoc_utilities import Input
import aocd
import sys
# import itertools

# day must be 2 digit
DAY = '06'


"""
PART1
"""


def solve1(input):
    """Solves part 1."""
    mapping = {}
    cnt = 1
    for line in input:
        print(line)
        x, y = map(int, line.split(", "))
        mapping[(x,y)] = 'l' + str(cnt)
        cnt += 1


    min_x = print(min(mapping.items(), key=lambda i: i[0][0])[0][0])
    max_x = print(max(mapping.items(), key=lambda i: i[0][0])[0][0])
    min_y = print(min(mapping.items(), key=lambda i: i[0][1])[0][1])
    max_y = print(max(mapping.items(), key=lambda i: i[0][1])[0][1])

    return min_x, max_x, min_y, max_y
"""
PART 2
"""


def solve2(input):
    """Solves part2."""
    pass


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
