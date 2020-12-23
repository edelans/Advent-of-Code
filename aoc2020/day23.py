#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
from aoc_utilities import Input, test_input
from collections import deque

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def move(circle, current_cup, min_cup=1, max_cup=9):

    while circle[0] != current_cup:
        circle.rotate(-1)

    circle.rotate(-1)
    c1 = circle.popleft()
    c2 = circle.popleft()
    c3 = circle.popleft()

    dest_cup = current_cup - 1
    while dest_cup not in circle:
        dest_cup -= 1
        if dest_cup < min_cup:
            dest_cup = max_cup

    while circle[0] != dest_cup:
        circle.rotate(+1)

    circle.rotate(-1)

    circle.extendleft([c3, c2, c1])

    while circle[0] != current_cup:
        circle.rotate(-1)

    circle.rotate(-1)

    current_cup = circle[0]
    return circle, current_cup


def solve1(data):
    """Solves part 1."""
    circle = deque([int(x) for x in data.strip()])
    # print(circle)
    current_cup = circle[0]

    for i in range(100):
        circle, current_cup = move(circle, current_cup)

    while circle[0] != 1:
        circle.rotate(1)

    circle.popleft()

    return ''.join([str(x) for x in circle])


def pprint(llist):
    l = [1]
    for _ in range(len(llist) - 1):
        l.append(llist[l[-1]])
    print(''.join(map(str, l)))
    return


def llist_move(llist, current_cup, min_cup=1, max_cup=9):
    """implement move with linked list"""
    next1 = llist[current_cup]
    next2 = llist[next1]
    next3 = llist[next2]

    # remove the next 3 cups :
    llist[current_cup] = llist[next3]

    # find destination cup
    dest_cup = current_cup - 1
    while dest_cup not in llist or dest_cup in [next1, next2, next3]:
        dest_cup -= 1
        if dest_cup < min_cup:
            dest_cup = max_cup

    # print("dest_cup is {}".format(dest_cup))
    # insert next 3 just after the destination cup
    llist[next3] = llist[dest_cup]
    llist[dest_cup] = next1

    # new current cup
    current_cup = llist[current_cup]
    # pprint(llist)
    return llist, current_cup


def solve2(data):
    """Solves part2."""
    input_max = 1000000
    move_count = 10000000
    # input_max = 9
    # move_count = 10
    input_seq = [int(x) for x in data.strip()]
    # print(input_seq)
    input_seq += list(range(10, input_max + 1))
    # print(input_seq)
    llist = {}
    for i in range(len(input_seq) - 1):
        llist[input_seq[i]] = input_seq[i + 1]
    llist[input_seq[-1]] = input_seq[0]

    current_cup = input_seq[0]
    # pprint(llist)
    for i in range(move_count):
        llist, current_cup = llist_move(llist, current_cup, 1, input_max)

    a = llist[1]
    b = llist[a]

    return a, b, a * b


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
