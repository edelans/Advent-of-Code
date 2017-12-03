# Python 3.x

import re
import math

##################### PART 1 #########################

input1 = 325489


def spiral_mem(square):
    n = find_square_index(square)
    x = (n - 1) / 2
    y = 0
    #print('n is {}'.format(n))
    leg_length = n - 1
    #print('leg_length is {}'.format(leg_length))
    half_side = int(leg_length / 2)
    #print('half_side is {}'.format(half_side))
    if square < n**2 - 3*leg_length:
        #print('leg 1')
        center = (n**2 - 3*leg_length - half_side)
        #print('center is {}'.format(center))
        y = abs(square - center)
    elif square < n**2 - 2*leg_length:
        #print('leg 2')
        center = (n**2 - 2*leg_length - half_side)
        #print('center is {}'.format(center))
        y = abs(square - center)
    elif square < n**2 - 2*leg_length:
        #print('leg 3')
        center = (n**2 - 1*leg_length - half_side)
        #print('center is {}'.format(center))
        y = abs(square - center)
    else:
        #print('leg 4')
        center = (n**2 - 0*leg_length - half_side)
        #print('center is {}'.format(center))
        y = abs(square - center)
    #print('x is {} and y is {}'.format(x, y))
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


print(spiral_mem(input1))


##################### PART 2 #########################
