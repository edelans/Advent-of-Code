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


def distance_squared(p1, p2):
    """Return squared distance between two points in 3D space.
    Since we are not interested in the actual distance, just in the ordering,
    we calculate the squared distance which saves the math.sqrt() operation.
    """
    return sum((a - b) ** 2 for a, b in zip(p1, p2, strict=True))


def parse_boxes(data):
    """Parse boxes from input data."""
    return [tuple(map(int, line.split(","))) for line in data.splitlines()]


def merge_circuits(
    circuits: list[set],
    box_to_circuit: dict,
    box1: tuple,
    box2: tuple,
    connection_num: int,
) -> bool:
    """Merge circuits containing box1 and box2, or create new circuit.
    Returns True if boxes were merged/added, False if already in same circuit.
    """
    circuit1 = box_to_circuit.get(box1)
    circuit2 = box_to_circuit.get(box2)

    logger.info(f"\n#{connection_num} shortest connection is between {box1} and {box2}")

    def log_circuit_lengths():
        circuit_lengths = sorted((len(c) for c in circuits), reverse=True)
        logger.info(f"  - current circuits lengths are: {circuit_lengths}")

    if circuit1 is None and circuit2 is None:
        # Both boxes are new - create new circuit
        new_circuit = {box1, box2}
        circuits.append(new_circuit)
        box_to_circuit[box1] = new_circuit
        box_to_circuit[box2] = new_circuit
        logger.info(
            f"  - {box1} and {box2} are not part of any circuit, creating a new circuit!"
        )
        log_circuit_lengths()
        return True

    if circuit1 is None:
        # box1 is new, add it to circuit2
        circuit2.add(box1)
        box_to_circuit[box1] = circuit2
        logger.info(f"  - {box1} is not part of any circuit, adding it to {circuit2}")
        log_circuit_lengths()
        return True

    if circuit2 is None:
        # box2 is new, add it to circuit1
        circuit1.add(box2)
        box_to_circuit[box2] = circuit1
        logger.info(f"  - {box2} is not part of any circuit, adding it to {circuit1}")
        log_circuit_lengths()
        return True

    if circuit1 is circuit2:
        # Both boxes already in same circuit
        logger.info(
            f"  - {box1} and {box2} are already part of the same circuit -> no circuit change"
        )
        log_circuit_lengths()
        return False

    # Merge two existing circuits
    merged = circuit1 | circuit2
    circuits.remove(circuit1)
    circuits.remove(circuit2)
    circuits.append(merged)
    # Update all boxes in merged circuit to point to new circuit
    for box in merged:
        box_to_circuit[box] = merged
    logger.info(f"  - Merging two existing circuits: {circuit1} and {circuit2}")
    log_circuit_lengths()
    return True


@timer_func
def solve1(data, max_connections=1000):
    """Solves part 1."""
    boxes = parse_boxes(data)

    # Generate all pairs with their distances
    all_distances = [
        (box1, box2, distance_squared(box1, box2))
        for box1, box2 in combinations(boxes, 2)
    ]
    all_distances.sort(key=lambda x: x[2])

    circuits = []
    box_to_circuit = {}  # map each box to its circuit, leverages O(1) dictionary lookups

    for i, (box1, box2, _) in enumerate(all_distances[:max_connections], 1):
        merge_circuits(circuits, box_to_circuit, box1, box2, i)

    logger.info("Final circuits are:")
    for c in circuits:
        logger.info(f"  - {c}")

    circuit_lengths = sorted((len(c) for c in circuits), reverse=True)
    logger.warning(f"Total number of circuits is {len(circuits)}")
    logger.warning(f"3 largest circuit sizes are: {circuit_lengths[:3]}")

    return circuit_lengths[0] * circuit_lengths[1] * circuit_lengths[2]


@timer_func
def solve2(data):
    """Solves part2."""
    boxes = parse_boxes(data)
    total_boxes = len(boxes)

    # Generate all pairs with their distances
    all_distances = [
        (box1, box2, distance_squared(box1, box2))
        for box1, box2 in combinations(boxes, 2)
    ]
    all_distances.sort(key=lambda x: x[2])

    circuits = []
    box_to_circuit = {}

    for i, (box1, box2, _) in enumerate(all_distances, 1):
        merge_circuits(circuits, box_to_circuit, box1, box2, i)

        # Check if all boxes are connected (only need to check if we have one circuit)
        if len(circuits) == 1 and len(circuits[0]) == total_boxes:
            logger.info("All boxes are in circuits!")
            return box1[0] * box2[0]


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
