# Python 3.x

import re

program_list = "abcdefghijklmnop"

def parse_words(text):
    "All the words in text"
    return text.split(',')

def Input(day):
    "Open this day's input file."
    filename = './input_files/input{}.txt'.format(day)
    return open(filename)


# Part 1


def spin(progs, X):
    return progs[len(progs) - X:] + progs[:len(progs) - X]


assert(spin([x for x in "abcde"], 3) == [x for x in "cdeab"])


def exchange(progs, A, B):
    tmp = progs[A]
    progs[A] = progs[B]
    progs[B] = tmp
    return progs


assert(exchange([x for x in "eabcd"], 3, 4) == [x for x in "eabdc"])


def partner(progs, A, B):
    return exchange(progs, progs.index(A), progs.index(B))


assert(partner([x for x in "eabdc"], 'e', 'b') == [x for x in "baedc"])


def solve1(operations):
    progs = [x for x in "abcdefghijklmnop"]

    for op in operations:
        # print(op)
        if op[0] == 's':
            progs = spin(progs, int(op[1:]))
        if op[0] == 'x':
            progs = exchange(progs, int(op[1:].split('/')[0]), int(op[1:].split('/')[1]))
        if op[0] == 'p':
            progs = partner(progs, op[1:].split('/')[0], op[1:].split('/')[1])
    return ''.join(progs)

res = solve1(parse_words(Input(16).readline()))
# testres = solve1(teststr)
print(res)
# assert solve1(teststr) == 8108

# print(solve1('ljoxqyyw'))


def solve2(input):
    pass


# res, colored_dict = solve2('ljoxqyyw')

# for i in range(0, 128):
#     line = []
#     for j in range(0, 128):
#         line.append(colored_dict.get((i,j), 0))
#     print(line)

# print(res)
