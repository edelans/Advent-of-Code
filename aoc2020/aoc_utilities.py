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


def get_neighbors(point):
    """returns a set of all the neighboring positions of the input point
    whatever the number of dimentions

    Examples : 
    >>> import aoc_utilities
    >>> aoc_utilities.get_neighbors((0,0))
    {(0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, 0), (1, -1), (1, 1)}
    >>> aoc_utilities.get_neighbors((0,0,0))
    {(0, 1, 1), (1, -1, -1), (1, 0, 0), (-1, 0, -1), (0, 0, 1), (0, -1, 1), (1, 0, 1), (-1, -1, -1), (-1, 1, -1), (0, -1, 0), (1, 1, 1), (-1, 1, 0), (1, 1, 0), (1, 1, -1), (-1, 1, 1), (-1, -1, 1), (1, -1, 0), (0, -1, -1), (-1, -1, 0), (0, 0, -1), (-1, 0, 1), (1, 0, -1), (1, -1, 1), (-1, 0, 0), (0, 1, 0), (0, 1, -1)}
    >>> len(aoc_utilities.get_neighbors((0,0)))
    8
    >>> len(aoc_utilities.get_neighbors((0,0,0)))
    26
    >>> len(aoc_utilities.get_neighbors((0,0,0,0)))
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
