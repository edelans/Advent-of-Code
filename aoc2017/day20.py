# Python 3.x

import re
from aoc_utilities import *
DAY = 20

# Part 1

teststr = """p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>"""


def solve1(lines):
    idmin = 1
    min = 10000
    for i, line in enumerate(lines):
        parts = line.split('a=<')
        if len(parts)>1:
            a = [int(x) for x in re.findall(r'\d+', parts[1])]
            metric = sum(map(abs, a))
            if metric < min:
                idmin = i
                min = metric
                print(min)
                print("new leader @ metric {} for line #{} : {}".format(metric, i, line))

            elif metric == min:
                print("equality @ metric {} for line #{} : {}".format(metric, i, line))
    return idmin


# assert(solve1(teststr.splitlines()) == 1)


res = solve1((Input(DAY).readlines()))
print(res)



# def solve2(input):
#     pass
#
# res = solve2(parse_words(Input(DAY).readline()))
# print(res)
