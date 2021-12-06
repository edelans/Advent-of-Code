#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
import re
from aoc_utilities import Input, test_input

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def cycle(timers):
    newTimers = []
    for t in timers:
        if t>0:
            newTimers.append(t-1)
        else:
            newTimers.append(6)
            newTimers.append(8)
    return newTimers



def solve1(data):
    """Solves part 1."""
    fishTimers = [int(x) for x in re.findall(r'\d+', data)]
    for _ in range(80):
        fishTimers = cycle(fishTimers)
        #print(fishTimers)
    return len(fishTimers)


def cycle2(timers):
    """
    changing datastructure form list to dict to batch operations
    """
    newTimers = {}
    for k in range(1,9):
        newTimers[k-1] = timers.get(k,0)

    # dealing with 0 timers :
    newTimers[6] = newTimers.get(6,0) + timers.get(0,0)
    newTimers[8] = timers.get(0,0)
    return newTimers


def solve2(data):
    """Solves part2."""
    fishTimers = [int(x) for x in re.findall(r'\d+', data)]

    # initialize the dict for counting numbers of fishs who share the same timer value
    dictFishTimers = {}
    for t in fishTimers:
        dictFishTimers[t] = dictFishTimers.get(t, 0) + 1

    for d in range(256):
        dictFishTimers = cycle2(dictFishTimers)
        # print(f"After {d+1} days : {dictFishTimers}")

    return sum([v for v in dictFishTimers.values()])


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
