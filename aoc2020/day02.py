#!/usr/bin/env python3
"""Template file to be used as boilerplate for each day puzzle."""
from aoc_utilities import Input
import os
import re
import sys
# import itertools

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


"""
PART1
"""


def solve1(input):
    valid_password_counter = 0
    for line in input:
        #1-3 a: abcde
        min_char, max_char, letter, password = filter(None, re.split('[- :]',line)) 
        min_char = int(min_char)
        max_char = int(max_char)
        if password.count(letter) >= min_char and password.count(letter) <= max_char:
            valid_password_counter +=1
    return valid_password_counter


"""
PART 2
"""


def solve2(input):
    """Solves part2."""
    valid_password_counter = 0
    for line in input:
        #1-3 a: abcde
        min_char, max_char, letter, password = filter(None, re.split('[- :]',line)) 
        min_char = int(min_char)
        max_char = int(max_char)
        if (password[min_char-1] == letter and  password[max_char-1] != letter) or (password[min_char-1] != letter and  password[max_char-1] == letter): 
            valid_password_counter +=1
    return valid_password_counter





"""
Use script args to execute the right function.
"""
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '1':
        res = solve1((Input(DAY).readlines()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        res = solve2((Input(DAY).readlines()))
        print(res)
