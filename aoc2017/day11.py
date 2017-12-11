from math import sqrt, ceil
import re


def Input(day):
    "Open this day's input file."
    filename = './input_files/input{}.txt'.format(day)
    return open(filename)


def parse_words(text):
    "All the words in text"
    return re.findall(r'\w+', text)


def get_distance_from_loc(loc):

    # for the horizontal component, it's only provided in sqrt(3)/2 increments from ne, nw, se, sw moves
    hor = abs(int(loc.real / (sqrt(3) / 2)))

    # we adjust the distance with N/S moves depending
    # on what is needed (out of reach for ne, nw, se, sw previous mouvements)
    if abs(loc.imag) <= hor / 2:
        # there were sufficient ne, nw, se, sw moves to account for the vertical component of final loc
        vert = 0
    else:
        # we have to add some N/S moves to reach final loc
        # max vertical distance travelled by hor [ne, nw, se, sw] moves is hor * 1 / 2 so we substract that part from loc vertical com
        vert = ceil(abs(loc.imag) - hor / 2)

    return hor + vert



def solve1(directions):
# location coorinates are complex type coordinates from the center of the current hex
# point (0, 0) @ the center of starting hex
# hex positionned on top of central hex has position (0, 1j)
    move = {
        "s": -1j,
        "sw": - sqrt(3) / 2 - 1 / 2 *1j,
        "nw": - sqrt(3) / 2 + 1 / 2 *1j,
        "n": 1j,
        "ne": sqrt(3) / 2 + 1 / 2 *1j,
        "se": sqrt(3) / 2 - 1 / 2 *1j
    }
    loc = 0
    max_d = 0
    for dir in directions:
        loc += move[dir]
        max_d = max(max_d, get_distance_from_loc(loc))
    return get_distance_from_loc(loc), max_d

assert solve1(["ne", "ne", "ne"])[0] == 3
assert solve1(["ne", "ne", "sw", "sw"])[0] == 0
assert solve1(["ne", "ne", "s", "s"])[0] == 2
assert solve1(["se", "sw", "se", "sw", "sw"])[0] == 3


print("the result for part 1 and 2 is {}".format(solve1(parse_words(Input(11).readline()))))
