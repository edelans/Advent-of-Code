#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input
from collections import deque, defaultdict


# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def parser(data):
    ptemplate, rules = data.split("\n\n")
    rules = {k:v for (k,v) in [line.split(" -> ") for line in rules.splitlines()]}
    return ptemplate, rules

def solve1(data):
    """Solves part 1."""
    ptemplate, rules = parser(data)
    polymer = deque(ptemplate)

    for _ in range(10):
        for _ in range(len(polymer) - 1):
            pattern = ''.join([polymer[0], polymer[1]])
            #print(f"looking for pattern {pattern}")
            polymer.rotate(-1)
            if pattern in rules:
                #print(f"pattern found ! inserting {rules[pattern]}")
                polymer.append(rules[pattern])
                #print(polymer)
                #print()
        polymer.rotate(-1)

    #print(polymer)

    elements = set(polymer)
    counts = [polymer.count(x) for x in elements]

    return max(counts) - min(counts)




def solve2(data):
    """
    Perf problem with first approach
    As often with performance problems, let's revisit the data structure, and try to factorize the data we store
    -> let's store only pairs, this is all we need to deliver the final result
    """
    ptemplate, rules = parser(data)

    pcount = defaultdict(int)

    for i in range(len(ptemplate)-1):
        pcount[''.join([ptemplate[i], ptemplate[i+1]])] += 1

    for _ in range(40):
        new_pcount = defaultdict(int)   # let's create a new dict to store the pair counts in the new step
                                        # a new dict to avoid changing the pairs during the iteration

        for p in [k for k, v in pcount.items() if v > 0]:
            #print(p)
            if p in rules:
                # one pair is replaced by 2 new pairs
                new_pair_left = ''.join([p[0], rules[p]])
                new_pair_right = ''.join([rules[p], p[1]])

                new_pcount[new_pair_left] += pcount[p]
                new_pcount[new_pair_right] += pcount[p]

            else:
                new_pcount[p] = pcount[p]

        pcount = new_pcount


    #new dict storing counts for each elements
    ecount = defaultdict(int)
    for p, c in pcount.items():
        ecount[p[0]] += c
    ecount[ptemplate[-1]] += 1  # last char is not counted in the iteration above
                                # last char of the polymer always remain the same
    return max(ecount.values()) - min(ecount.values())



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

