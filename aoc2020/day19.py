#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
import re
from aoc_utilities import Input, test_input

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def parser(data):
    raw_rules, messages = data.split("\n\n")

    raw_rules = raw_rules.splitlines()
    rules = {}
    for rule in raw_rules:
        n, r = rule.split(": ")
        rules[n] = [str(x) for x in r.replace('"', '').split(' ')]

    messages = messages.splitlines()

    return rules, messages


def get_regex_validation(rule, rules_dict):
    if not rule[0].isdigit():
        return rule[0]
    elif "|" in rule:
        i = rule.index("|")
        return "(" + get_regex_validation(
            rule[0:i], rules_dict) + "|" + get_regex_validation(
                rule[i + 1:], rules_dict) + ")"
    else:
        return ''.join(
            [get_regex_validation(rules_dict[k], rules_dict) for k in rule])


def get_regex_validation2(rule, rules_dict):
    # print(rule)
    # clean it like https://topaz.github.io/paste/#XQAAAQDzAgAAAAAAAAA0m0pnuFI8c/T1e9t0PMBti2mEcdYipHZYhCofRqVaOlj+UK7uG+kSryqDPRjN/l8dPcN5sLCzGZ2IRrIEpKPX8OHlryZm3WWNmcUuUvO5MG27hmtq8X4zRbvBtpEPKlMHFdtcTZIVFZVH/mcOHgz6cVQKD66YwKkfwHR5hMI8Xf9Q3Disai0qcjSa0hpmav4AmbNIa+zTHJy4YiimtZjV/FwJUhFByU8SuzHT3gp/F+QgIxwnLTHAkHbccyfEPjbX8y2XFx55gfiBuANOAypGeam+kvuAqUogjqySAHrbjun5HOHKHqyFpKtSkuOOMb2YitItlNVGFZ/5vD7Agq16CGS3wHAzEJJ0BsJ4r4atTu6e3o2subbpcVXvC/p+VY6sPezNGc/l0qb5sWUjkGbc3Go3AVqKHR25B9Jc1mhYn8iQjYZbyrqsaceoTwF+bMYQEAomMDZHgHPXzhHNEwF2aRg4iULmnKHgsrtZikwjn6NIz8ogidDYtVBHsRqQpTx1BUsqGVvDFFyP7EUPLVqAqseM9/aHQyno5uy58LL/1K+v4w==
    if not rule[0].isdigit():
        return rule[0]
    elif "|" in rule:
        i = rule.index("|")
        return "(" + get_regex_validation2(
            rule[0:i], rules_dict) + "|" + get_regex_validation2(
                rule[i + 1:], rules_dict) + ")"
    else:
        if rule == ['42']:
            print("rule 8")
            return ''.join(
                [get_regex_validation2(rules_dict['42'], rules_dict), "+"])
        elif rule == "42 31".split(' '):
            print("rule 11")
            return "(" + "|".join([
                get_regex_validation2(rules_dict['42'], rules_dict) * i +
                get_regex_validation2(rules_dict['31'], rules_dict) * i
                for i in range(1, 10)
            ]) + ")"

        else:
            print(rule)
            return ''.join([
                get_regex_validation2(rules_dict[k], rules_dict) for k in rule
            ])


def isvalid(message, pattern):
    if re.match(pattern, message):
        return (True)
    else:
        return (False)


def solve1(data):
    """Solves part 1."""
    rules, messages = parser(data)
    pattern = "^" + get_regex_validation(rules["0"], rules) + "$"
    print(pattern)
    return sum([isvalid(m, pattern) for m in messages])


def solve2(data):
    """Solves part2."""
    rules, messages = parser(data)
    pattern = "^" + get_regex_validation2(rules["0"], rules) + "$"
    print(pattern)
    return sum([isvalid(m, pattern) for m in messages])


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
