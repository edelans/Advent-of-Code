import operator
import time
from itertools import product

OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "%": operator.mod,
    "^": operator.xor,
}


def parse_words(text: str) -> list[str]:
    "All the words in text"
    return text.split(",")


def Input(day):
    "Open this day's input file."
    filename = f"./input_files/input{day}.txt"
    return open(filename)


def test_input(day):
    "Open this day's test input file"
    filename = f"./input_files/input{day}.test.txt"
    return open(filename)


def neighbors_all(point: tuple[int, ...]) -> set[tuple[int, ...]]:
    """returns a set of all the neighboring positions of the input point
    whatever the number of dimentions
    ⚠️ Be careful as these positions can be outside your map ⚠️
    💡 Use a set intersection to remove out of bounds positions


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
    return set(product(*ranges)) - {point}


def neighbors_4(pos: tuple[int, int]) -> list[tuple[int, int]]:
    """
    returns positions of 4 neighbors : up, down, left, right
    ⚠️ Be careful as these positions can be outside your map ⚠️
    """
    return [
        (pos[0] - 1, pos[1]),
        (pos[0] + 1, pos[1]),
        (pos[0], pos[1] - 1),
        (pos[0], pos[1] + 1),
    ]


def mprint(maping: dict[tuple[int, int], str | int], min_half_size: int = 10) -> None:
    """
    Helper function to print a map
    when the map is a dictionary, with keys as tuples of coordinates (1,2)
    no need to have all the coordinates in the keys
    """
    xmax = max(max([int(i) for (i, j) in maping]), min_half_size)
    xmin = min(min([int(i) for (i, j) in maping]), -min_half_size)
    ymax = max(max([int(j) for (i, j) in maping]), min_half_size)
    ymin = min(min([int(j) for (i, j) in maping]), -min_half_size)
    for y in range(ymax, ymin - 1, -1):
        print("".join([str(maping.get((x, y), ".")) for x in range(xmin, xmax + 1)]))
    return


def sign(x: int | float) -> int:
    """
    note : sometimes it can be more useful to use math.copysign()
    see https://stackoverflow.com/a/1986718/1570104
    """
    return bool(x > 0) - bool(x < 0)


def timer_func(func):
    # This function shows the execution time of
    # the function object passed
    # (to be used as a wraper)
    def wrap_func(*args: object, **kwargs: object) -> object:
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        print(f"Function {func.__name__!r} executed in {(t2 - t1):.4f}s")
        return result

    return wrap_func
