# Python 3.x

from aoc_utilities import Input
DAY = 19

# Part 1

teststr = """     |
     |  +--+
     A  |  C
 F---|----E|--+
     |  |  |  D
     +B-+  +--+
"""


def get_maze(input):
    maze = {}
    for i in range(0, len(input)):
        for j in range(0, len(input[i])):
            if input[i][j] != ' ':
                maze[(i,j)] = input[i][j]
    return maze


print(get_maze(teststr.split('\n')))

def solve1(input):
    pass


# assert(solve1(teststr.splitlines()) == XXXXX)


# res = solve1(parse_words(Input(DAY).readline()))
# print(res)



# def solve2(input):
#     pass
#
# res = solve2(parse_words(Input(DAY).readline()))
# print(res)
