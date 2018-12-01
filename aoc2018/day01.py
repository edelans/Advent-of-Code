# Python 3.x
from aoc_utilities import Input

# day must be 2 digit
DAY = '01'


"""
PART1
"""

def solve1(input):
    freq = 0

    for delta in input:
        freq += int(delta)

    return freq

# res = solve1((Input(DAY).readlines()))
# print(res)
