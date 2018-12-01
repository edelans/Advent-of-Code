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

"""
PART 2
"""
import itertools


def solve2(input):
    freq = 0
    freq_set = set([])

    for delta in itertools.cycle(input):
        freq += int(delta)
        if freq in freq_set:
            return freq
        else:
            freq_set.add(freq)


res = solve2((Input(DAY).readlines()))
print(res)
