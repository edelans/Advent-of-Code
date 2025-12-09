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
        print(f"\n⏱️ Function {func.__name__!r} executed in {(t2 - t1):.4f}s")
        return result

    return wrap_func


def point_in_polygon(point: tuple[int, int], polygon: list[tuple[int, int]]) -> bool:
    """Ray casting algorithm to check if point is inside polygon.
    Concept:
      - Cast a horizontal ray from the point to the right (positive x). Yes, only 1 direction is needed.
      - Count how many polygon edges it crosses:
        - If the count is odd, the point is inside
        - If the count is even, it's outside.
    """
    x, y = point
    n = len(polygon)
    inside = False  # will toggle as we count crossings

    # Iterate through edges of the polygon:
    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[
            i % n
        ]  # get next vertex, i % n will wrap around to the first vertex

        # First check if point is exactly on this edge (including horizontal edges)
        if p1y == p2y == y and min(p1x, p2x) <= x <= max(p1x, p2x):
            return True  # point is on horizontal edge, consider it inside
        elif p1x == p2x == x and min(p1y, p2y) <= y <= max(p1y, p2y):
            return True  # point is on vertical edge, consider it inside

        # Check if ray crosses this edge
        if (
            p1y != p2y  # skip horizontal edges, only vertical edges affect the result
            and min(p1y, p2y) < y <= max(p1y, p2y)  # The ray at y crosses this edge
            and x
            <= (y - p1y) * (p2x - p1x) / (p2y - p1y)
            + p1x  # The point is to the left of (or at) the intersection of the ray and the edge
        ):
            inside = not inside
        p1x, p1y = p2x, p2y  # move to the next edge

    return inside  # if crossing count is odd, the point is inside


def test_point_in_polygon():
    """Test point_in_polygon function with various test cases.

    polygon = [(2,1), (7,1), (7,4), (12,4), (12,2), (14,2), (14,6), (2,6)]

        |0   |5   |10  |15
    0  ....................
        ..######............
        ..#....#....###.....
        ..#....#....#.#.....
        ..#....######.#.....
    5  ..#...........#.....
        ..#############.....
        ....................
    """
    polygon = [(2, 1), (7, 1), (7, 4), (12, 4), (12, 2), (14, 2), (14, 6), (2, 6)]

    """
    X = (0,0) -> outside

        |0   |5   |10  |15
    0  X------------------>
        ..######............
        ..#....#....###.....
        ..#....#....#.#.....
        ..#....######.#.....
    5  ..#...........#.....
        ..#############.....
        ....................
    """
    assert not point_in_polygon((0, 0), polygon)

    """
    X = (0,3) -> outside

        |0   |5   |10  |15
    0  ....................
        ..######............
        ..#....#....###.....
        X->---->---->->------->
        ..#....######.#.....
    5  ..#...........#.....
        ..#############.....
        ....................
    """
    assert not point_in_polygon((0, 3), polygon)

    """
    X = (5,3) -> inside

        |0   |5   |10  |15
    0  ....................
        ..######............
        ..#....#....###.....
        ..#..X->---->->------->
        ..#....######.#.....
    5  ..#...........#.....
        ..#############.....
        ....................
    """
    assert point_in_polygon((5, 3), polygon)

    """
    X = (10,3) -> outside

        |0   |5   |10  |15
    0  ....................
        ..######............
        ..#....#....###.....
        ..#....#..X->->------->
        ..#....######.#.....
    5  ..#...........#.....
        ..#############.....
        ....................
    """
    assert not point_in_polygon((10, 3), polygon)

    """
    X = (13,3) -> inside

        |0   |5   |10  |15
    0  ....................
        ..######............
        ..#....#....###.....
        ..#....#....#X>------->
        ..#....######.#.....
    5  ..#...........#.....
        ..#############.....
        ....................
    """
    assert point_in_polygon((13, 3), polygon)

    """
    X = (17,3) -> outside

        |0   |5   |10  |15
    0  ....................
        ..######............
        ..#....#....###.....
        ..#....#....#.#..X--->
        ..#....######.#.....
    5  ..#...........#.....
        ..#############.....
        ....................
    """
    assert not point_in_polygon((17, 3), polygon)

    """
    X = (5,1) -> inside

        |0   |5   |10  |15
    0  ....................
        ..###X>>-------------->
        ..#....#....###.....
        ..#....#....#.#.....
        ..#....######.#.....
    5  ..#...........#.....
        ..#############.....
        ....................
    """
    assert point_in_polygon((5, 1), polygon)

    print("All point_in_polygon tests passed!")
