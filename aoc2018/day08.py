#!/usr/bin/env python3
"""Template file to be used as boilerplate for each day puzzle."""
from aoc_utilities import Input
import aocd
import os
# import re
import sys
# import itertools

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


"""
PART1
"""

teststr = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'
# teststr = '    1 1 0 1 99 2 0 3 10 11 12 '
# teststr = '        0 1 99 2 0 3 10 11 12 '

def solve1(input):
    """Solves part 1."""
    return sumtree([int(i) for i in input[0].split()], {'sum': 0})


def sumtree(t, val):
    # print("start with t: {}".format(t))
    ch = t.pop(0)
    md = t.pop(0)
    for _ in range(ch):
        # enter recursion
        # print("t in the recursion is : {}".format(t))
        sumtree(t, counter)
    for _ in range(md):
        counter['sum'] += t.pop(0)  # we use a dict because we need a mutable objects
                                    # an int is not mutable -> if we use an int counter, recusions would overwrite
                                    # with new objects. Whereas with a mutable object like a dict,
                                    # recursions can access the same object and change it.
    return counter['sum']


"""
PART 2
"""


def valtree(t):
    # print("start with t: {}".format(t))
    ch = t.pop(0)
    md = t.pop(0)

    vals = [valtree(t) for _ in range(ch)]
    mds = [t.pop(0) for _ in range(md)]

    if ch == 0:
        return sum(mds)

    return sum(vals[i-1] for i in mds if i-1 in range(ch))


def solve2(input):
    """Solves part2."""
    return valtree([int(i) for i in input[0].split()])




"""
Use script args to execute the right function.
"""
if __name__ == '__main__':
    if len(sys.argv)>1 and sys.argv[1] == '1':
        res = solve1((Input(DAY).readlines()))
        print(res)
        if len(sys.argv) == 3:
            if sys.argv[2] == 's':
                print("attempting to submit the response '{}' to part 1: \n\n".format(res))
                aocd.submit1(res)

    if len(sys.argv)>1 and sys.argv[1] == '2':
        res = solve2((Input(DAY).readlines()))
        print(res)
        if len(sys.argv) == 3:
            if sys.argv[2] == 's':
                print("attempting to submit the response '{}' to part 2: \n\n".format(res))
                aocd.submit2(res)
