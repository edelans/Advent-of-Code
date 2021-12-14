import re
from itertools import product 


def parse_words(text):
    "All the words in text"
    return text.split(',')


def Input(day):
    "Open this day's input file."
    filename = './input_files/input{}.txt'.format(day)
    return open(filename)


def test_input(day):
    "Open this day's test input file"
    filename = './input_files/input{}.test.txt'.format(day)
    return open(filename)


def neighbors_all(point):
    """returns a set of all the neighboring positions of the input point
    whatever the number of dimentions

    Examples : 
    >>> import aoc_utilities
    >>> aoc_utilities.neighbors_all((0,0))
    {(0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, 0), (1, -1), (1, 1)}
    >>> aoc_utilities.neighbors_all((0,0,0))
    {(0, 1, 1), (1, -1, -1), (1, 0, 0), (-1, 0, -1), (0, 0, 1), (0, -1, 1), (1, 0, 1), (-1, -1, -1), (-1, 1, -1), (0, -1, 0), (1, 1, 1), (-1, 1, 0), (1, 1, 0), (1, 1, -1), (-1, 1, 1), (-1, -1, 1), (1, -1, 0), (0, -1, -1), (-1, -1, 0), (0, 0, -1), (-1, 0, 1), (1, 0, -1), (1, -1, 1), (-1, 0, 0), (0, 1, 0), (0, 1, -1)}
    >>> len(aoc_utilities.neighbors_all((0,0)))
    8
    >>> len(aoc_utilities.neighbors_all((0,0,0)))
    26
    >>> len(aoc_utilities.neighbors_all((0,0,0,0)))
    80"""

    ranges = ((c - 1, c, c + 1) for c in point)
    return (set(product(*ranges)) - set([point]))


def neighbors_4(pos):
    """
    returns positions of 4 neighbors : up, down, left, right
    Be careful as these positions can be outside your map
    """
    return [(pos[0] - 1, pos[1]), (pos[0] + 1, pos[1]), (pos[0], pos[1] - 1),
            (pos[0], pos[1] + 1)]


def mprint(maping):
    """
    Helper function to print the map
    when the map is a dictionary, with keys as tuples of coordinates (1,2)
    no need to have all the coordinates in the keys
    """
    xmax = max([int(i) for (i,j) in maping.keys()])
    ymax = max([int(j) for (i,j) in maping.keys()])
    for y in range(ymax + 1):
        print(''.join([str(maping.get((x,y),".")) for x in range(xmax + 1)]))
    return