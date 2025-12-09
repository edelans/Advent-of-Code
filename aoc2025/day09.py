#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import logging
import os
import sys
from itertools import combinations

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


def area(tile1, tile2):
    return (abs(tile2[0] - tile1[0]) + 1) * (abs(tile2[1] - tile1[1]) + 1)


@timer_func
def solve1(data):
    """Solves part 1."""
    tiles = []
    lines = [line.strip() for line in data.splitlines()]
    for line in lines:
        x, y = line.split(",")
        x = int(x)
        y = int(y)
        tiles.append((x, y))

    max_area = 0
    logger.info(f"tiles are {tiles}")
    for tile1, tile2 in combinations(tiles, 2):
        logger.info(f"Area between tiles {tile1} and {tile2} is {area(tile1, tile2)}")
        if area(tile1, tile2) > max_area:
            max_area = area(tile1, tile2)
            logger.info(
                f"Found new max_area is {max_area} for tiles {tile1} and {tile2}"
            )
    return max_area


def mprint(maping: dict[tuple[int, int], str | int], padding: int = 2) -> None:
    """
    Helper function to print a map
    when the map is a dictionary, with keys as tuples of coordinates (1,2)
    no need to have all the coordinates in the keys
    """
    xmax = max([int(i) for (i, j) in maping]) + padding
    xmin = min([int(i) for (i, j) in maping]) - padding
    ymax = max([int(j) for (i, j) in maping]) + padding
    ymin = min([int(j) for (i, j) in maping]) - padding
    for y in range(ymin, ymax, 1):
        logger.info(
            "".join([str(maping.get((x, y), ".")) for x in range(xmin, xmax + 1)])
        )
    return


def is_area_inside(tile1, tile2, tiles_dict):
    for x in range(min(tile1[0], tile2[0]), max(tile1[0], tile2[0]) + 1):
        for y in range(min(tile1[1], tile2[1]), max(tile1[1], tile2[1]) + 1):
            if (x, y) not in tiles_dict:
                return False
    return True


@timer_func
def solve2(data):
    """Solves part2."""
    tiles_dict = {}

    # add red tiles
    lines = [line.strip() for line in data.splitlines()]
    red_tiles = []
    for line in lines:
        x, y = line.split(",")
        x = int(x)
        y = int(y)
        red_tiles.append((x, y))
        tiles_dict[(x, y)] = "#"

    logger.info("\nWith red tiles: ")
    mprint(tiles_dict)

    logger.info(f"red tiles are {red_tiles}")

    # add green tiles (connect consecutive red tiles)
    for i in range(len(red_tiles)):
        tile1 = red_tiles[i]
        tile2 = red_tiles[i + 1] if i + 1 < len(red_tiles) else red_tiles[-1]
        # add all tiles between tile1 and tile2
        x_min, x_max = min(tile1[0], tile2[0]), max(tile1[0], tile2[0])
        y_min, y_max = min(tile1[1], tile2[1]), max(tile1[1], tile2[1])
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                tiles_dict.setdefault((x, y), "X")

    logger.info("\nWith green tiles: ")
    mprint(tiles_dict)

    # fill allowed tiles with green tiles in the middle
    ymax = max(tiles_dict.keys(), key=lambda x: x[1])[1]
    ymin = min(tiles_dict.keys(), key=lambda x: x[1])[1]
    for y in range(ymin, ymax + 1):
        xtmin = min([tile[0] for tile in tiles_dict if tile[1] == y])
        xtmax = max([tile[0] for tile in tiles_dict if tile[1] == y])
        for x in range(xtmin, xtmax + 1):
            if (x, y) not in tiles_dict:
                tiles_dict[(x, y)] = "X"

    logger.info("\nWith filler tiles: ")
    mprint(tiles_dict)

    max_area_inside = 0
    # Use red_tiles directly instead of filtering from tiles_dict
    for tile1, tile2 in combinations(red_tiles, 2):
        rect_area = area(tile1, tile2)
        # Early exit: skip if area is not larger than current max
        if rect_area <= max_area_inside:
            continue

        logger.debug(f"Area between tiles {tile1} and {tile2} is {rect_area}")

        if is_area_inside(tile1, tile2, tiles_dict):
            logger.debug(
                f"Area between tiles {tile1} and {tile2} is inside allowed tiles"
            )
            max_area_inside = rect_area
            logger.debug(
                f"Found new max_area_inside is {max_area_inside} for tiles {tile1} and {tile2}"
            )
    return max_area_inside


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
        expected = 50  # TODO: replace with expected value
        assert res == expected, f"Expected {expected}, got {res}"
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "1":
        logger.setLevel(logging.WARNING)
        res = solve1(Input(DAY).read())
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2t":
        logger.setLevel(logging.INFO)
        res = solve2(test_input(DAY).read())
        expected = 24  # TODO: replace with expected value
        assert res == expected, f"Expected {expected}, got {res}"
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        logger.setLevel(logging.WARNING)
        res = solve2(Input(DAY).read())
        print(res)
