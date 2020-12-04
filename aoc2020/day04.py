#!/usr/bin/env python3
from aoc_utilities import Input
import os
import re
import sys
# import itertools
import logging

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]



def input_parser(input):
    """
    hcl:#ae17e1 iyr:2013
    eyr:2024
    """
    keys = ["byr","iyr","eyr","hgt","hcl","ecl","pid","cid"]
    raw_passports = input.split('\n\n')
    dict_passports = []
    for raw_passport in raw_passports:
        dict_passport = {}
        for k in keys:
            pattern = k+":"+"(.+?)(?:\s|$)"   # the ? makes the match ungreedy (match as little text as possible)
            match = re.search(pattern, raw_passport, re.MULTILINE)
            if match:
                dict_passport[k] = match.group(1)
        dict_passports.append(dict_passport)
    return dict_passports
            

"""
PART1
"""



def solve1(input):
    """Solves part 1."""
    passports = input_parser(input)
    mandatory_keys = ["byr","iyr","eyr","hgt","hcl","ecl","pid"]
    valid_passport_count = 0
    for p in passports:
        logging.debug(p)
        if (len(p) == 8):
            valid_passport_count += 1
            logging.debug("valid")
        if (len(p) == 7 and ("cid" not in p.keys())):
            logging.debug("valid")
            valid_passport_count += 1
    return valid_passport_count





"""
PART 2
"""


def solve2(input):
    """Solves part2."""
    pass


"""
Use script args to execute the right function.
"""
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '1':
        res = solve1((Input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        res = solve2((Input(DAY).readlines()))
        print(res)
