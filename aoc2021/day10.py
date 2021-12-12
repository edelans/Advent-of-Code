#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input
from collections import deque
from statistics import median


# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]



def solve1(data):
    """Solves part 1."""
    SCORES = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137
    }
    total = 0

    for line in data.splitlines():
        stack = deque()
        for c in line:
            if c == '(':
                stack.append(')')
            elif c == '[':
                stack.append(']')
            elif c == '<':
                stack.append('>')
            elif c == '{':
                stack.append('}')

            elif c in ')>}]':
                expected_closing = stack.pop()
                if c != expected_closing:
                    print(f"Expected {expected_closing}, but found {c} instead")
                    total += SCORES[c]
    return total


def solve2(data):
    """Solves part2."""
    SCORES = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4
    }

    incomplete_lines_scores = []

    for line in data.splitlines():
        stack = deque()
        corrupt = False

        for c in line:
            if c == '(':
                stack.append(')')
            elif c == '[':
                stack.append(']')
            elif c == '<':
                stack.append('>')
            elif c == '{':
                stack.append('}')

            elif c in ')>}]':
                expected_closing = stack.pop()
                if c != expected_closing:
                    # corrupted line
                    corrupt = True

        score = 0
        if len(stack) > 0 and not corrupt:
            # incomplete line
            while len(stack) > 0:
                score *= 5
                score += SCORES[stack.pop()]
            incomplete_lines_scores.append(score)

    print(incomplete_lines_scores)
    return median(incomplete_lines_scores)


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
