#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
import json
from aoc_utilities import Input, test_input

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def parser(data):
    raw_lines = data.splitlines()
    all_ingredients = set()
    all_allergens = set()
    lines = []
    for raw_line in raw_lines:
        ingredients, allergens = raw_line.split("(contains ")
        ingredients = ingredients.strip().split(' ')
        all_ingredients |= set(ingredients)
        allergens = allergens[:-1].split(', ')
        all_allergens |= set(allergens)
        lines.append((ingredients, allergens))
    return lines, all_ingredients, all_allergens


def solve1(data):
    """Solves part 1."""
    lines, all_ingredients, all_allergens = parser(data)

    # intersect all ingredient list for each allergen
    allergens = {}
    unsafe_ingredients = set()
    for (l_ingredients, l_allergens) in lines:
        for a in l_allergens:
            if a in allergens:
                allergens[a] &= set(l_ingredients)
            else:
                allergens[a] = set(l_ingredients)
            if len(allergens[a]) == 1:
                unsafe_ingredients |= allergens[a]

    # flatten the intersection sets iteratively, worst case we have to to it len(lines) times
    for _ in range(len(lines)):
        for k, v in allergens.items():

            if len(v) > 1:
                v -= unsafe_ingredients
                if len(v) == 1:
                    unsafe_ingredients |= v

    safe_ingredients = all_ingredients - unsafe_ingredients

    # compute the count asked
    count = 0
    for line in lines:
        for ing in safe_ingredients:
            if ing in line[0]:
                count += 1

    return count


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
