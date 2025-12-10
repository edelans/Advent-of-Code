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


def machine_parser(
    machine: str,
) -> tuple[list[bool], list[tuple[int, ...], ...], tuple[int]]:
    # input is a string: aline from the input file, formatted as:
    # [light_diagram] (button1) (button2) ... (buttonN) {joltage_requirements}
    #
    # Test cases:
    # "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"" -> [False, True, True, False], ((3), (1, 3), (2,), (2, 3), (0, 2), (0, 1)), (3,5,4,7))
    # "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}"" -> [False, False, False, True, False], ((0, 2, 3, 4), (2, 3), (0, 4), (0, 1, 2), (1, 2, 3, 4)), (7,5,12,7,2)
    # "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"" -> [False, True, True, True, False, True], ((0, 1, 2, 3, 4), (0, 3, 4), (0, 1, 2, 4, 5), (1, 2)), (10,11,11,5,10,5)
    elements = machine.split(" ")
    light_diagram = [c == "#" for c in elements[0][1:-1]]  # Remove [ and ]
    joltage_requirements = tuple(map(int, elements[-1][1:-1].split(",")))

    buttons = []
    for button in elements[1:-1]:
        buttons.append(tuple(map(int, button[1:-1].split(","))))  # Remove ( and )
    return light_diagram, buttons, joltage_requirements


def push_button(light_diagram: list[bool], button_wiring: tuple[int, ...]):
    for i in button_wiring:
        light_diagram[i] = not light_diagram[i]
    return light_diagram


def min_button_presses(
    target_light_diagram: list[bool], buttons: tuple[tuple[int, ...], ...]
):
    pass


@timer_func
def solve1(data):
    """Solves part 1."""
    machines = data.strip().splitlines()
    total_button_presses = 0
    for machine in machines:
        light_diagram, buttons, joltage_requirements = machine_parser(machine)
        total_button_presses += min_button_presses(light_diagram, buttons)
    return total_button_presses


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
        push_result = push_button([True, False, False, False, False, False], (0, 3, 4))
        expected_push_result = [False, False, False, True, True, False]
        assert push_result == expected_push_result, (
            f"push_button failed: expected {expected_push_result}, got {push_result}"
        )

        # Unit tests for machine_parser
        parser_test_cases = [
            (
                "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}",
                (
                    [False, True, True, False],
                    [(3,), (1, 3), (2,), (2, 3), (0, 2), (0, 1)],
                    (3, 5, 4, 7),
                ),
            ),
            (
                "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}",
                (
                    [False, False, False, True, False],
                    [(0, 2, 3, 4), (2, 3), (0, 4), (0, 1, 2), (1, 2, 3, 4)],
                    (7, 5, 12, 7, 2),
                ),
            ),
            (
                "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}",
                (
                    [False, True, True, True, False, True],
                    [(0, 1, 2, 3, 4), (0, 3, 4), (0, 1, 2, 4, 5), (1, 2)],
                    (10, 11, 11, 5, 10, 5),
                ),
            ),
        ]
        for i, (input_str, expected) in enumerate(parser_test_cases, 1):
            result = machine_parser(input_str)
            assert result == expected, (
                f"machine_parser test case {i} failed: \nexpected: {expected} \nresult:{result}"
            )

        # Unit tests for min_button_presses
        test_cases = [
            (
                [False, True, True, False],
                ((3,), (1, 3), (2,), (2, 3), (0, 2), (0, 1)),
                2,
            ),
            (
                [False, False, False, True, False],
                ((0, 2, 3, 4), (2, 3), (0, 4), (0, 1, 2), (1, 2, 3, 4)),
                3,
            ),
            (
                [False, True, True, True, False, True],
                ((0, 1, 2, 3, 4), (0, 3, 4), (0, 1, 2, 4, 5), (1, 2)),
                2,
            ),
        ]
        for i, (target, buttons, expected) in enumerate(test_cases, 1):
            result = min_button_presses(target, buttons)
            assert result == expected, (
                f"Test case {i} failed: expected {expected}, got {result}"
            )

        res = solve1(test_input(DAY).read())
        expected = 7  # TODO: replace with expected value
        assert res == expected, f"Expected {expected}, got {res}"
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "1":
        logger.setLevel(logging.WARNING)
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
