#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def bitsToInt(listOfBits):
    return int("".join(str(x) for x in listOfBits), 2)

def solve1(data):
    """Solves part 1."""
    lines = [list(line) for line in data.splitlines()]
    columns = [*zip(*lines)]

    gammaBits = []
    epsilonBits = []
    minimumToBeMostCommon = int(len(lines) / 2)

    for col in columns:
        if col.count("1") > minimumToBeMostCommon:
            gammaBits.append("1")
            epsilonBits.append("0")
        else:
            gammaBits.append("0")
            epsilonBits.append("1")

    return bitsToInt(gammaBits) * bitsToInt(epsilonBits)


def solve2(data):
    """Solves part2."""
    lines = [list(line) for line in data.splitlines()]

    candidatesForO2gen = lines
    candidatesForCO2scrub = lines

    for index in range(len(lines[0])):
        columns = [*zip(*candidatesForO2gen)]
        howMany1s = columns[index].count("1")
        howMany0s = len(columns[0]) - howMany1s

        if howMany1s > howMany0s:
            print(f"most common bit for column n°{index} is 1")
            candidatesForO2gen = [x for x in candidatesForO2gen if x[index]=="1"]
        elif howMany1s == howMany0s:
            print(f"for column n°{index}, there are as many 1s as 0s, keeping 1s")
            candidatesForO2gen = [x for x in candidatesForO2gen if x[index] == "1"]
        else:
            print(f"most common bit for column n°{index} is 0")
            candidatesForO2gen = [x for x in candidatesForO2gen if x[index]=="0"]
        if len(candidatesForO2gen) == 1:
            print(f"most common bit for column n°{index} is 0")
            break

    for index in range(len(lines[0])):
        columns = [*zip(*candidatesForCO2scrub)]
        howMany1s = columns[index].count("1")
        howMany0s = len(columns[0]) - howMany1s

        if howMany0s > howMany1s:
            print(f"least common bit for column n°{index} is 1")
            candidatesForCO2scrub = [x for x in candidatesForCO2scrub if x[index]=="1"]
        elif howMany1s == howMany0s:
            print(f"for column n°{index}, there are as many 1s as 0s, keeping 0s")
            candidatesForCO2scrub = [x for x in candidatesForCO2scrub if x[index] == "0"]
        else:
            print(f"least common bit for column n°{index} is 0")
            candidatesForCO2scrub = [x for x in candidatesForCO2scrub if x[index]=="0"]
        if len(candidatesForCO2scrub) == 1:
            break


    return bitsToInt(candidatesForO2gen[0]) * bitsToInt(candidatesForCO2scrub[0])

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
