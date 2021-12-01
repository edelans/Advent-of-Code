import re


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


# part 2


def build_dict(lines):
    children_dict = {}
    for line in lines:
        node, child = line.split('<->')
        children_dict[int(node)] = list(map(lambda x: int(x), child.split(',')))
    return children_dict


def find_group_members(children_dict, N_id):
    group0 = set()
    nodes_to_explore = set([N_id])

    while len(nodes_to_explore) > 0:
        node = nodes_to_explore.pop()
        group0.add(node)
        for i in children_dict[node]:
            nodes_to_explore.add(i)
        nodes_to_explore -= group0
    return group0


def solve2(lines):
    children_dict = build_dict(lines)
    nodes_to_group = set(children_dict.keys())
    group_nb = 0

    while len(nodes_to_group) > 0:
        group_nb += 1
        node = nodes_to_group.pop()
        nodes_to_group -= find_group_members(children_dict, node)

    return group_nb

assert solve2(teststr.splitlines()) == 2

print("The result for part 2 is : {}".format(solve2(Input(12).readlines())))
