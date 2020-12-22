#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input
from collections import deque

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]

# to avoid messing up with indices
P1 = 0
P2 = 1


def parser(data):
    p1, p2 = data.split("\n\n")
    deck1 = deque([int(x) for x in p1.splitlines()[1:]])
    deck2 = deque([int(x) for x in p2.splitlines()[1:]])
    return [deck1, deck2]


def score(deck):
    score = 0
    m = 1
    for _ in range(len(deck)):
        score += m * deck.pop()
        m += 1
    return score


def solve1(data):
    """Solves part 1."""
    deck = parser(data)
    while len(deck[P1]) > 0 and len(deck[P2]) > 0:
        card1 = deck[P1].popleft()
        card2 = deck[P2].popleft()
        if card1 > card2:
            deck[P1].append(card1)
            deck[P1].append(card2)
        else:
            deck[P2].append(card2)
            deck[P2].append(card1)

    return score(deck[P1]), score(deck[P2])


def recursive_combat(deck):

    # record history to avoid infinity combats
    hist = set()

    while deck[P1] and deck[P2]:

        t = (tuple(deck[P1]), tuple(deck[P2]))
        if t in hist:
            return P1
        hist.add((tuple(deck[P1]), tuple(deck[P2])))

        card1 = deck[P1].popleft()
        card2 = deck[P2].popleft()

        if len(deck[P1]) >= card1 and len(deck[P2]) >= card2:
            rdeck1 = deque([deck[P1][i] for i in range(card1)])
            rdeck2 = deque([deck[P2][i] for i in range(card2)])
            winner = recursive_combat([rdeck1, rdeck2])

        else:
            winner = P1 if card1 > card2 else P2

        winner_card = card1 if winner == P1 else card2
        loser_card = card2 if winner == P1 else card1
        deck[winner].append(winner_card)
        deck[winner].append(loser_card)

    return winner


def solve2(data):
    """Solves part2."""
    deck = parser(data)

    recursive_combat(deck)

    return score(deck[P1]), score(deck[P2])


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
        # res = solve2((test_input(DAY).read()))
        res = solve2("""Player 1:
43
19

Player 2:
2
29
14""")
        print(res)
