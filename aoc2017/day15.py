import re


def Input(day):
    "Open this day's input file."
    filename = './input_files/input{}.txt'.format(day)
    return open(filename)


def parse_words(text):
    "All the words in text"
    return re.findall(r'\w+', text)


def parse_numbers(text):
    "All the numbers in text"
    return [int(x) for x in re.findall(r'\d+', text)]




teststr = """generator A uses 65, while generator B uses 8921"""
inputstr = """Generator A starts with 783
Generator B starts with 325"""



# PART 1
#
# A initial_value 65 factor 16807
# B initial_value 8921 factor 48271

def generator(initial_value, factor, previous_value=None):
    if previous_value == None:
        previous_value = initial_value
    return (previous_value * factor) % 2147483647





def solve1(initA, initB):
    count = 0
    valueA = None
    valueB = None
    for _ in range(40000000):
        valueA = generator(initA, 16807, valueA)
        bvalueA = bin(valueA)[2:].zfill(32)
        valueB = generator(initB, 48271, valueB)
        bvalueB = bin(valueB)[2:].zfill(32)
        # print('\n')
        # print(bvalueA[16:])
        # print(bvalueB[16:])
        if bvalueA[16:] == bvalueB[16:]:
            count += 1
    return count


# print("The result for part 1 is : {}".format(solve1(parse_numbers(inputstr)[0], parse_numbers(inputstr)[1])))


# part 2


def solve2(initA, initB, iterations):
    count = 0
    valueA = None
    valueB = None
    for _ in range(iterations):
        valueA = generator(initA, 16807, valueA)
        while valueA % 4 != 0:
            valueA = generator(initA, 16807, valueA)
        bvalueA = bin(valueA)[2:].zfill(32)
        valueB = generator(initB, 48271, valueB)
        while valueB % 8 != 0:
            valueB = generator(initB, 48271, valueB)
        bvalueB = bin(valueB)[2:].zfill(32)
        # print('\n')
        # print(valueA)
        # print(valueB)
        # print('\n')
        # print(bvalueA[16:])
        # print(bvalueB[16:])
        if bvalueA[16:] == bvalueB[16:]:
            count += 1
    return count

# test = solve2(parse_numbers(teststr)[0], parse_numbers(teststr)[1], 5)
# print("The result for part 2 is : {}".format(test))


res = solve2(parse_numbers(inputstr)[0], parse_numbers(inputstr)[1], 5000000)
print("The result for part 2 is : {}".format(res))
