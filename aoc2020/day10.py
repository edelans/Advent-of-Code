#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input
# import re
# import itertools

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def solve1(data):
    """Solves part 1."""
    adapters = sorted([0] + [int(x) for x in data])
    print(adapters)
    delta1 = 0
    delta3 = 1  # accoutns for the end of the chain which is always 3 jolts diff
    for i in range(0, len(adapters) - 1):
        if adapters[i + 1] - adapters[i] == 1:
            delta1 += 1
        if adapters[i + 1] - adapters[i] == 3:
            delta3 += 1
    return delta1, delta3, delta1 * delta3


def solve2(data):
    """Solves part2."""
    for i in data:
        print(i)
    pass

# part2 solved by hand : 
"""
dans l'input ya que des écarts de 1 ou de 3
les écarts de 3 ne permettent pas d'alternative
les écarts de 1 permettent différentes alternatives en fonction de leur longueur :
  - pas d'alternative pour une suite de 2 élément
  - 2 alternatives pour une suite de 3 elements
  - 4 aternatives pour une suite de 4 éléments
  - 7 alternatives pour une suite de 5 éléments
  - yavais pas de suite plus grande que ça
2^x*4^y*7^z avec x le nombre de suite 3 éléments écartés de 1, y celui de 4 et z celui de 5
"""


"""
Use script args to execute the right function.
"""
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '1':
        res = solve1((Input(DAY).readlines()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '1t':
        res = solve1((test_input(DAY).readlines()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        res = solve2((Input(DAY).readlines()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '2t':
        res = solve2((test_input(DAY).readlines()))
        print(res)
