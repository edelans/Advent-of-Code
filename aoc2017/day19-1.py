# Python 3.x

from aoc_utilities import *
DAY = 19

# Part 1

teststr = """     |
     |  +--+
     A  |  C
 F---|----E|--+
     |  |  |  D
     +B-+  +--+
"""


def solve1(lines):
    road = {}
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j].strip():
                road[(j + 1j * i)] = lines[i][j]

    direction = 1j
    pos = min(road, key=lambda v: v.imag)
    path = []

    while pos in road:
        if road[pos] == '+':
            direction = next(d for d in [direction*1j, direction*-1j]
                             if pos+d in road and d != path[-1]-pos)
        path += [pos]
        pos += direction
    print(''.join(c for c in map(road.get, path) if c.isalpha()))
    print(len(path))
    return None


def orig(lines):
    road = {x+1j*y: v for y, line in enumerate(lines) for x, v in enumerate(line) if v.strip()}
    direction, pos, path = 1j, min(road, key=lambda v: v.imag), []
    while pos in road:
        if road[pos] == '+':
            direction = next(d for d in [direction*1j, direction*-1j]
                             if pos+d in road and d != path[-1]-pos)
        path += [pos]
        pos += direction
    print(''.join(c for c in map(road.get, path) if c.isalpha()))
    print(len(path))
    return None

# res = solve1(teststr.splitlines())
solve1(Input(DAY).readlines())
orig(Input(DAY).readlines())



# def solve2(input):
#     pass
#
# res = solve2(parse_words(Input(DAY).readline()))
# print(res)
