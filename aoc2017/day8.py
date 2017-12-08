# Python 3.x

import re
import math

def Input(day):
    "Open this day's input file."
    filename = './input_files/input{}.txt'.format(day)
    return open(filename)



# PART 1

regex = r"^(?P<register>\w+)\s(?P<operation>inc|dec)\s(?P<value>-?\d+)\sif\s(?P<cond_register>\w+)\s(?P<cond_operation><|>|<=|>=|==|!=)\s(?P<cond_value>-?\d+)"


test_input = """b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""


def part1(lines):
    registers = {}

    for line in lines:
        matches = re.search(regex, line)
        if matches:
            condition = " ".join([str(registers.get(matches.group('cond_register'), 0)), matches.group('cond_operation'), matches.group('cond_value')])
            if eval(condition):
                if matches.group('operation') == 'inc':
                    registers[matches.group('register')] = registers.get(matches.group('register'), 0) + int(matches.group('value'))
                if matches.group('operation') == 'dec':
                    registers[matches.group('register')] = registers.get(matches.group('register'), 0) - int(matches.group('value'))


    return max(registers.values())


assert part1(test_input.split('\n')) == 1
# print(part1(Input(8).readlines()))



# part 2

def part2(lines):
    registers = {}
    max = 0

    for line in lines:
        matches = re.search(regex, line)
        if matches:
            condition = " ".join([str(registers.get(matches.group('cond_register'), 0)), matches.group('cond_operation'), matches.group('cond_value')])
            if eval(condition):
                if matches.group('operation') == 'inc':
                    registers[matches.group('register')] = registers.get(matches.group('register'), 0) + int(matches.group('value'))
                if matches.group('operation') == 'dec':
                    registers[matches.group('register')] = registers.get(matches.group('register'), 0) - int(matches.group('value'))
                if registers[matches.group('register')] > max:
                    max = registers[matches.group('register')]
    return max

assert part2(test_input.split('\n')) == 10
# print(part2(Input(8).readlines()))
