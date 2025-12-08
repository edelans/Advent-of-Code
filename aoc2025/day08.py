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


def distance(p1, p2):
    """Return straight line squarred distance between two points in 3D space.
    Since we are not interested in the actual distance, just in the ordering,
    we calculate the squared distance which saves the math.sqrt() operation.
    """
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2


@timer_func
def solve1(data, max_connections=1000):
    """Solves part 1."""
    points = []
    for line in data.splitlines():
        points.append(tuple(int(i) for i in line.split(",")))

    all_distances = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            all_distances.append(
                tuple((points[i], points[j], distance(points[i], points[j])))
            )
    all_distances.sort(key=lambda x: x[2])

    circuits = []

    for i, d in enumerate(all_distances[0:max_connections]):
        logger.info(f"\n#{i + 1} shortest connection is between {d[0]} and {d[1]}")
        c0 = {d[0]}
        c1 = {d[1]}
        for c in circuits:
            if d[0] in c:
                c0 = c
                logger.info(f"  - {d[0]} is already in circuit {c}")
            if d[1] in c:
                c1 = c
                logger.info(f"  - {d[1]} is already in circuit {c}")
        if c0 == c1:
            logger.info(
                f"  - {d[0]} and {d[1]} are already part of the same circuit -> no circuit change"
            )
        else:
            if len(c0) == 1 and len(c1) > 1:
                logger.info(f"  - {d[0]} is not part of any circuit, adding it to {c1}")
                circuits.remove(c1)
                c1.add(d[0])
                circuits.append(c1)

            elif len(c1) == 1 and len(c0) > 1:
                logger.info(f"  - {d[1]} is not part of any circuit, adding it to {c0}")
                circuits.remove(c0)
                c0.add(d[1])
                circuits.append(c0)

            elif len(c0) == 1 and len(c1) == 1:
                logger.info(
                    f"  - {d[0]} and {d[1]} are not part of any circuit, creating a new circuit!"
                )
                circuits.append(c0.union(c1))
            elif len(c0) > 1 and len(c1) > 1:
                logger.info(
                    f"  - {d[0]} and {d[1]} are not part of any circuit, creating a new circuit!"
                )
                circuits.remove(c0)
                circuits.remove(c1)
                circuits.append(c0.union(c1))
        logger.info(
            f"  - current circuits lengths are: {sorted([len(c) for c in circuits], reverse=True)}"
        )

    logger.info("Final circuits are:")
    for c in circuits:
        logger.info(f"  - {c}")

    logger.warning(f"Total number of circuits is {len(circuits)}")
    circuit_lengths = sorted([len(c) for c in circuits], reverse=True)
    logger.warning(f"3 largest circuit sizes are: {circuit_lengths[0:3]}")
    return circuit_lengths[0] * circuit_lengths[1] * circuit_lengths[2]


@timer_func
def solve2(data):
    """Solves part2."""
    points = []
    for line in data.splitlines():
        points.append(tuple(int(i) for i in line.split(",")))

    all_distances = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            all_distances.append(
                tuple((points[i], points[j], distance(points[i], points[j])))
            )
    all_distances.sort(key=lambda x: x[2])

    circuits = []

    for i, d in enumerate(all_distances[0:]):
        logger.info(f"\n#{i + 1} shortest connection is between {d[0]} and {d[1]}")
        c0 = {d[0]}
        c1 = {d[1]}
        for c in circuits:
            if d[0] in c:
                c0 = c
                logger.info(f"  - {d[0]} is already in circuit {c}")
            if d[1] in c:
                c1 = c
                logger.info(f"  - {d[1]} is already in circuit {c}")
        if c0 == c1:
            logger.info(
                f"  - {d[0]} and {d[1]} are already part of the same circuit -> no circuit change"
            )
        else:
            if len(c0) == 1 and len(c1) > 1:
                logger.info(f"  - {d[0]} is not part of any circuit, adding it to {c1}")
                circuits.remove(c1)
                c1.add(d[0])
                circuits.append(c1)

            elif len(c1) == 1 and len(c0) > 1:
                logger.info(f"  - {d[1]} is not part of any circuit, adding it to {c0}")
                circuits.remove(c0)
                c0.add(d[1])
                circuits.append(c0)

            elif len(c0) == 1 and len(c1) == 1:
                logger.info(
                    f"  - {d[0]} and {d[1]} are not part of any circuit, creating a new circuit!"
                )
                circuits.append(c0.union(c1))
            elif len(c0) > 1 and len(c1) > 1:
                logger.info(
                    f"  - {d[0]} and {d[1]} are not part of any circuit, creating a new circuit!"
                )
                circuits.remove(c0)
                circuits.remove(c1)
                circuits.append(c0.union(c1))
        circuit_lengths = [len(c) for c in circuits]
        if sum(circuit_lengths) == len(points):
            logger.info("All points are in circuits!")
            return d[0][0] * d[1][0]

        logger.info(
            f"  - current circuits lengths are: {sorted([len(c) for c in circuits], reverse=True)}"
        )

    logger.info("Final circuits are:")
    for c in circuits:
        logger.info(f"  - {c}")

    logger.warning(f"Total number of circuits is {len(circuits)}")

    logger.warning(f"3 largest circuit sizes are: {circuit_lengths[0:3]}")
    return circuit_lengths[0] * circuit_lengths[1] * circuit_lengths[2]


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
        res = solve1(test_input(DAY).read(), 10)
        expected = 40  # TODO: replace with expected value
        assert res == expected, f"Expected {expected}, got {res}"
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "1":
        logger.setLevel(logging.WARNING)
        res = solve1(Input(DAY).read(), 1000)
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2t":
        logger.setLevel(logging.INFO)
        res = solve2(test_input(DAY).read())
        expected = 25272  # TODO: replace with expected value
        assert res == expected, f"Expected {expected}, got {res}"
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        logger.setLevel(logging.WARNING)
        res = solve2(Input(DAY).read())
        print(res)
