# Python 3.x

from collections import defaultdict

from aoc_utilities import *
DAY = 23

# Part 1

def get(registers, value):
    """
    we need this because in the instructions, the values can be alternatively
    - the value itself (when it's an integer),
    - or the value from the register
    """
    try:
        return int(value)
    except ValueError:
        # print("exception for : {}, will return {}".format(value, registers[value]))
        return registers[value]


def solve1(instructions):
    registers = defaultdict(int)
    i = 0
    mulcount = 0
    while i >= 0 and i < len(instructions):
        inst = instructions[i].split()
        op = inst[0]

        if op == 'set':
            registers[inst[1]] = get(registers, inst[2])
            i += 1
        elif op == 'sub':
            registers[inst[1]] -= get(registers, inst[2])
            i += 1
        elif op == 'mul':
            mulcount += 1
            registers[inst[1]] *= get(registers, inst[2])
            i += 1
        elif op == 'jnz':
            if get(registers, inst[1]) != 0:
                i += get(registers, inst[2])
            else:
                i += 1
        else:
            print("unrecognized operator : {}".format(op))
            return None
    return mulcount


res = solve1(Input(DAY).readlines())
print(res)



# def solve2(input):
#     pass
#
# res = solve2(parse_words(Input(DAY).readline()))
# print(res)
