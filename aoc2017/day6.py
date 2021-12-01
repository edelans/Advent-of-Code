# Python 3.x

import re
import operator

def Input(day):
    "Open this day's input file."
    filename = './input_files/input{}.txt'.format(day)
    return open(filename)


def parse_input(text):
    "All the words in text"
    return re.findall(r'\w+', text)



# PART 1

def cycles(allocation):
    hist = set()
    counter = 0

    while tuple(allocation) not in hist:
        counter += 1
        hist.add(tuple(allocation))
        # value and index of max :
        index, value = max(enumerate(allocation), key=operator.itemgetter(1))
        allocation[index] = 0
        for i in range(index + 1, index + value + 1):
            allocation[i % len(allocation)] += 1

    return counter, allocation


assert cycles([0, 2, 7, 0])[0] == 5

print(cycles([int(x) for x in parse_input(Input(6).read())]))
# count_steps([int(x) for x in Input(5)])


# part 2
# adapted return of function from part1
# from
#       return counter
# to
#       return counter, allocation
# to avoid rewriting new function


def part2(allocation):
    recurring_state = cycles(allocation)[1]
    return cycles(recurring_state)[0]

print(part2([int(x) for x in parse_input(Input(6).read())]))
