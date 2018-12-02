# Python 3.x
from aoc_utilities import Input
import sys
import itertools

# day must be 2 digit
DAY = '02'


"""
PART1
"""

def solve1(input):
    count2, count3 = 0, 0

    for id in input:
        occurences = {}
        for letter in id:
            occurences[letter] = occurences.get(letter, 0) + 1
        values = set(occurences.values())
        if 2 in values:
            count2+=1
        if 3 in values:
            count3+=1

    return count2*count3

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
