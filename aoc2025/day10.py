#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import heapq
import logging
import os
import random
import sys
from collections import deque

import z3

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
) -> tuple[list[bool], list[tuple[int, ...], ...], tuple[int, ...]]:
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


def stringify(light_diagram: list[bool]):
    return "".join(["#" if light else "." for light in light_diagram])


def min_button_presses(
    target_light_diagram: list[bool], buttons: tuple[tuple[int, ...], ...]
):
    min_presses = float("inf")
    # Try random combinations of button presses to reach target
    # Repeat max_iterations times
    # keep track of the minimum
    # max_iterations: scales with buttons since more buttons = larger search space
    # yes, this is a bit lame, totally unreliable, and super lazy
    # ... but was fun to try and tune to see it work :)
    max_iterations = 1000 * len(buttons)
    for _ in range(max_iterations):
        light_diagram = [False] * len(target_light_diagram)
        logger.info("Starting a new random search!")
        max_presses = (
            min(2 * len(buttons), min_presses - 1)
            if min_presses != float("inf")
            else 2 * len(buttons)
        )
        last_button = None
        for presses in range(1, max_presses + 1):
            if last_button is not None and len(buttons) > 1:
                # Pick a button different from the last one
                # because pushing the same button twice returns to the same light diagram
                available_buttons = [b for b in buttons if b != last_button]
                button = available_buttons[
                    random.randint(0, len(available_buttons) - 1)
                ]
            else:
                button = buttons[random.randint(0, len(buttons) - 1)]
            last_button = button
            logger.info(
                f"  - Light diagram is: {stringify(light_diagram)}, pushing button: {button}"
            )
            light_diagram = push_button(light_diagram, button)
            # logger.info(f" -> Light diagram is now: {stringify(light_diagram)}")
            if light_diagram == target_light_diagram:
                logger.info(
                    f"  - Light diagram is: {stringify(light_diagram)} and matches target!"
                )
                logger.info(f"  -> Found a combination with min presses: {presses}!")
                if presses < min_presses:
                    logger.info("This is a new minimum!")
                    min_presses = presses
                break
        logger.info(f"Couldn't find a new better combination in {max_presses} presses!")
    return min_presses if min_presses != float("inf") else -1


def min_button_presses_bfs(
    target_light_diagram: list[bool], buttons: tuple[tuple[int, ...], ...]
):
    target = tuple(target_light_diagram)
    start = tuple([False] * len(target_light_diagram))

    if start == target:
        return 0

    queue = deque([(start, 0)])
    visited = {start}

    while queue:
        state, presses = queue.popleft()

        for button in buttons:
            # Create new state by applying button
            new_state = list(state)
            for i in button:
                new_state[i] = not new_state[i]
            new_state = tuple(new_state)

            if new_state == target:
                return presses + 1

            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_state, presses + 1))

    return "No solution found"


@timer_func
def solve1(data):
    """Solves part 1."""
    machines = data.strip().splitlines()
    total_button_presses = 0
    for machine in machines:
        light_diagram, buttons, joltage_requirements = machine_parser(machine)
        total_button_presses += min_button_presses_bfs(light_diagram, buttons)
    return total_button_presses


def min_button_presses_joltage_mode(
    buttons: tuple[tuple[int, ...], ...], joltage_requirements: list[int]
):
    # we need to find the minimum number of button presses to reach the target joltage requirements
    # The counters are all initially set to zero.
    # When you push a button, each listed counter is increased by 1

    # This is a graph search problem

    # A* search with heuristic because BFS is too slow
    # A* explores promising paths first, which should reduce the search space.
    # The heuristic guides toward the target, and early pruning avoids generating invalid states.

    target = tuple(joltage_requirements)
    start = tuple([0] * len(joltage_requirements))

    if start == target:
        return 0

    # Heuristic: sum of remaining increments needed
    def heuristic(state):
        return sum(max(0, target[i] - state[i]) for i in range(len(target)))

    # Priority queue: (heuristic + presses, presses, state)
    # We use heuristic + presses as the priority to guide A* search
    queue = [(heuristic(start), 0, start)]
    processed = set()  # Track states we've already popped (processed)

    iterations = 0
    while queue:
        iterations += 1
        if iterations % 1000 == 0:
            logger.info(
                f"  Iteration {iterations}: Queue size: {len(queue)}, processed: {len(processed)}"
            )
        _, presses, state = heapq.heappop(queue)

        # Skip if we've already processed this state (can happen if added multiple times)
        if state in processed:
            continue
        processed.add(state)

        for button in buttons:
            # Pruning: skip if this button would increase any counter that's already at target
            if any(state[i] >= joltage_requirements[i] for i in button):
                continue

            # Create new state by applying button
            new_state = list(state)
            for i in button:
                new_state[i] += 1
            new_state = tuple(new_state)

            if new_state == target:
                return presses + 1

            # Pruning: skip if any counter exceeds its requirement
            if any(
                new_state[i] > joltage_requirements[i]
                for i in range(len(joltage_requirements))
            ):
                continue

            # Don't add if already processed (won't help since counters only increase)
            if new_state not in processed:
                h = heuristic(new_state)
                heapq.heappush(queue, (h + presses + 1, presses + 1, new_state))
                logger.debug(
                    f"Added new state: {new_state} to queue with heuristic {h} and priority {h + presses + 1}"
                )

    return -1


def push_button_joltage_mode(joltage: list[int], button_wiring: tuple[int, ...]):
    for i in button_wiring:
        joltage[i] += 1
    return joltage


