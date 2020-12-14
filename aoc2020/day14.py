#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input
from collections import defaultdict
# import re
# import itertools

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def apply_mask(value, mask):
    bvalue = format(value,
                    "#038b")  # '#' makes the format include the 0b prefix
    # 038 for the output to fit in 38 characters width, with padding of '0'
    # b for binary conversion

    s = ["0b"]
    for i, c in enumerate(mask):
        if c == "X":
            s.append(bvalue[2 + i])
        else:
            s.append(c)
    return int(''.join(s), 2)


def solve1(data):
    """Solves part 1."""
    mem = defaultdict(int)
    for line in data:
        if line[:2] == "ma":
            # update the mask
            mask = line[7:].strip()
        else:
            addr, value = line.split(" = ")
            value = int(value)
            addr = int(addr[4:-1])
            mem[addr] = apply_mask(value, mask)
    return sum(mem.values())


def xfill(xmask):
    if "X" not in xmask:
        return [xmask]
    else:
        return xfill(xmask.replace("X", "0", 1)) + xfill(
            xmask.replace("X", "1", 1))


def mask_addresses(addr, mask):
    """returns every possible addresses (as int) resulting from addr decoding with mask"""
    baddr = format(addr, "#038b")

    xmask = ["0b"]
    for i, c in enumerate(mask):
        if c == "0":
            xmask.append(baddr[i + 2])
        elif c == "1":
            xmask.append("1")
        else:
            xmask.append("X")
    xmask = ''.join(xmask)

    return list(map(lambda a: int(a, 2), xfill(xmask)))


def solve2(data):
    """Solves part2."""
    mem = defaultdict(int)
    for line in data:
        if line[:2] == "ma":
            # update the mask
            mask = line[7:].strip()
        else:
            addr, value = line.split(" = ")
            value = int(value)
            addr = int(addr[4:-1])

            for a in mask_addresses(addr, mask):
                mem[a] = value
    return sum(mem.values())


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
