#!/usr/bin/env python3

from aoc_utilities import Input
import sys

# day must be 2 digit
DAY = '01'


"""
PART1
"""

def solve1(input):
    for i in range(len(input)):
        for j in range(i+1, len(input)):
            a = int(input[i])
            b = int(input[j])
            if (a + b) == 2020:
                return a * b
    raise Exception("Sorry, no match found in your input")

"""
PART 2
"""

def solve2(input):
    for i in range(len(input)):
        for j in range(i+1, len(input)):
            for k in range(j+1, len(input)):
                a = int(input[i])
                b = int(input[j])
                c = int(input[k])
                if (a + b + c) == 2020:
                    return a * b * c
    raise Exception("Sorry, no match found in your input")



if __name__ == '__main__':
    if sys.argv[1] == '1':
        res = solve1((Input(DAY).readlines()))
        print(res)

    if sys.argv[1] == '2':
        res = solve2((Input(DAY).readlines()))
        print(res)



