#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def get_points(shape1, shape2):
    """
    returns the points awarded to player 1 when he plays shape1 against shape2
    """
    shape_score = {
        "rock": 1,
        "paper": 2,
        "scissors": 3
    }
    win_score = {
        ("rock", "rock"): 3,
        ("rock", "paper"): 0,
        ("rock", "scissors"): 6,
        ("paper", "rock"): 6,
        ("paper", "paper"): 3,
        ("paper", "scissors"): 0,
        ("scissors", "rock"): 0,
        ("scissors", "paper"): 6,
        ("scissors", "scissors"): 3,
    }
    return shape_score[shape1] + win_score[(shape1, shape2)]


def solve1(data):
    """Solves part 1."""
    shape_map = {
        "A": "rock",
        "B": "paper",
        "C": "scissors",
        "X": "rock",
        "Y": "paper",
        "Z": "scissors"
    }
    total_score = 0
    for round in data.splitlines():
        (shape1, shape2) = (shape_map[x] for x in round.split(" "))
        total_score += get_points(shape2, shape1)
    return total_score


def solve2(data):
    """Solves part2."""
    total_score = 0
    shape_map = {
        "A": "rock",
        "B": "paper",
        "C": "scissors",
    }
    outcome_score_map = {
        "X": 0,
        "Y": 3,
        "Z": 6
    }
    shape_score = {
        "rock": 1,
        "paper": 2,
        "scissors": 3
    }
    shape_to_play = {
        "rock": {
            "X": "scissors",
            "Y": "rock",
            "Z": "paper"
        },
        "paper": {
            "X": "rock",
            "Y": "paper",
            "Z": "scissors"
        },
        "scissors": {
            "X": "paper",
            "Y": "scissors",
            "Z": "rock"
        }
    }
    for round in data.splitlines():
        opponent_shape, outcome = round.split(" ")
        opponent_shape = shape_map[opponent_shape]
        total_score += outcome_score_map[outcome] + shape_score[shape_to_play[opponent_shape][outcome]]

    return total_score


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
