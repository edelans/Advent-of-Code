#!/usr/bin/env python3
"""Template file to be used as boilerplate for each day puzzle."""
from aoc_utilities import Input
import aocd
import os
import sys
# import itertools

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


"""
PART1
"""


def solve1(input):
    """Solves part 1."""
    requirements = {}  # is steps 3 requires steps 1 and 2 : {3 : [1, 2]}
    steps = set()
    # build requirements mapping
    for line in input:
        req, st = line.split(' ')[1], line.split(' ')[7]
        requirements[st] = requirements.get(st, []) + [req]
        steps.add(req)
        steps.add(st)
    print(requirements)

    # solve requirements one at a time
    res = ''
    while requirements != {}:
        for i in sorted(steps):
            if requirements.get(i, []) == []:
                res += i
                if i in requirements:
                    del requirements[i]
                steps -= set(i)
                for j in requirements:
                    if i in requirements[j]:
                        requirements[j].remove(i)
                break  # because requirement simplification may have altered order sorted(steps)
    return res


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
    if len(sys.argv) > 1 and sys.argv[1] == '1':
        res = solve1((Input(DAY).readlines()))
        print(res)
        if len(sys.argv) == 3:
            if sys.argv[2] == 's':
                print("attempting to submit the response '{}' to part 1: \n\n".format(res))
                aocd.submit1(res)

    if len(sys.argv) > 1 and sys.argv[1] == '2':
        res = solve2((Input(DAY).readlines()))
        print(res)
        if len(sys.argv) == 3:
            if sys.argv[2] == 's':
                print("attempting to submit the response '{}' to part 2: \n\n".format(res))
                aocd.submit2(res)
