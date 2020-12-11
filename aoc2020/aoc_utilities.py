import re


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


def neighbors_4(pos):
    """
    returns positions of 4 neighbors : up, down, left, right
    Be careful as these positions can be outside your map
    """
    return [(pos[0] - 1, pos[1]), (pos[0] + 1, pos[1]), (pos[0], pos[1] - 1),
            (pos[0], pos[1] + 1)]


def neighbors_8(pos):
    """
    Returns positions of 8 neighbors : up-left, left, down-left, up, down, up-right, right, down-right
    Be careful as these positions can be outside your map
   
    neighbors_8((2,2)) ->  [(1,1), (1,2), (1,3), (2,1), (2,3), (3,1), (3,2), (3,3)]

    """
    return [(pos[0] - 1, pos[1] - 1), (pos[0] - 1, pos[1]),
            (pos[0] - 1, pos[1] + 1), (pos[0], pos[1] - 1),
            (pos[0], pos[1] + 1), (pos[0] + 1, pos[1] - 1),
            (pos[0] + 1, pos[1]), (pos[0] + 1, pos[1] + 1)]
