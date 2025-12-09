#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import logging
import os
import sys
from itertools import combinations

from aoc_utilities import Input, point_in_polygon, test_input, timer_func

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
    lines = [line.strip() for line in data.splitlines()]
    red_tiles = [tuple(map(int, line.split(","))) for line in lines]

    max_area = 0
    logger.info(f"red_tiles are {red_tiles}")
    for tile1, tile2 in combinations(red_tiles, 2):
        logger.info(f"Area between tiles {tile1} and {tile2} is {area(tile1, tile2)}")
        if area(tile1, tile2) > max_area:
            max_area = area(tile1, tile2)
            logger.info(
                f"Found new max_area is {max_area} for tiles {tile1} and {tile2}"
            )
    return max_area


def mprint(
    maping: dict[tuple[int, int], str | int],
    padding: int = 2,
    log_level: int = logging.DEBUG,
) -> None:
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
        logger.log(
            log_level,
            "".join([str(maping.get((x, y), ".")) for x in range(xmin, xmax + 1)]),
        )
    return


def add_green_tiles(red_tiles, tiles_dict):
    """Add green tiles connecting consecutive red tiles."""
    for i in range(len(red_tiles)):
        tile1 = red_tiles[i]
        tile2 = red_tiles[i + 1] if i + 1 < len(red_tiles) else red_tiles[0]
        # add all tiles between tile1 and tile2
        x_min, x_max = min(tile1[0], tile2[0]), max(tile1[0], tile2[0])
        y_min, y_max = min(tile1[1], tile2[1]), max(tile1[1], tile2[1])
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                tiles_dict.setdefault((x, y), "X")
        logger.debug(f"Added green tiles between {tile1} and {tile2}")
        mprint(tiles_dict, log_level=logging.DEBUG)

    logger.info("\nWith green tiles: ")
    mprint(tiles_dict)


def edges_intersect(edge1, edge2):
    """Check if two horizontal or vertical line segments cross.
    Args:
        edge1: ((x1, y1), (x2, y2)) - first line segment (horizontal or vertical)
        edge2: ((x3, y3), (x4, y4)) - second line segment (horizontal or vertical)
    Returns:
        True if segments cross (one horizontal, one vertical, and they intersect), False otherwise
    """
    (x1, y1), (x2, y2) = edge1
    (x3, y3), (x4, y4) = edge2

    edge1_horizontal = y1 == y2
    edge2_horizontal = y3 == y4

    # Both same orientation: they don't cross
    if edge1_horizontal == edge2_horizontal:
        return False

    # Make edge1 horizontal, edge2 vertical (swap if needed)
    if not edge1_horizontal:
        (x1, y1), (x2, y2), (x3, y3), (x4, y4) = (x3, y3), (x4, y4), (x1, y1), (x2, y2)

    # Now edge1 is horizontal, edge2 is vertical
    x_min, x_max = min(x1, x2), max(x1, x2)
    y_min, y_max = min(y3, y4), max(y3, y4)
    return x_min < x3 < x_max and y_min < y1 < y_max


def is_rect_inside_path(tile1, tile2, path_tiles):
    """Check if rectangle defined by tile1 and tile2 is completely inside the path."""
    x_min, x_max = min(tile1[0], tile2[0]), max(tile1[0], tile2[0])
    y_min, y_max = min(tile1[1], tile2[1]), max(tile1[1], tile2[1])

    corners = [
        (x_min, y_min),
        (x_max, y_min),
        (x_min, y_max),
        (x_max, y_max),
    ]

    # Early exit if any corner is outside
    if any(not point_in_polygon(corner, path_tiles) for corner in corners):
        return False

    rect_edges = [
        ((x_min, y_min), (x_max, y_min)),  # bottom edge
        ((x_min, y_max), (x_max, y_max)),  # top edge
        ((x_min, y_min), (x_min, y_max)),  # left edge
        ((x_max, y_min), (x_max, y_max)),  # right edge
    ]

    logger.info(
        f"Rectangle formed by {tile1} and {tile2} has all corners inside the polygon, checking its edges now..."
    )

    n = len(path_tiles)
    for rect_edge in rect_edges:
        for i in range(n):
            poly_edge = (path_tiles[i], path_tiles[(i + 1) % n])
            if edges_intersect(rect_edge, poly_edge):
                logger.info(
                    f"  - Rectangle edge {rect_edge} intersects polygon edge {poly_edge}"
                )
                return False

    return True


@timer_func
def solve2(data):
    """Solves part2."""
    lines = [line.strip() for line in data.splitlines()]
    red_tiles = [tuple[int, ...](map(int, line.split(","))) for line in lines]

    # Generate combinations sorted by area descending, allows early exit in iteration below
    all_combinations = sorted(
        combinations(red_tiles, 2),
        key=lambda pair: area(pair[0], pair[1]),
        reverse=True,
    )
    logger.info("All combinations generated and sorted.")

    for tile1, tile2 in all_combinations:
        if is_rect_inside_path(tile1, tile2, red_tiles):
            return area(tile1, tile2)


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
        res = solve2(Input(DAY).read())  # 4599890450 -> too high, 114727710 -> too low
        print(res)
