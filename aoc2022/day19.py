#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
import logging
from aoc_utilities import Input, test_input
import re
from functools import lru_cache
import math

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
BLUEPRINTS = {}


def load_bp(data):
    global BLUEPRINTS
    BLUEPRINTS = {}
    for line in data.splitlines():
        # Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
        digits = list(map(int, re.findall(r"(\d+)", line)))
        BLUEPRINTS[digits[0]] = {
            "cost_ore_rbt": digits[1],
            "cost_clay_rbt": digits[2],
            "cost_obsidian_rbt__ore": digits[3],
            "cost_obsidian_rbt__clay": digits[4],
            "cost_geode_rbt__ore": digits[5],
            "cost_geode_rbt__obsidian": digits[6],
            "max_ore_cost": max(digits[1], digits[2], digits[3], digits[5]),
        }
    return


def quality_level(blueprint_id, t):
    maxg = max_geodes(t, blueprint_id, 0, 0, 0, 0, 1, 0, 0, 0)
    ql = blueprint_id * maxg
    print(
        f"blueprint {blueprint_id} can open {maxg} geodes in {t}min, reaching a quality level of {ql} "
    )
    return ql


@lru_cache(maxsize=None)
def max_geodes(
    T,
    blueprint,
    ore,
    clay,
    obsidian,
    geode,
    ore_robot,
    clay_robot,
    obsidian_robot,
    geode_robot,
):
    if T == 0:
        return geode
        # TODO : Make a cache for a state consisting of a tuple with the time, the materials, and the robots we have. If we reach a node that has fewer geodes broken than we cached for a similar node, we can stop at this node
        # TODO 2 : if the path reaches a point at which a geode machine can be produced every turn the search stops and trivially computes how many more geodes could be produced in the remaining time
        # TODO 3 : break if a very optimistic estimate of geode production (one new geode breaking robot per remaining turn) from the current point doesn't go over the maximum found so far.
        # Saving the state as (robots per resource & stack per resource) with an associated time, if the state is encountered again with more time left, the associated time is updated, if the state is encountered with less or the same time left you can prune.
    bp = BLUEPRINTS[blueprint]
    options = []

    # build a geode robot
    # Each geode robot costs 3 ore and 12 obsidian.
    # if I can build a geode robot, it's definitely the only option I should consider
    if ore >= bp["cost_geode_rbt__ore"] and obsidian >= bp["cost_geode_rbt__obsidian"]:
        options.append(
            (
                T - 1,
                blueprint,
                ore + ore_robot - bp["cost_geode_rbt__ore"],
                clay + clay_robot,
                obsidian + obsidian_robot - bp["cost_geode_rbt__obsidian"],
                geode + geode_robot,
                ore_robot,
                clay_robot,
                obsidian_robot,
                geode_robot + 1,
            )
        )

    else:
        # build an obsidian robot
        if obsidian_robot <= bp["cost_geode_rbt__obsidian"] and (
            ore >= bp["cost_obsidian_rbt__ore"]
            and clay >= bp["cost_obsidian_rbt__clay"]
        ):
            options.append(
                (
                    T - 1,
                    blueprint,
                    ore + ore_robot - bp["cost_obsidian_rbt__ore"],
                    clay + clay_robot - bp["cost_obsidian_rbt__clay"],
                    obsidian + obsidian_robot,
                    geode + geode_robot,
                    ore_robot,
                    clay_robot,
                    obsidian_robot + 1,
                    geode_robot,
                )
            )

        # do nothing
        # TODO : skip clock cycles until each new machine can be produced, interpolating the accumulated resources during the missing ticks (your final comment)
        # * there is no benefit to waiting a turn to buy a robot if you could buy it immediately. Therefore, if you choose not to buy anything, the next robot you buy must be one of the robots you *couldn't* already afford that turn.
        options.append(
            (
                T - 1,
                blueprint,
                ore + ore_robot,
                clay + clay_robot,
                obsidian + obsidian_robot,
                geode + geode_robot,
                ore_robot,
                clay_robot,
                obsidian_robot,
                geode_robot,
            )
        )

        # build a clay robot
        # Each clay robot costs 3 ore.
        # it's useless to produce in 1 step more than the max that you can consume in one step
        if ore >= bp["cost_clay_rbt"] and clay_robot <= bp["cost_obsidian_rbt__clay"]:
            options.append(
                (
                    T - 1,
                    blueprint,
                    ore + ore_robot - bp["cost_clay_rbt"],
                    clay + clay_robot,
                    obsidian + obsidian_robot,
                    geode + geode_robot,
                    ore_robot,
                    clay_robot + 1,
                    obsidian_robot,
                    geode_robot,
                )
            )
        # build a ore robot
        # it's useless to produce in 1 step more than the max that you can consume in one step
        if (ore >= bp["cost_ore_rbt"]) and ore_robot <= bp["max_ore_cost"]:
            options.append(
                (
                    T - 1,
                    blueprint,
                    ore + ore_robot - bp["cost_ore_rbt"],
                    clay + clay_robot,
                    obsidian + obsidian_robot,
                    geode + geode_robot,
                    ore_robot + 1,
                    clay_robot,
                    obsidian_robot,
                    geode_robot,
                )
            )

    # print(options)
    return max([max_geodes(*o) for o in options])


def solve1(data):
    """Solves part 1."""
    load_bp(data)
    return sum([quality_level(k, 24) for k in BLUEPRINTS.keys()])


def solve2(data):
    """Solves part2."""
    load_bp(data)
    res = 1
    for k in [1, 2, 3]:
        m = max_geodes(32, k, 0, 0, 0, 0, 1, 0, 0, 0)
        print(f"blueprint {k} can open {m} geodes")
        res *= m
    return res

    # 20979 too low


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
        res = solve1((test_input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "1":
        logger.setLevel(logging.WARNING)
        res = solve1((Input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2t":
        logger.setLevel(logging.INFO)
        res = solve2((test_input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        logger.setLevel(logging.WARNING)
        res = solve2((Input(DAY).read()))
        print(res)

"""
NOTES
- super elegant solution https://www.reddit.com/r/adventofcode/comments/zpihwi/comment/j0tvzgz/?utm_source=share&utm_medium=web2x&context=3
- another way to solve : use a solver, like z3 or cpmpy
"""