def min_button_presses_joltage_mode_random(
    buttons: tuple[tuple[int, ...], ...], joltage_requirements: list[int]
):
    min_presses = float("inf")
    max_iterations = 10000 * len(buttons)
    for _ in range(max_iterations):
        joltage = [0] * len(joltage_requirements)
        logger.info("Starting a new random search!")
        max_presses = (
            min(2 * len(buttons), min_presses - 1)
            if min_presses != float("inf")
            else 2 * len(buttons)
        )
        for presses in range(1, max_presses + 1):
            button = buttons[random.randint(0, len(buttons) - 1)]
            logger.info(f"  - Joltage is: {joltage}, pushing button: {button}")
            joltage = push_button_joltage_mode(joltage, button)
            if joltage == joltage_requirements:
                logger.info(f"  - Joltage is: {stringify(joltage)} and matches target!")
                logger.info(f"  -> Found a combination with min presses: {presses}!")
                if presses < min_presses:
                    logger.info("This is a new minimum!")
                    min_presses = presses
                break
            elif any(
                joltage[i] > joltage_requirements[i]
                for i in range(len(joltage_requirements))
            ):
                logger.info(f"  - Joltage is: {joltage} and exceeds requirements!")
                break
        logger.info(f"Couldn't find a new better combination in {max_presses} presses!")
    return min_presses if min_presses != float("inf") else -1


def min_button_presses_joltage_mode_linear_equations(
    buttons: tuple[tuple[int, ...], ...], joltage_requirements: list[int]
):
    # changing approach again to use linear equations
    # There are m buttons and n joltage requirements
    # each button i B[i] is a vector of ones and zeros : B[i][1], B[i][2], ... B[i][n] with n being the size of joltage requirements
    # the joltage requirements is a vector of integers : J[1], J[2], ... J[n] with n being the size of joltage requirements

    # we need to find the minimum number of button presses to reach the target joltage requirements
    # the solution is a vector of integers : X[1], X[2], ... X[m]
    # X[i] is the number of times each button i is pressed

    # we can represent the problem as a system of linear equations:
    # B[1][1] * X[1] + B[1][2] * X[2] + B[1][3] * X[3] + ... + B[1][m] * X[m] = J[1]
    # B[2][1] * X[1] + B[2][2] * X[2] + B[2][3] * X[3] + ... + B[2][m] * X[m] = J[2]
    # ...
    # sum(B[i][j] * X[j] for j in range(m)) = J[i] for i in range(n)
    # ...
    # B[n][1] * X[1] + B[n][2] * X[2] + B[n][3] * X[3] + ... + B[n][m] * X[m] = J[n]

    # or in matrix form:
    # B * X = J
    # where B is a matrix of size n x m, X is a vector of size m, and J is a vector of size n

    # Integer Linear Programming approach:
    # Minimize: sum(X) = X[0] + X[1] + ... + X[m-1]
    # Subject to: B * X = J, X >= 0 (integers)
    n = len(joltage_requirements)
    m = len(buttons)

    # Variables: X[j] = number of times button j is pressed
    x = [z3.Int(f"x_{j}") for j in range(m)]
    opt = z3.Optimize()

    # Constraints: X >= 0
    for j in range(m):
        opt.add(x[j] >= 0)

    # Constraints: B * X = J
    # For each counter i, sum the presses of buttons that affect it
    for i in range(n):
        opt.add(
            sum(x[j] for j, button in enumerate(buttons) if i in button)
            == joltage_requirements[i]
        )

    # Objective: minimize sum(X)
    opt.minimize(z3.Sum(x))

    if opt.check() == z3.sat:
        model = opt.model()
        return sum(model[x[j]].as_long() for j in range(m))
    return -1


@timer_func
def solve2(data):
    """Solves part2."""
    machines = data.strip().splitlines()
    total_button_presses = 0
    for i, machine in enumerate(machines):
        light_diagram, buttons, joltage_requirements = machine_parser(machine)
        logger.critical(f"Solving machine {i}: {machine}")
        total_button_presses += min_button_presses_joltage_mode_linear_equations(
            buttons, joltage_requirements
        )
    return total_button_presses


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
            result = min_button_presses_bfs(target, buttons)
            assert result == expected, (
                f"Test case {i} failed: expected {expected}, got {result}"
            )

        res = solve1(test_input(DAY).read())
        expected = 7  # TODO: replace with expected value
        assert res == expected, f"Expected {expected}, got {res}"
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "1":
        logger.setLevel(logging.WARNING)
        res = solve1(Input(DAY).read())  # 489 too high
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2t":
        logger.setLevel(logging.INFO)
        # Unit tests for min_button_presses_joltage_mode
        test_cases = [
            (
                ((3,), (1, 3), (2,), (2, 3), (0, 2), (0, 1)),
                [3, 5, 4, 7],
                10,
            ),
            (
                ((0, 2, 3, 4), (2, 3), (0, 4), (0, 1, 2), (1, 2, 3, 4)),
                [7, 5, 12, 7, 2],
                12,
            ),
            (
                ((0, 1, 2, 3, 4), (0, 3, 4), (0, 1, 2, 4, 5), (1, 2)),
                [10, 11, 11, 5, 10, 5],
                11,
            ),
        ]
        for i, (buttons, joltage_requirements, expected) in enumerate(test_cases, 1):
            result = min_button_presses_joltage_mode(buttons, joltage_requirements)
            assert result == expected, (
                f"Test case {i} failed: expected {expected}, got {result}"
            )

        res = solve2(test_input(DAY).read())
        expected = 33  # TODO: replace with expected value
        assert res == expected, f"Expected {expected}, got {res}"
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        logger.setLevel(logging.DEBUG)
        res = solve2(Input(DAY).read())
        print(res)
