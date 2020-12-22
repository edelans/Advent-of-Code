#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input
from collections import deque

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]

# to avoid messing up with indiced
P1 = 0
P2 = 1

# history as global var to help with recursions
hist = set()


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
    print("\ngame with:")
    print(f'deck1 = {deck[P1]}')
    print(f'deck2 = {deck[P2]}')
    if (tuple(deck[P1]), tuple(deck[P2])) in hist:
        print("infinite game detected, player1 wins")
        return P1
    else:
        hist.add((tuple(deck[P1]), tuple(deck[P2])))

    card1 = deck[P1].popleft()
    card2 = deck[P2].popleft()

    if len(deck[P1]) >= card1 and len(deck[P2]) >= card2:
        # recursive combat
        print("\n=== entering subgame ===\n")
        rdeck1 = deque([deck[P1][i] for i in range(card1)])
        rdeck2 = deque([deck[P2][i] for i in range(card2)])
        winner = recursive_combat([rdeck1, rdeck2])

    else:
        # winner of the round is the player with the higher-value card
        print("regular combat")
        winner = P1 if card1 > card2 else P2

    return winner


def solve2(data):
    """Solves part2."""
    deck = parser(data)

    while len(deck[P1]) > 0 and len(deck[P2]) > 0:

        winner = recursive_combat(deck)

        card1 = deck[P1].popleft()
        card2 = deck[P2].popleft()
        winner_card = card1 if winner == P1 else card2
        loser_card = card2 if winner == P1 else card1

        deck[winner].append(winner_card)
        deck[winner].append(loser_card)

    print(deck[P1])
    print(deck[P2])

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
        res = solve2((test_input(DAY).read()))
        print(res)
