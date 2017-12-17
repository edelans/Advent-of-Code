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
    # Python evaluates the right hand side of an assignment first so you can swap variables like this (no need for temp var)
    progs[A], progs[B] = progs[B], progs[A]
    return progs


assert(exchange([x for x in "eabcd"], 3, 4) == [x for x in "eabdc"])


def partner(progs, A, B):
    return exchange(progs, progs.index(A), progs.index(B))


assert(partner([x for x in "eabdc"], 'e', 'b') == [x for x in "baedc"])


def solve1(alpha, operations):
    progs = [x for x in alpha]

    for op in operations:
        # print(op)
        if op[0] == 's':
            progs = spin(progs, int(op[1:]))
        if op[0] == 'x':
            progs = exchange(progs, int(op[1:].split('/')[0]), int(op[1:].split('/')[1]))
        if op[0] == 'p':
            progs = partner(progs, op[1:].split('/')[0], op[1:].split('/')[1])
    return ''.join(progs)


# res = solve1("abcdefghijklmnop", parse_words(Input(16).readline()))
# print(res)



def solve2(operations):
    progs = [x for x in "abcdefghijklmnop"]
    alpha = 'abcdefghijklmnop'
    alpha = solve1(alpha, operations)

    # let's find a cycle
    i = 1
    while alpha != 'abcdefghijklmnop':
        alpha = solve1(alpha, operations)
        i += 1

    j = 1000000000 % i

    for k in range(j):
        alpha = solve1(alpha, operations)

    return alpha

res = solve2(parse_words(Input(16).readline()))
print(res)
