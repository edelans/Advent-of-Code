# Python 3.x

from aoc_utilities import *
from collections import defaultdict
DAY = 22


# Part 1

teststr = """..#
#..
...
"""

def parse(lines):
    infected = set()
    side_length = len(lines)
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            x = int(j - (side_length - 1) / 2)
            y = int((side_length - 1) / 2 - i)
            if char == '#':
                infected.add(x + y * 1j)
    return infected


print(parse(teststr.splitlines()))


def solve1(lines, bursts):
    infected = parse(lines)
    infections = 0
    # virus carrier position
    vcp = 0
    # virus carrier direction
    vcd = 1j

    for _ in range(bursts):
        if vcp in infected:
            infected.remove(vcp)
            vcd *= -1j
        else:
            infected.add(vcp)
            infections += 1
            vcd *= 1j
        # move forward in direction vcd
        vcp += vcd
    #     print("infected nodes are : {} and vc position is {}".format(infected, vcp))
    # print("there have been {} infections !".format(infections))
    return infections

# assert(solve1(teststr.splitlines(), 70) == 41)
# assert(solve1(teststr.splitlines(), 10000) == 5587)
#
#
# res = solve1((Input(DAY).readlines()), 10000)
# print(res)


def solve2(lines, bursts):
    state = defaultdict(int)
    infections = 0
    # virus carrier position
    vcp = 0
    # virus carrier direction
    vcd = 1j
    # infection states :
    # 0 is clean
    # 1 is weakened
    # 2 is infected
    # 3 is flagged

    side_length = len(lines)
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            x = int(j - (side_length - 1) / 2)
            y = int((side_length - 1) / 2 - i)
            if char == '#':
                state[(x + y * 1j)] = 2

    for _ in range(bursts):

        # update direction vcd
        if vcp not in state or state[vcp] == 0:
            vcd *= 1j
        elif state[vcp] == 1:
            # keep same direction
            pass
        elif state[vcp] == 2:
            vcd *= -1j
        elif state[vcp] == 3:
            vcd *= -1

        # update state of current position vcp
        state[vcp] = (state[vcp] + 1) % 4
        if state[vcp] == 2:
            infections += 1

        # move forward in direction vcd
        vcp += vcd
    #     print("infected nodes are : {} and vc position is {}".format(infected, vcp))
    # print("there have been {} infections !".format(infections))
    return infections

res = solve2((Input(DAY).readlines()), 10000000)
print(res)
