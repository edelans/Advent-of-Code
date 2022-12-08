#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
import logging

from aoc_utilities import Input, test_input

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def solve1(data):
    """Solves part 1."""
    forest = []
    for line in data.splitlines():
        treeline = []
        for char in line:
            treeline.append(int(char))
        forest.append(treeline)

    # init visible trees with the trees visible on the edge
    visible_trees = 2 * len(forest) + 2 * len(forest[1]) - 4

    # add visible trees inside the forest
    for i in range(1, len(forest) - 1):
        for j in range(1, len(forest[i]) - 1):
            tree_height = forest[i][j]
            visibility_array = []

            left_visibility = all([forest[i][k] < tree_height for k in range(j)])
            if left_visibility:
                visibility_array.append("left")

            right_visibility = all(
                [forest[i][k] < tree_height for k in range(j + 1, len(forest[i]))]
            )
            if right_visibility:
                visibility_array.append("right")

            up_visibility = all([forest[k][j] < tree_height for k in range(i)])
            if up_visibility:
                visibility_array.append("up")

            down_visibility = all(
                [forest[k][j] < tree_height for k in range(i + 1, len(forest))]
            )
            if down_visibility:
                visibility_array.append("down")

            if len(visibility_array) > 0:
                visible_trees += 1
                logger.info(
                    f"The tree at line {i}, col {j} with height {tree_height} is visible from {visibility_array}"
                )
    return visible_trees


def solve2(data):
    """Solves part2."""
    max_scenic_score = 0
    forest = []
    for line in data.splitlines():
        treeline = []
        for char in line:
            treeline.append(int(char))
        forest.append(treeline)

    # compute scenic score for each tree
    for i in range(1, len(forest) - 1):
        for j in range(1, len(forest[i]) - 1):
            tree_height = forest[i][j]
            scenic_score = 1

            # list of trees as viewed from the current tree
            left_trees = [forest[i][k] for k in range(j)][::-1]
            right_trees = [forest[i][k] for k in range(j + 1, len(forest[i]))]
            up_trees = [forest[k][j] for k in range(i)][::-1]
            down_trees = [forest[k][j] for k in range(i + 1, len(forest))]
            tree_views = [left_trees, right_trees, up_trees, down_trees]
            logger.info(
                f"the tree view for tree at line {i}, col {j} with height {tree_height} is {tree_views}"
            )

            for line_of_sight in tree_views:
                viewing_distance = 0
                t = 0
                while t < len(line_of_sight):
                    viewing_distance += 1
                    if line_of_sight[t] < tree_height:
                        t += 1
                    else:
                        t = len(line_of_sight)  # stop the while loop
                logger.info(
                    f"viewing distance for tree line {line_of_sight} is {viewing_distance} (height is {tree_height})"
                )
                scenic_score *= viewing_distance

            if scenic_score > max_scenic_score:
                max_scenic_score = scenic_score

    return max_scenic_score


"""
Use script args to execute the right function.
"""
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "1":
        logger.setLevel(logging.WARNING)
        res = solve1((Input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "1t":
        logger.setLevel(logging.INFO)
        res = solve1((test_input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        logger.setLevel(logging.WARNING)
        res = solve2((Input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2t":
        logger.setLevel(logging.INFO)
        res = solve2((test_input(DAY).read()))
        print(res)
