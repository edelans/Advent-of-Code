#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input
import re

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def rule_parser(raw_rules):
    rules = {}
    pattern = re.compile(
        "(?P<name>.*): (?P<lower_bound_1>\d+)-(?P<upper_bound_1>\d+) or (?P<lower_bound_2>\d+)-(?P<upper_bound_2>\d+)"
    )
    iterator = pattern.finditer(raw_rules)
    for match in iterator:
        rules[match.group('name')] = [
            int(match.group('lower_bound_1')),
            int(match.group('upper_bound_1')),
            int(match.group('lower_bound_2')),
            int(match.group('upper_bound_2'))
        ]
    return rules


def is_valid(n, rule_bounds):
    return rule_bounds[0] <= n <= rule_bounds[1] or rule_bounds[
        2] <= n <= rule_bounds[3]


def parser(data):
    rules, your_ticket, nearby_tickets = data.split("\n\n")
    rules = rule_parser(rules)
    your_ticket = your_ticket.split("\n")[1]
    your_ticket = [int(x) for x in your_ticket.strip().split(",")]
    nearby_tickets = nearby_tickets.strip().split("\n")[1:]
    nearby_tickets = [[int(x) for x in line.strip().split(",")]
                      for line in nearby_tickets]
    return rules, your_ticket, nearby_tickets


def solve1(data):
    """Solves part 1."""
    rules, your_ticket, nearby_tickets = parser(data)
    res = 0
    for ticket in nearby_tickets:
        for n in ticket:
            if not any([is_valid(n, rule) for rule in rules.values()]):
                res += n
    return res


def solve2(data):
    """Solves part2."""
    pass


"""
Use script args to execute the right function.
"""
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '1':
        res = solve1((Input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '1t':
        res = solve1((test_input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        res = solve2((Input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '2t':
        res = solve2((test_input(DAY).read()))
        print(res)
