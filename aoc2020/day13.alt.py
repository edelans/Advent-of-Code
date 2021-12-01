#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input
from functools import reduce
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


def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = int(prod / n_i)
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    print("{}, {}, {}".format(a, b, x1))
    return x1


def solve2(data):
    """Solves part2."""
    eta, buses = parser(data)
    a = []
    n = []
    for i, value in enumerate(buses):
        if value != "x":
            a.append(-i)
            n.append(value)
    print(a)
    print(n)
    # return chinese_remainder(n, a)
    return chinese_remainder(n, a)


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
