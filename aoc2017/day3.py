# Python 3.x

import re
import math

from itertools import count

##################### PART 1 #########################

input1 = 325489


def spiral_mem(square):
    n = find_square_index(square)
    x = (n - 1) / 2
    y = 0
    leg_length = n - 1
    half_side = int(leg_length / 2)
    if square < n**2 - 3*leg_length:
        center = (n**2 - 3*leg_length - half_side)
        y = abs(square - center)
    elif square < n**2 - 2*leg_length:
        center = (n**2 - 2*leg_length - half_side)
        y = abs(square - center)
    elif square < n**2 - 2*leg_length:
        center = (n**2 - 1*leg_length - half_side)
        y = abs(square - center)
    else:
        center = (n**2 - 0*leg_length - half_side)
        y = abs(square - center)
    return int(x + y)


def find_square_index(square):
    n = math.ceil(math.sqrt(square)) # index of the square around the central 1

    if (n % 2) == 0:
        return n+1
    else:
        return n


assert spiral_mem(1) == 0
assert spiral_mem(12) == 3
assert spiral_mem(23) == 2
assert spiral_mem(1024) == 31


# print(spiral_mem(input1))


##################### PART 2 #########################


# compute sum of neighbors values
def sum_8_neighbors(points, pos):
    (i, j) = pos
    res = 0
    for k in range(i - 1, i + 2):
        for l in range(j - 1, j + 2):
            res += points.get((k, l), 0)
    return res



def neighbors8(point):
    "The eight neighbors (with diagonals)."
    x, y = point
    return ((x+1, y), (x-1, y), (x, y+1), (x, y-1),
            (x+1, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1))


def sum_spiral():
    """generator for the values of the spiral"""

    # store values of the spiral in a dict.
    # key is coordinates
    # set the spiral center to (0,0), with value of 1
    a, i, j = {(0,0): 1}, 0, 0

    # for each "square" that forms the spiral (defined by its odd side length)
    # not really a square though, as the left side exceeds by 1
    # see example below from S (start) to F (finish)
    #
    #   * < < < *
    #   v       ^
    #   v       ^
    #   v S > > *
    #   F
    #
    for s in count(1, 2):
        # for each directions possible on that path
        # right, up, left, down
        for (ds, di, dj) in [(0, 1, 0), (0, 0, 1), (1, -1, 0), (1, 0, -1)]:
            # for every atomic movement on that direction
            for _ in range(s + ds):
                i += di
                j += dj
                a[i, j] = sum(a.get((k, l), 0) for (k, l) in neighbors8((i, j)))
                yield a[i, j]


def part2(n):
    for x in sum_spiral():
        if x > n:
            return x

print(part2(input1))
