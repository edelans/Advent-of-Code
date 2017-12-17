# Python 3.x

from aoc_utilities import *
DAY = 1

# Part 1

teststr = """0: 3
1: 2
4: 4
6: 4"""


def spinlock(l, cur, offset, value_to_insert):
    """returns the new list with new value inserted"""
    position_to_insert = (cur + offset) % len(l) + 1
    l.insert(position_to_insert, value_to_insert)
    return l, position_to_insert


assert spinlock([0], 0, 3, 1) == ([0, 1], 1)
assert spinlock([0, 1], 1, 3, 2) == ([0, 2, 1], 1)
assert spinlock([0, 2, 1], 1, 3, 3) == ([0, 2, 3, 1], 2)


def solve1(offset):
    l = [0]
    cur = 0
    for i in range(1, 2017 + 1):
        l, cur = spinlock(l, cur, offset, i)
    return l[(cur + 1) % len(l)]


# assert(solve1(teststr.splitlines()) == XXXXX)


res = solve1(382)
print(res)


#
# def solve2(operations):
#     l[l.index(0) + 1]
#
# res = solve2(parse_words(Input(DAY).readline()))
# print(res)
