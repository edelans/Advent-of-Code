import re


def Input(day):
    "Open this day's input file."
    filename = './input_files/input{}.txt'.format(day)
    return open(filename)


def parse_words(text):
    "All the words in text"
    return re.findall(r'\w+', text)


teststr = """0: 3
1: 2
4: 4
6: 4"""


def is_up(clock, depth):
    return int(clock % (2 * (depth - 1)) == 0)


def solve1(lines):
    firewall_depth = {}
    for line in lines:
        depth, scan_range = map(int, line.split(': '))
        firewall_depth[depth] = scan_range
    firewall_length = max(firewall_depth.keys()) + 1

    severity = 0
    for i in range(0, firewall_length):
        severity += is_up(i, firewall_depth.get(i, 0)) * i * firewall_depth.get(i, 0)
    return severity

assert solve1(teststr.splitlines()) == 24

print("The result for part 1 is : {}".format(solve1(Input(13).readlines())))


# part 2

#
#
# assert solve2(teststr.splitlines()) == 2
#
# print("The result for part 2 is : {}".format(solve2(Input(12).readlines())))
