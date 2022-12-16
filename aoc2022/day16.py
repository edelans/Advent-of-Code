#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
import logging
from aoc_utilities import Input, test_input
import networkx as nx


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

TIME_LIMIT = 30


def parser(data):
    G = nx.Graph()
    for line in data.splitlines():
        # Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
        line = line.replace(",", "").split(" ")
        adj_valves = line[9:]
        valve = line[1]
        rate = int(line[4].replace("rate=", "").replace(";", ""))
        G.add_node(valve, rate=rate, closed=True)
        for v in adj_valves:
            G.add_edge(valve, v)
    return G


CURRENT_MAX_EXPECTATION = -1


def max_path(state):
    global CURRENT_MAX_EXPECTATION
    G = state["G"]
    # logger.info(f"current path length is {len(state['path'])}")

    # pruning
    remaining_time = TIME_LIMIT - len(state["path"])

    closed_valves = [n for n in G.nodes() if G.nodes[n]["closed"]]
    remaining_rates = sorted([G.nodes[n]["rate"] for n in closed_valves], reverse=True)

    if remaining_rates[0] == 0:
        # all valves with positive flow rates are already open, nothing to gain anymore
        return state

    potential = 0
    for i, time in enumerate(range(remaining_time - 1, 0, -2)):
        potential += remaining_rates[i] * time
        if i + 2 > len(remaining_rates):
            break

    logger.info(
        f"potential is {potential}, expected final pressure is {state['pressure_released']} current max is {CURRENT_MAX_EXPECTATION} , remaining time {remaining_time}"
    )
    if state["pressure_released"] + potential < CURRENT_MAX_EXPECTATION:
        # drop this branch
        logger.info(
            f"droping path {state['path']}, cause potential {potential} is too low to catch up {CURRENT_MAX_EXPECTATION} with remaining time {remaining_time} while at pressure {state['pressure_released']}"
        )
        return {"path": [], "current_node": "AA", "pressure_released": 0, "G": G}

    else:
        if len(state["path"]) < TIME_LIMIT:
            actions = []
            if (
                G.nodes[state["current_node"]]["closed"]
                and G.nodes[state["current_node"]]["rate"] >= 1
            ):
                # open the valve
                newG = G.copy()
                newG.nodes[state["current_node"]]["closed"] = False
                final_pressure_expectation = (
                    state["pressure_released"]
                    + (30 - len(state["path"]) - 1)
                    * G.nodes[state["current_node"]]["rate"]
                )
                actions.append(
                    max_path(
                        {
                            "path": state["path"]
                            + [f"open valve {state['current_node']}"],
                            "current_node": state["current_node"],
                            "pressure_released": final_pressure_expectation,
                            "G": newG,
                        }
                    )
                )

                if final_pressure_expectation > CURRENT_MAX_EXPECTATION:
                    CURRENT_MAX_EXPECTATION = final_pressure_expectation
            for n in G.neighbors(state["current_node"]):
                # move to neighbor n
                actions.append(
                    max_path(
                        {
                            "path": state["path"] + [f"go to node {n}"],
                            "current_node": n,
                            "pressure_released": state["pressure_released"],
                            "G": G,
                        }
                    )
                )

            return max(actions, key=lambda a: a["pressure_released"])

        else:
            return state


def solve1(data):
    """Solves part 1."""
    G = parser(data)
    initial_state = {"path": [], "current_node": "AA", "pressure_released": 0, "G": G}
    return max_path(initial_state)


def max_path2(state):
    global CURRENT_MAX_EXPECTATION
    G = state["G"]
    # logger.info(f"current path length is {len(state['path'])}")

    # pruning
    remaining_time = TIME_LIMIT - len(state["path"])

    closed_valves = [n for n in G.nodes() if G.nodes[n]["closed"]]
    remaining_rates = sorted([G.nodes[n]["rate"] for n in closed_valves], reverse=True)

    if remaining_rates[0] == 0:
        # all valves with positive flow rates are already open, nothing to gain anymore
        return state

    potential = 0
    for i, time in enumerate(range(remaining_time - 1, 0, -2)):
        potential += remaining_rates[i] * time
        if i + 2 > len(remaining_rates):
            break

    logger.info(
        f"potential is {potential}, expected final pressure is {state['pressure_released']} current max is {CURRENT_MAX_EXPECTATION} , remaining time {remaining_time}"
    )
    if state["pressure_released"] + potential < CURRENT_MAX_EXPECTATION:
        # drop this branch
        logger.info(
            f"droping path {state['path']}, cause potential {potential} is too low to catch up {CURRENT_MAX_EXPECTATION} with remaining time {remaining_time} while at pressure {state['pressure_released']}"
        )
        return {"path": [], "current_node": "AA", "pressure_released": 0, "G": G}

    else:
        if len(state["path"]) < TIME_LIMIT:
            actions = []
            if (
                G.nodes[state["current_node"]]["closed"]
                and G.nodes[state["current_node"]]["rate"] >= 1
            ):
                # open the valve
                newG = G.copy()
                newG.nodes[state["current_node"]]["closed"] = False
                final_pressure_expectation = (
                    state["pressure_released"]
                    + (30 - len(state["path"]) - 1)
                    * G.nodes[state["current_node"]]["rate"]
                )
                actions.append(
                    max_path(
                        {
                            "path": state["path"]
                            + [f"open valve {state['current_node']}"],
                            "current_node": state["current_node"],
                            "pressure_released": final_pressure_expectation,
                            "G": newG,
                        }
                    )
                )

                if final_pressure_expectation > CURRENT_MAX_EXPECTATION:
                    CURRENT_MAX_EXPECTATION = final_pressure_expectation
            for n in G.neighbors(state["current_node"]):
                # move to neighbor n
                actions.append(
                    max_path(
                        {
                            "path": state["path"] + [f"go to node {n}"],
                            "current_node": n,
                            "pressure_released": state["pressure_released"],
                            "G": G,
                        }
                    )
                )

            return max(actions, key=lambda a: a["pressure_released"])

        else:
            return state


def solve2(data):
    """Solves part2."""
    pass
    G = parser(data)
    initial_state = {"path": [], "current_node": "AA", "pressure_released": 0, "G": G}
    return max_path2(initial_state)


"""
Use script args to execute the right function solve1 / solve2, with the right logging level (only activated on test inputs)
  - python dayXX.py 1
  - python dayXX.py 1t
  - python dayXX.py 2
  - python dayXX.py 2t 
"""
if __name__ == "__main__":
    """some logger levels : DEBUG, INFO, WARNING, CRITICAL"""
    print(f"TIME_LIMIT is {TIME_LIMIT}")
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
