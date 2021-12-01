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


def parse_firewall(lines):
    firewall = {}
    for line in lines:
        depth, scan_range = map(int, line.split(': '))
        firewall[depth] = scan_range
    return firewall


def is_caught(index, scan_range):
    return index % (2 * (scan_range - 1)) == 0


def solve1(lines):
    firewall = parse_firewall(lines)
    severity = 0
    for key, value in firewall.items():
        severity += key * value if is_caught(key, value) else 0
    return severity


assert solve1(teststr.splitlines()) == 24

# print("The result for part 1 is : {}".format(solve1(Input(13).readlines())))


# part 2


def does_trigger(firewall, delay):
    for key, value in firewall.items():
        if (key + delay) % (2 * (value - 1)) == 0:
            return True
    return False


def solve2(lines):
    firewall = parse_firewall(lines)
    delay = 0
    while does_trigger(firewall, delay):
        delay += 1
    return delay


# firewall = parse_firewall(Input(13).readlines())
assert solve2(teststr.splitlines()) == 10


# print("The result for part 2 is : {}".format(solve2(Input(13).readlines())))
