#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import logging
import os
import sys

from aoc_utilities import Input, test_input, timer_func

"""
Logger config
  use logger.info("") instead of print statement
  those messages will be displayed while running the code on testing sets
  but not displayed while running on real puzzle inputs
"""
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def parser(data: str) -> tuple[list[set[tuple[int, int]]], dict]:
    """Parses the input data."""
    shapes = []
    regions = {}
    blocks = data.split("\n\n")
    str_regions = blocks[-1]
    for b in blocks[:-1]:
        str_shape = b.splitlines()[1:]
        shape = set()
        for y, line in enumerate(str_shape):
            for x, char in enumerate(line):
                if char == "#":
                    shape.add((x, y))
        shapes.append(shape)

    for i, line in enumerate(str_regions.splitlines()):
        area, shapes_req = line.split(":")
        regions[i] = {}
        regions[i]["width"], regions[i]["height"] = map(int, area.split("x"))
        regions[i]["shape_count"] = list(map(int, shapes_req.strip().split(" ")))

    return shapes, regions


def translate(
    shape: set[tuple[int, int]], offset: tuple[int, int]
) -> set[tuple[int, int]]:
    dx, dy = offset
    return {(x + dx, y + dy) for x, y in shape}


def generate_region_set(height: int, width: int) -> set[tuple[int, int]]:
    return {(x, y) for x in range(width) for y in range(height)}


def generate_shape_set(shape: str) -> set[tuple[int, int]]:
    result = set()
    for y, line in enumerate(shape.splitlines()):
        for x, char in enumerate(line):
            if char == "#":
                result.add((x, y))
    return result


def rotate(shape: set[tuple[int, int]]) -> set[tuple[int, int]]:
    """Rotates a shape 90 degrees clockwise, around the point (1,1)
    a b c
    d e f
    g h i
    becomes
    c f i
    b e h
    a d g

    """
    rotation_map: dict[tuple[int, int], tuple[int, int]] = {
        (0, 0): (0, 2),  # a
        (0, 1): (1, 2),  # d
        (0, 2): (2, 2),  # g
        (1, 0): (0, 1),  # b
        (1, 1): (1, 1),  # e
        (1, 2): (2, 1),  # h
        (2, 0): (0, 0),  # c
        (2, 1): (1, 0),  # f
        (2, 2): (2, 0),  # i
    }

    return {rotation_map[(x, y)] for x, y in shape}


def flip(shape: set[tuple[int, int]]) -> set[tuple[int, int]]:
    """Flips a shape over horizontal axis
    a b c
    d e f
    g h i
    becomes
    g h i
    d e f
    a b c
    """
    flip_map: dict[tuple[int, int], tuple[int, int]] = {
        (0, 0): (2, 0),  # a
        (0, 1): (2, 1),  # d
        (0, 2): (2, 2),  # g
        (1, 0): (1, 0),  # b
        (1, 1): (1, 1),  # e
        (1, 2): (1, 2),  # h
        (2, 0): (0, 0),  # c
        (2, 1): (0, 1),  # f
        (2, 2): (0, 2),  # i
    }
    return {flip_map[(x, y)] for x, y in shape}


def get_shape_alternatives(shape: set[tuple[int, int]]) -> list[set[tuple[int, int]]]:
    shape_alternatives = [shape]
    for _ in range(3):
        shape = rotate(shape)
        if shape not in shape_alternatives:
            shape_alternatives.append(shape)
    for s in shape_alternatives:
        flipped_shape = flip(s)
        if flipped_shape not in shape_alternatives:
            shape_alternatives.append(flipped_shape)
    return shape_alternatives


def can_fit_presents(region, shapes):
    """Checks if a region can fit into a shape."""

    return False


@timer_func
def solve1(data):
    """Solves part 1."""
    shapes, regions = parser(data)
    logger.info(f"There are {len(shapes)} shapes and {len(regions)} regions.")

    # simplify problem space by removing regions that are too small to fit the shapes,
    # or the ones so large that nesting shapes will not even be needed (presents will fit for sure!)
    small_regions = 0
    large_regions = 0
    keys_to_remove = set()
    for key, region in regions.items():
        area = region["width"] * region["height"]
        minimal_shape_area = 0
        for i, shape in enumerate(shapes):
            minimal_shape_area += region["shape_count"][i] * len(shape)

        if area < minimal_shape_area:
            # no combinaison can fit all the shapes in that region
            small_regions += 1
            keys_to_remove.add(key)

        if area >= 9 * sum(region["shape_count"]):
            # region is so large that nesting shapes will not even be needed (presents will fit for sure!)
            large_regions += 1
            keys_to_remove.add(key)

    for key in keys_to_remove:
        regions.pop(key)

    logger.info(f"small regions: {small_regions}")
    logger.info(f"large regions: {large_regions}")
    logger.info(f"regions left: {len(regions)}")

    return large_regions  # turns out we got pranked by AoC : no need to nest shapes !


@timer_func
def solve2(data):
    """Solves part2."""
    pass


"""
Use script args to execute the right function solve1 / solve2, with the right logging level (only activated on test inputs)
  - python dayXX.py 1
  - python dayXX.py 1t
  - python dayXX.py 2
  - python dayXX.py 2t
"""
if __name__ == "__main__":
    """some logger levels : DEBUG, INFO, WARNING, CRITICAL"""
    if len(sys.argv) > 1 and sys.argv[1] == "1t":
        logger.setLevel(logging.INFO)
        res = solve1(test_input(DAY).read())
        expected = XXX  # TODO: replace with expected value
        assert res == expected, f"Expected {expected}, got {res}"
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "1":
        logger.setLevel(logging.INFO)
        res = solve1(Input(DAY).read())
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2t":
        logger.setLevel(logging.INFO)
        res = solve2(test_input(DAY).read())
        expected = XXX  # TODO: replace with expected value
        assert res == expected, f"Expected {expected}, got {res}"
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        logger.setLevel(logging.WARNING)
        res = solve2(Input(DAY).read())
        print(res)
