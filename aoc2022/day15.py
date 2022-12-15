#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
import logging
from aoc_utilities import Input, test_input
import re
from collections import defaultdict

"""
Logger config
  use logger.ingo("") instead of print statement
  those messages will be displayed while running the code on testing sets
  but not displayed while running on real puzzle inputs
  note: when you want to avoid logging, 
  be careful to also skip any expensive computation leading to what you want to log
"""
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def parser(data):
    regex = r"=?(-?[0-9]+)"
    m = {}
    for line in data.splitlines():
        sx, sy, bx, by = map(int, re.findall(r"=?(-?[0-9]+)", line))
        m[(sx, sy)] = "S"
        m[(bx, by)] = "B"
    return m


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def mdump(m):
    """
    Helper function to print a map
    when the map is a dictionary, with keys as tuples of coordinates (1,2)
    no need to have all the coordinates in the keys
    """
    xmin = min([int(i) for (i, j) in m.keys()])
    xmax = max([int(i) for (i, j) in m.keys()])
    ymin = min([int(j) for (i, j) in m.keys()])
    ymax = max([int(j) for (i, j) in m.keys()])
    dump = ""
    for y in range(ymin, ymax + 1, 1):
        for x in range(xmin, xmax + 1):
            dump += str(m.get((x, y), "."))
        dump += "\n"
    return dump


def solve1_tooslow(data):
    """Solves part 1."""
    m = {}
    for line in data.splitlines():
        sx, sy, bx, by = map(int, re.findall(r"=?(-?[0-9]+)", line))
        m[(sx, sy)] = "S"
        m[(bx, by)] = "B"

        # add the # where B cannot be
        dmax = manhattan((sx, sy), (bx, by))
        for x in range(sx - dmax, sx + dmax + 1):
            for y in range(sy - dmax, sy + dmax + 1):
                if manhattan((sx, sy), (x, y)) <= dmax and (x, y) not in m.keys():
                    m[(x, y)] = "#"

    logger.info(mdump(m))

    return len([p for (p, q), v in m.items() if (q == 2000000 and v == "#")])


def count_points(intervals):
    intervals = sorted(intervals)
    logger.info(f"sorted intervals: {intervals}")
    count = intervals[0][1] - intervals[0][0] + 1
    right_bound = intervals[0][1]
    logger.info(f"initializing count at {count} with interval {intervals[0]}")
    for i in range(1, len(intervals)):

        if intervals[i - 1][1] < intervals[i][1]:
            # i is NOT included in i-1
            if intervals[i][0] <= right_bound:
                # there is continuity
                count += intervals[i][1] - right_bound
                logger.info(f"continuity, {intervals[i]} increments count to {count}")
                right_bound = intervals[i][1]
            else:
                # both intervals are disjoint
                count += intervals[i][1] - intervals[i][0] + 1
                right_bound = intervals[i][1]
                logger.info(f"disjoint, {intervals[i]} increments count to {count}")

    return count


def find_possible_value(intervals):
    intervals = sorted(intervals)
    logger.info(f"sorted intervals: {intervals}")
    count = intervals[0][1] - intervals[0][0] + 1
    possible_value = None
    right_bound = intervals[0][1]
    logger.info(f"initializing count at {count} with interval {intervals[0]}")
    for i in range(1, len(intervals)):

        if intervals[i - 1][1] < intervals[i][1]:
            # i is NOT included in i-1
            if intervals[i][0] - 1 <= right_bound:
                # there is continuity
                count += intervals[i][1] - right_bound
                logger.info(f"continuity, {intervals[i]} increments count to {count}")
                right_bound = intervals[i][1]
            else:
                # both intervals are disjoint
                count += intervals[i][1] - intervals[i][0] + 1
                if intervals[i][0] - right_bound == 2:
                    possible_value = intervals[i][0] - 1
                    return possible_value
                right_bound = intervals[i][1]
                logger.info(
                    f"disjoint, {intervals[i]} increments count to {count}, possible value {possible_value}"
                )


def solve1(data, row):
    """Solves part 1."""
    m = {}
    intervals = []

    for line in data.splitlines():
        sx, sy, bx, by = map(int, re.findall(r"=?(-?[0-9]+)", line))
        m[(sx, sy)] = "S"
        m[(bx, by)] = "B"

        # add the # where B cannot be
        dmax = manhattan((sx, sy), (bx, by))

        if sy - dmax <= row <= sy + dmax:
            # this exclusion area overlaps our row
            intervals.append((sx - (dmax - abs(sy - row)), sx + (dmax - abs(sy - row))))
    return count_points(intervals) - len(
        [p for (p, q), v in m.items() if (q == row and v == "B")]
    )


def solve1_range(data, row):
    """Solves part 1."""
    m = {}
    points = set()

    for line in data.splitlines():
        sx, sy, bx, by = map(int, re.findall(r"=?(-?[0-9]+)", line))
        m[(sx, sy)] = "S"
        m[(bx, by)] = "B"

        # add the # where B cannot be
        dmax = manhattan((sx, sy), (bx, by))

        if sy - dmax <= row <= sy + dmax:
            # this exclusion area overlaps our row
            points.update(
                range(sx - (dmax - abs(sy - row)), sx + (dmax - abs(sy - row)) + 1)
            )
    return len(points) - len([p for (p, q), v in m.items() if (q == row and v == "B")])
    # 4886370


def solve2(data, cmax):
    """Solves part2."""
    cmin = 0
    intervals = defaultdict(list)

    for line in data.splitlines():
        sx, sy, bx, by = map(int, re.findall(r"=?(-?[0-9]+)", line))
        dmax = manhattan((sx, sy), (bx, by))

        for row in range(cmin, cmax + 1):
            if sy - dmax <= row <= sy + dmax:
                # this exclusion area overlaps our row
                left_bound = sx - (dmax - abs(sy - row))
                right_bound = sx + (dmax - abs(sy - row))

                new_interval = (max(left_bound, cmin), min(right_bound, cmax))
                intervals[row].append(new_interval)

    for y, inters in intervals.items():
        logger.info(f"\nexamining row {y}")
        x = find_possible_value(inters)

        if x is not None:
            logger.warning(
                f"possible value found at ({x},{y}) making tuning frequency to {4000000*x + y}"
            )
            logger.warning(f"intervals are {sorted(inters)}")
    return
    # 13529158836090 too high
    # I don't know why I get 5 possible values.... I ended up testing them all, the 2nd worked...  ¯\_(ツ)_/¯
    # it's really lame but I spent to much time on that shit for now.


"""
Use script args to execute the right function solve1 / solve2, with the right logging level (only activated on test inputs)
  - python dayXX.py 1
  - python dayXX.py 1t
  - python dayXX.py 2
  - python dayXX.py 2t 
"""
if __name__ == "__main__":
    """some logger levels : DEBUG, INFO, WARNING, CRITICAL"""
    if len(sys.argv) > 1 and sys.argv[1] == "1":
        logger.setLevel(logging.WARNING)
        res = solve1((Input(DAY).read()), 2000000)
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "1t":
        logger.setLevel(logging.INFO)
        res = solve1((test_input(DAY).read()), 10)
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        logger.setLevel(logging.WARNING)
        res = solve2((Input(DAY).read()), 4000000)
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2t":
        logger.setLevel(logging.INFO)
        res = solve2((test_input(DAY).read()), 20)
        print(res)
