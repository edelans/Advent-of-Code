# Python 3.x
from aoc_utilities import Input
import sys
import itertools

# day must be 2 digit
DAY = '01'


"""
PART1
"""

def solve1(input):
    return



"""
PART 2
"""


def solve2(input):
    return



if sys.argv[1] == '1':
    res = solve1((Input(DAY).readlines()))
    print(res)
    if len(sys.argv) == 3:
        if sys.argv[2] == 's':
            submit1(res)

if sys.argv[1] == '2':
    res = solve1((Input(DAY).readlines()))
    print(res)
    if len(sys.argv) == 3:
        if sys.argv[2] == 's':
            submit2(res)
