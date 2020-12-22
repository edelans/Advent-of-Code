#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input
from collections import deque

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def parser(data):
    p1, p2 = data.split("\n\n")
    deck1 = deque([int(x) for x in p1.splitlines()[1:]])
    deck2 = deque([int(x) for x in p2.splitlines()[1:]])
    return deck1, deck2


def score(deck):
    score = 0
    m = 1
    for _ in range(len(deck)):
        score += m * deck.pop()
        m += 1
    return score


def solve1(data):
    """Solves part 1."""
    deck1, deck2 = parser(data)
    while len(deck1) > 0 and len(deck2) > 0:
        card1 = deck1.popleft()
        card2 = deck2.popleft()
        if card1 > card2:
            deck1.append(card1)
            deck1.append(card2)
        else:
            deck2.append(card2)
            deck2.append(card1)
    print(deck1)
    print(deck2)

    return score(deck1), score(deck2)


def solve2(data):
    """Solves part2."""
    pass


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
