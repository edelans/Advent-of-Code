#!/usr/bin/env python3
"""Template file to be used as boilerplate for each day puzzle."""
from aoc_utilities import Input
import aocd
import os
# import re
import sys
# import itertools
from collections import defaultdict
# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


"""
PART1
"""



def solve1(input):
    """Solves part 1."""
    input = input[0].split()
    players = int(input[0])
    max_marble = int(input[6])
    return marble_scores(players, max_marble)


def marble_scores(players, max_marble):
    scores = defaultdict(int)
    curr_marble_idx = 0
    circle = [0]

    for i in range(1, max_marble + 1):
        if i % 23 == 0:
            player = i % players
            scores[player] += i + circle.pop(curr_marble_idx - 7)
            curr_marble_idx = curr_marble_idx - 7
        else:
            insertion_idx = (curr_marble_idx + 2) % len(circle)
            circle.insert(insertion_idx, i)
            curr_marble_idx = insertion_idx
        # print("{} : {}".format(i % players, circle))

    # print(scores)
    return max(scores.values())


def marble_scores(max_players, max_marble):
    scores = defaultdict(int)
    curr_marble_idx = 0
    circle = [0]

    for marble in range(1, max_marble + 1):
        if marble % 23 == 0:
            scores[marble % max_players] += marble
            curr_marble_idx = (curr_marble_idx - 7) % len(circle)
            scores[marble % max_players] += circle.pop(curr_marble_idx)
            curr_marble_idx = curr_marble_idx % len(circle)
        else:
            insertion_idx = (curr_marble_idx + 1) % len(circle) + 1
            circle.insert(insertion_idx, marble)
            curr_marble_idx = insertion_idx
        # print("{} : {}".format(i%max_players, circle))
    # print(scores)
    return max(scores.values())

# print(marble_scores2(9, 25))
# print(marble_scores(10, 1618))
# print(marble_scores(13, 7999))
# print(marble_scores(17, 1104))
# print(marble_scores(21, 6111))
print(marble_scores(30, 5807))
# 439068 IS TOO LOW

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
