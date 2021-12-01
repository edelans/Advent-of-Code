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
    insertions = [0]
    cur = 0
    for i in range(1, 2017 + 1):
        insertions, cur = spinlock(insertions, cur, offset, i)
    return insertions[(cur + 1) % len(insertions)]


# res = solve1(382)
# print(res)


### PART 2


# def solve2(offset, total_insertions):
#     insertions = [0]
#     cur = 0
#
#     for i in range(1, total_insertions + 1):
#         if (i % 500000) == 0:
#             print(" i = {}, progress: {}% ".format(i, 100 * i / total_insertions))
#         val_after_0 = i
#         insertions, cur = spinlock(insertions, cur, offset, i)
#     return val_after_0
#
#
# res = solve2(382, 50000000)
# print(res)


# it's not necessary to keep the list in memory !!
def next0(step):
    pos = 0
    final = 0
    for i in range(1, 50000000 + 1):
        pos = (pos + step) % i + 1
        if pos == 1:
            final = i
    return(final)
print('Value after 0 in completed buffer is', next0(382))
