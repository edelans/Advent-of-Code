# Python 3.x

import re

# PART 1


def Input(day):
    "Open this day's input file."
    filename = './input_files/input{}.txt'.format(day)
    with open(filename) as f:
        lines = f.readlines()
    return lines

teststr = """0
3
0
1
-3"""


def parse_input(input):
    return [int(x) for x in re.findall(r'\-?\d+', input)]


def count_steps(l):
    counter = 0
    index = 0
    while index >= 0 and index < len(l):
        # print('index is {}, counter is {}, list is {}'.format(index, counter, str(l)))
        old_index = index
        index = index + l[index]
        l[old_index] += 1
        counter += 1

    # print('index is {}, counter is {}, list is {}'.format(index, counter, str(l)))
    print('Inscruction list exited after {} steps.'.format(counter))
    return counter


assert parse_input(teststr) == [0, 3, 0, 1, -3]
assert count_steps(parse_input(teststr)) == 5

# count_steps([int(x) for x in Input(5)])
