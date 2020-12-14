#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input
# import re
# import itertools

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def parser(data):
    eta = int(data[0])
    buses = [int(i) if i != "x" else "x" for i in data[1].split(",")]
    return (eta, buses)


def earliest_arrival_after_eta(eta, bus_id):
    return bus_id * (eta // bus_id) + bus_id


def solve1(data):
    """Solves part 1."""
    eta, buses = parser(data)
    buses = [b for b in buses if b != "x"]
    print(buses)
    earliest_arrivals = [earliest_arrival_after_eta(eta, b) for b in buses]
    print(earliest_arrivals)
    min_arrival = min(earliest_arrivals)
    return (min_arrival - eta) * buses[earliest_arrivals.index(min_arrival)]


def check_sequence(time, bus_constraints):
    for i, value in enumerate(bus_constraints):
        if value != "x":
            if (time + i) % value != 0:
                return False
    return True


def solve2(data):
    """Solves part2."""
    eta, buses = parser(data)
    k = 1
    while True:
        if check_sequence(k * buses[0], buses):
            return k * buses[0]
        k += 1


"""
Use script args to execute the right function.
"""
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '1':
        res = solve1((Input(DAY).readlines()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '1t':
        res = solve1((test_input(DAY).readlines()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        res = solve2((Input(DAY).readlines()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '2t':
        res = solve2((test_input(DAY).readlines()))
        print(res)
