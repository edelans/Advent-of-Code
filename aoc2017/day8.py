# Python 3.x

import re
from collections import defaultdict


def Input(day):
    "Open this day's input file."
    filename = './input_files/input{}.txt'.format(day)
    return open(filename)


# PART 1


test_input = """b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""


def reg_max(lines):
    regex = r"^(?P<register>\w+)\s(?P<operation>inc|dec)\s(?P<value>-?\d+)\sif\s(?P<cond_register>\w+)\s(?P<cond_operation><|>|<=|>=|==|!=)\s(?P<cond_value>-?\d+)"
    registers = defaultdict(int)  # default value of int is 0
    maxv = 0

    for line in lines:
        matches = re.search(regex, line)
        if matches:
            condition = str(registers.get(matches.group('cond_register'), 0)) + " " + matches.group('cond_operation') + matches.group('cond_value')
            if eval(condition):
                if matches.group('operation') == 'inc':
                    registers[matches.group('register')] += int(matches.group('value'))
                if matches.group('operation') == 'dec':
                    registers[matches.group('register')] -= int(matches.group('value'))
                maxv = max(registers[matches.group('register')], maxv)
    return max(registers.values()), maxv


assert reg_max(test_input.split('\n'))[0] == 1
assert reg_max(test_input.split('\n'))[1] == 10

print(reg_max(Input(8).readlines()))



# part 2
#
# amended reg_max with lines containing maxv
