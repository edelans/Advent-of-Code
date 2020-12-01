import re


def parse_words(text):
    "All the words in text"
    return text.split(',')


def Input(day):
    "Open this day's input file."
    filename = './input_files/input{}.txt'.format(day)
    return open(filename)


def neighbors_4(pos):
    """
    returns positions of 4 neighbors : up, down, left, right
    Be careful as these positions can be outside your map
    """
    return [(pos[0] - 1, pos[1]), (pos[0] + 1, pos[1]), (pos[0], pos[1] - 1), (pos[0], pos[1] + 1)]
