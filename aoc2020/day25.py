#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def loop(value, snum):
    res = value * snum
    res = res % 20201227
    return res


def get_handshake(snum, loop_size):
    """Transforms the subject number"""
    value = 1
    for _ in range(loop_size):
        value = loop(value, snum)
    return value


def solve1(data):
    """Solves part 1."""
    card_pkey, door_pkey = map(int, data.splitlines())
    card_secret_loop = None
    door_secret_loop = None

    handshake = loop(1, 7)
    nloop = 1
    while card_secret_loop == None or door_secret_loop == None:
        nloop += 1
        handshake = loop(handshake, 7)
        if handshake == card_pkey:
            card_secret_loop = nloop
        if handshake == door_pkey:
            door_secret_loop = nloop

    return card_secret_loop, door_secret_loop, get_handshake(
        card_pkey, door_secret_loop)


def solve2(data):
    """Solves part2."""
    pass


"""
Use script args to execute the right function.
"""
if __name__ == '__main__':
    assert get_handshake(7, 8) == 5764801
    assert get_handshake(7, 11) == 17807724
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
