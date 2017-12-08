# Python 3.x

import re

def Input(day):
    "Open this day's input file."
    filename = './input_files/input{}.txt'.format(day)
    return open(filename)


def parse_input(text):
    "All the words in text"
    return re.findall(r'\w+', text)



# PART 1

regex = r"^([a-zA-Z]+)\s\((\d+)\)(\s-\>\s(.*))?"


test_input = """pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)"""


def find_root(lines):
    nodes = set()
    children = set()

    for line in lines:
        matches = re.search(regex, line)
        if matches:
            nodes.add(matches.group(1))
            if matches.group(4):
                for child in matches.group(4).split(", "):
                    children.add(child)

    # print("nodes are: {}".format(nodes))
    # print("children are: {}".format(children))
    # print("root is: {}".format(nodes - children))
    return (nodes - children).pop()


assert find_root(test_input.split('\n')) == "tknk"


print(find_root(Input(7).readlines()))
# ykpsek

# part 2


def build_objects(lines):
    children = {}
    parent = {}
    weight = {}
    for line in lines:
        matches = re.search(regex, line)
        if matches:
            node_name = matches.group(1)
            weight[node_name] = int(matches.group(2))
            if matches.group(4):
                node_children = matches.group(4).split(", ")
                children[node_name] = node_children
                for child in node_children:
                    parent[child] = node_name
    return children, parent, weight



def child_values(node, get_children, get_parent, get_weight):
    values = []

    for child in get_children[node]:
        if child in get_children.keys():
            sub_values = child_values(child, get_children, get_parent, get_weight)
            values.append(get_weight[child] + sum(sub_values))
        else:
            values.append(get_weight[child])

    if len(set(values)) != 1:
        print("unbalanced node is {} with weight {} and values {}".format(node, get_weight[node], values))
        for e in get_children[node]:
            print("child {} has weight {}".format(e, get_weight[e]))

    return values


def part2(lines, node):
    children, parent, weight = build_objects(lines)
    return child_values(node, children, parent, weight)

# part2(Input(7).readlines(), find_root(lines))
print(part2(Input(7).readlines(), "uduyfo"))
