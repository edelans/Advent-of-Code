import re
from functools import reduce


def Input(day):
    "Open this day's input file."
    filename = './input_files/input{}.txt'.format(day)
    return open(filename)


def parse_words(text):
    "All the words in text"
    return re.findall(r'\w+', text)


def trace1(f):
    "Print a trace of the input and output of a function on one line."
    def traced_f(*args):
        result = f(*args)
        print('{}({}) = {}'.format(f.__name__, ', '.join(map(str, args)), result))
        return result
    return traced_f


teststr = """0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""


def solve1(lines):
    children_dict = {}
    for line in lines:
        node, child = line.split('<->')
        children_dict[int(node)] = list(map(lambda x: int(x), child.split(',')))

    # aborted idea
    # reduce((lambda acc, update: x * y), [1, 2, 3, 4], [])

    group0 = set()
    nodes_to_explore = set([0])

    while len(nodes_to_explore) > 0:
        node = nodes_to_explore.pop()
        group0.add(node)
        for i in children_dict[node]:
            nodes_to_explore.add(i)
        nodes_to_explore -= group0
    return len(group0)

assert solve1(teststr.splitlines()) == 6

print("The result for part 1 is : {}".format(solve1(Input(12).readlines())))
