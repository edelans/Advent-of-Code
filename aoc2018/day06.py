#!/usr/bin/env python3
"""Template file to be used as boilerplate for each day puzzle."""
from aoc_utilities import Input
import aocd
from collections import Counter
import sys
# import itertools


# day must be 2 digit
DAY = '06'


"""
PART1
"""


def man_dis(point1, point2):
    """Return manathan distance between 2 points."""
    return abs(point2[1] - point1[1]) + abs(point2[0] - point1[0])


def solve1(input):
    """Solves part 1."""
    mapping = {}
    cnt = 1
    for line in input:
        x, y = map(int, line.split(", "))
        mapping[(x, y)] = 'l' + str(cnt)
        cnt += 1

    min_x, k1 = min(mapping.items(), key=lambda i: i[0][0])[0]
    max_x, k2 = max(mapping.items(), key=lambda i: i[0][0])[0]
    k3, min_y = min(mapping.items(), key=lambda i: i[0][1])[0]
    k4, max_y = max(mapping.items(), key=lambda i: i[0][1])[0]

    infinite_ids = set()    # to keep track of inifite points
    points = {}             #
    points.update(mapping)  # create independant copy

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if (x, y) in mapping:
                pass
            else:
                # look for closest point
                min_dis = man_dis((min_x, min_y), (max_x, max_y))
                for (i, j) in points:
                    dis = man_dis((x, y), (i, j))
                    if dis < min_dis:
                        min_dis = dis
                        mapping[(x, y)] = points[(i, j)]
                    elif dis == min_dis:
                        mapping[(x, y)] = "."

                # record edge points as infinite infinite_ids
                if x == min_x or x == max_x or y == min_y or y == max_y:
                    infinite_ids.add(mapping[(x, y)])

    # print(mapping)
    print("Edge points are : {}".format(sorted(infinite_ids)))
    print([i for i in Counter(mapping.values()).most_common() if i[0] not in infinite_ids])
    return next(i[1] for i in Counter(mapping.values()).most_common() if i[0] not in infinite_ids)


"""
PART 2
"""


def solve2(input):
    """Solves part2."""
    mapping = {}
    cnt = 1
    for line in input:
        x, y = map(int, line.split(", "))
        mapping[(x, y)] = 'l' + str(cnt)
        cnt += 1

    min_x, k1 = min(mapping.items(), key=lambda i: i[0][0])[0]
    max_x, k2 = max(mapping.items(), key=lambda i: i[0][0])[0]
    k3, min_y = min(mapping.items(), key=lambda i: i[0][1])[0]
    k4, max_y = max(mapping.items(), key=lambda i: i[0][1])[0]

    safe_region_size = 0
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if sum(man_dis((x, y), p) for p in mapping.keys()) < 10000:
                safe_region_size += 1

    return safe_region_size


"""
Use script args to execute the right function.
"""
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '1':
        res = solve1((Input(DAY).readlines()))
        print(res)
        if len(sys.argv) == 3:
            if sys.argv[2] == 's':
                print("attempting to submit the response '{}' to part 1: \n\n".format(res))
                aocd.submit1(res)

    if len(sys.argv) > 1 and sys.argv[1] == '2':
        res = solve2((Input(DAY).readlines()))
        print(res)
        if len(sys.argv) == 3:
            if sys.argv[2] == 's':
                print("attempting to submit the response '{}' to part 2: \n\n".format(res))
                aocd.submit2(res)
