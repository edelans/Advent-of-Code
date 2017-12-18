# Python 3.x
from collections import defaultdict
from aoc_utilities import Input

DAY = 18

# Part 1

teststr = """set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2"""


def get(registers, value):
    """
    we need this because in the instructions, the values can be alternatively
    - the value itself (when it's an integer),
    - or the value from the register
    """
    try:
        return int(value)
    except ValueError:
        print("exception for : {}, will return {}".format(value, registers[value]))
        return registers[value]


def solve1(instructions):
    registers = defaultdict(int)
    i = 0
    while i >= 0 and i < len(instructions):
        print(i)
        print(instructions[i])
        inst = instructions[i].split()
        op = inst[0]
        if op == 'snd':
            registers['sound'] = get(registers, inst[1])
            i += 1
        elif op == 'set':
            registers[inst[1]] = get(registers, inst[2])
            i += 1
        elif op == 'add':
            registers[inst[1]] += get(registers, inst[2])
            i += 1
        elif op == 'mul':
            registers[inst[1]] *= get(registers, inst[2])
            i += 1
        elif op == 'mod':
            registers[inst[1]] %= get(registers, inst[2])
            i += 1
        elif op == 'rcv':
            if get(registers, inst[1]) != 0:
                registers['recovered'] = registers['sound']
                print("first sound recovered !")
                return registers['recovered']
            i += 1
        elif op == 'jgz':
            if get(registers, inst[1]) > 0:
                i += get(registers, inst[2])
            else:
                i += 1
        else:
            print("unrecognized operator : {}".format(op))
            return None


# assert(solve1(teststr.splitlines()) == XXXXX)


res = solve1(Input(DAY).readlines())
print(res)



# def solve2(input):
#     pass
#
# res = solve2(parse_words(Input(DAY).readline()))
# print(res)
