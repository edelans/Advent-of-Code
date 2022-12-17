#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
import logging
from aoc_utilities import Input, test_input
import networkx as nx
from functools import lru_cache


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
TIME_LIMIT2 = 26


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
        print("nothing to gain anymore, cutting branch")
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
                    + (TIME_LIMIT - len(state["path"]) - 1)
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
    remaining_time = TIME_LIMIT2 - len(state["path"])

    closed_valves = [n for n in G.nodes() if G.nodes[n]["closed"]]
    remaining_rates = sorted([G.nodes[n]["rate"] for n in closed_valves], reverse=True)

    if remaining_rates[0] == 0:
        # all valves with positive flow rates are already open, nothing to gain anymore
        print("nothing to gain anymore, cutting branch")
        return state

    potential = 0
    for i, time in enumerate(range(remaining_time - 1, 0, -1)):
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
        if len(state["path"]) < TIME_LIMIT2:
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
                    + (TIME_LIMIT2 - len(state["path"]) - 1)
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
                    logger.warning(
                        f"CURRENT_MAX_EXPECTATION updated to {CURRENT_MAX_EXPECTATION}"
                    )
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
    initial_state = {
        "path": [],
        "path_e": [],
        "current_node": "AA",
        "current_node_e": "AA",
        "pressure_released": 0,
        "G": G,
    }
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
    if len(sys.argv) > 1 and sys.argv[1] == "1":
        print(f"TIME_LIMIT is {TIME_LIMIT}")
        logger.setLevel(logging.WARNING)
        res = solve1((Input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "1t":
        print(f"TIME_LIMIT is {TIME_LIMIT}")
        logger.setLevel(logging.WARNING)
        res = solve1((test_input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        print(f"TIME_LIMIT is {TIME_LIMIT2}")
        logger.setLevel(logging.WARNING)
        res = solve2((Input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == "2t":
        print(f"TIME_LIMIT is {TIME_LIMIT2}")
        logger.setLevel(logging.INFO)
        res = solve2((test_input(DAY).read()))
        print(res)


"""
Some inspiration:
- subreddit : https://www.reddit.com/r/adventofcode/comments/zn6k1l/2022_day_16_solutions/

- https://www.reddit.com/r/adventofcode/comments/zn6k1l/comment/j0g55m3/?utm_source=share&utm_medium=web2x&context=3
- solution with cahe : https://www.reddit.com/r/adventofcode/comments/zn6k1l/comment/j0fpyu4/?utm_source=share&utm_medium=web2x&context=3 / https://topaz.github.io/paste/#XQAAAQDtCAAAAAAAAAARiEJGPfQWNG6xo4rUnrU/FzgTXmJOWQF53DcS4Az2w2HhhD4+aO0E+caIqkLoXT1UvOavIg8dZNO6xHmGqs/aaew+IdftAbyyqS4jDaITL9h1gR8iukzsjQhUPcij97dbujSdUw2fOrwTDmVbiMKjbo9UM4BDxLDenIrQ+DrsPu5boZRHQcqt+rmQrf65TT19tFo3+aXZfKSgeDSt7P2qg4MPyOl0ez7YkeCAEDv6j1vZxqYhJylA2kXM+OU/sv9/vgeoau5yxgewLbjD+zoWA7gcbBAoDqpwbaGqJb4/mRc0m4yW9ncE5AQ5GfERRldNBVB5abpIHI6OwU6NgLfcye2vNYb5ol4l5lpBw+Btgi2qSyfXy/S1NSp2q6R+HgA4ocdYfPI+oIXeh8rv5LvsxS/+7zrag6/0ieNv9gH4flrGDnCNIcP7aaF84dY4hKgWQ4CgdD4SZ9Pz+8b7WjwzG+aulHFjpVahhrTOdMVodDuRcA9blNBQ5rn/5LxVNjudhh2JB63WIcvZC3zudC5rGkvWoX1T54eu0znk8XZxOzw9M0V1MszcBr7i4qEq772EitW802YBJVuETFe4Egn2d4y53W+XlXRx5y4a0q3h3vOq/PCL/AfkN7+wf5WBCCYK/YPBI9DMWb/QhgdSOfcAH2idIorA3dg4ZA+m8m/WZjKHM9CwZr1gOTeVZLri4CRohWz0bZdyRKmaIVVAi8D7KVx7UESWDft+vv/d4uHd4vaqJ4/rWXfaH00XXmm/ijx0+zlrJEyQ2RJZLSafN8jrd0qa2sSkwDam/Wl+89Uv53vduPlq/iwCY6VEOk/KxLkz9l87ipmai2tyB00Zbp8EATYXYOzWf6Ax5QaUkYOvkpu/65ic8B+djl6O507TGcWvE343t/3/+cGlbw==
- clear outlook of strategy here : https://www.reddit.com/r/adventofcode/comments/zn6k1l/comment/j0ftnif/?utm_source=share&utm_medium=web2x&context=3
- solution with cache : https://www.reddit.com/r/adventofcode/comments/zn6k1l/2022_day_16_solutions/
- solution with a solver : https://www.reddit.com/r/adventofcode/comments/zn6k1l/2022_day_16_solutions/
- this guy with his 2 one liners : https://github.com/kaathewise/aoc2022/blob/main/16.py
- compact and simple, pragmatic solution for part 1 : https://github.com/llimllib/personal_code/blob/master/misc/advent/2022/16/a.py
- compact powerful solution https://www.reddit.com/r/adventofcode/comments/zn6k1l/comment/j0glv1y/?utm_source=share&utm_medium=web2x&context=3 : https://topaz.github.io/paste/#XQAAAQB8CAAAAAAAAAA0m0pnuFI8c8huqZOxS6/JjBMFFgEh94Ggr4opHGMDLo6+34leTAsIOWgTplvWe0XBY5rUVYspwgtdF9f76UX4BG2hReyH6n3ej2eip/gSHXsdW6DxWiYO2hLfM3QOrzBSube6YzCeCco2uJGotP1JvYGdfihLYZ7P56/f5EFc1qlKKaQ5i5WXBEmtYRuzWcszUup20qOTqOv0ruFdO237U+QsLFs66Q/hzspaqIb1dIt8WkS86k7RdL3kmLrplaZVGNcvyYbZTOIQV177hFpUkcqZVewfDCqj419+/eK/6Kp4kgESUSQQ9ozF6jMuKfuWHdnaUX5F7e7O2506nSI/a9Q4DHemnsmgjCRTeC4xvHNuEfxQPMwfpnrFram7ndyDNLnECv41AgYX73pVNUvX9Tc3N3JGQQn3rZQKQJJv81e5SKaLBPg3urdXyTak//WydGMDSW6LARHnbdAn7FGO+U7HaP3k+7gQ/yJfIrvxsHy2L3+uIZSyMK3M5+M4PW0dyurF+9eEaM0tPp5UKz8ts0z8o62HO+Nw9AL3gk1ZkzLfTWcdYzAxbwetkQtAsh4jKjR5Txds1hGxBMzYflmRzb1UblUw5b9t7FFGLdI7Bp1kOpVy4Bb9LtC6EqahXL76Mwdw6wXItkvqy0fJGOTQ57Vy91Mt4h5F3Jj5cIGYr9jJgZ4+ISdCyvfwGqvQseQAyNIps0wPEM4VV7UQk/nL63SSPdYMRvMdQALVwK+GbBBNx5uaGGfOCtMAm/20riVyHXU0LvTCsbQzQ8dkRQM0Hy54NyaHgouWO1zTy39vzeUhiIlVQ0PRM4ossWd/dS0aiGN7k/UqDZtk6aKJF6ZQ44bQdYqXRPFFOgzd4wCJFxGvdqXLU0aqZW65Q2YVo6HkDpqO8faAUKEfZZAZH3379viWzrO0TcRy0DzG/Lw/jyTOKFRTSFnbl06PS2Pgzrd/PNstO31jDxBzAYT/7Z/o9SA0QEAOKz/JAXEKQ0KvvCI8/5tsfTvaPwabnNKU538Nx8fBpdq3FWIPzofDx2TLpUzUGQk2qGz0gVXebGGiy2Pt3EsGai47QeY9uZbls2fpF1kA8Qcs2wsSBo27YB1107kYmfLq8IGubXeLt0HDQxDogS12ObqTHMXEQGAyEDEppbdZabsb16HHWbptfynzP5PyUOdfSeOQVl5JLD1DDsxFvRJ+55MTb0cIMzoVsoBjFaQyA5OpYZNgZq1B//c/qKQ=
- recursion with cache : https://pastebin.com/jaHSDwJb
- bitwise operator : https://github.com/camaron-ai/adventofcode-2022/blob/4711b8ab7fcdf7272ce31bd4b86658abfeecc3cf/day16/main.py#L33
- funny one : the guy computes random paths... and it works :https://github.com/supermouette/adventofcode2022/blob/main/day16/p.py
- elegant strategy : https://www.reddit.com/r/adventofcode/comments/zn6k1l/comment/j0g8dq7/?utm_source=share&utm_medium=web2x&context=3
- https://www.reddit.com/r/adventofcode/comments/zn6k1l/comment/j0g6gs5/?utm_source=share&utm_medium=web2x&context=3
- DFS vs BFS : DFS uses less memory than BFS. It does not matter for correctness.
- straghtfwd strategy : https://www.reddit.com/r/adventofcode/comments/zn6k1l/comment/j0g5r48/?utm_source=share&utm_medium=web2x&context=3


learnings : 
- I need to think more in terms of search space, and see DFS / DFS 
- limit the arguments in recursive funtions to the maximum


"""
