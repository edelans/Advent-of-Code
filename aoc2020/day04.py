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
some inspiration from reddit : 

with open(sys.argv[1]) as f:
        passports = [p.replace(' ', '\n') for p in f.read().split('\n\n')]
        passports = [dict(f.split(':') for f in p.split('\n')) for p in passports]

interesting 3 liner for part 1 : 

passports = open('../input.txt').read().split('\n\n')
fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
print(sum(1 if all(f in p for f in fields) else 0 for p in passports))

"""



"""
PART1
"""



def solve1(input):
    """Solves part 1."""
    passports = input_parser(input)
    valid_passport_count = 0
    for p in passports:
        if (len(p) == 8) or (len(p) == 7 and ("cid" not in p.keys())):
            valid_passport_count += 1
    return valid_passport_count


"""
PART 2
"""

def validate_passport(p):
    if (len(p) == 8) or (len(p) == 7 and ("cid" not in p.keys())):
        return (1920 <= int(p["byr"]) <= 2002
                and 2010 <= int(p["iyr"]) <= 2020
                and 2020 <= int(p["eyr"]) <= 2030
                and ((p["hgt"].endswith("cm") and 150 <= int(p["hgt"][:-2]) <= 193) or (p["hgt"].endswith("in") and 29 <= int(p["hgt"][:-2]) <= 76) )
                and ((p["hcl"].startswith("#") and len(p["hcl"])==7) and all(c in '0123456789abcdef' for c in p["hcl"][1:]))
                and p["ecl"] in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')
                and len(p["pid"]) == 9) 
    return False

def solve2(input):
    passports = input_parser(input)
    valid_p = 0
    for p in passports:
        if validate_passport(p):
            valid_p += 1
    return valid_p

#in one line : return sum(validate_passport(p) for p in passports)

"""
Use script args to execute the right function.
"""
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '1':
        res = solve1((Input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        res = solve2((Input(DAY).read()))
        print(res)
