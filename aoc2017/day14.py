# Python 3.x


# helpers from day 10

def reverse_sublist(lst,start,end):
    sublist = []
    for i in range(start,end+1):
      sublist.append(lst[i % len(lst)])
    reverse = list(reversed(sublist))
    j=0
    for i in range(start,end+1):
      lst[i % len(lst)] = reverse[j]
      j+=1

    return lst


def hash(input):
    inp = input
    lengths = []
    for c in inp:
        lengths.append(ord(c))
    for i in [17, 31, 73, 47, 23]:
      lengths.append(i)
    numbers = [x for x in range(0,256)]
    curr_pos = 0
    skip_size = 0

    for _ in range(64):
      for l in lengths:
        numbers = reverse_sublist(numbers,curr_pos,curr_pos+l-1)
        curr_pos += (l+skip_size)
        skip_size += 1

    dense_list = []
    for i in range(16):
      for j in range(16):
        if j == 0:
          acc = numbers[(i*16) + j]
        else:
          acc = acc ^  numbers[(i*16) + j]
      dense_list.append(acc)

    final = ""
    for x in dense_list:
      h = hex(x)[2:]
      if len(h) == 1:
        h = "0"+h
      final += h
    return final

# print(hash(input))


# day 14

teststr = "flqrgnkx"


# Part 1


def h_to_bin(hash):
    # bin() Converts an integer number to a binary string prefixed with “0b”
    # zfill complete the string with zeros until the string length
    return bin(int(hash, 16))[2:].zfill(128)


def create_hash_matrix(input):
    matrix = []
    for i in range(0, 127):
        matrix.append([x for x in h_to_bin(hash(input + '-' + str(i)))])
    return matrix


# def solve1(input):
#     matrix = create_hash_matrix(input)
#     sum = 0
#     for bin_hash in matrix:
#         for bit in bin_hash:
#             sum += int(bit)
#     return sum
    # return sum(int(x) for y in matrix for x in y)


def solve1(input):
    sum = 0
    for i in range(0, 128):
        for bit in h_to_bin(hash(input + '-' + str(i))):
            sum += 1 if bit == '1' else 0
    return sum


# testres = solve1(teststr)
# print(testres)
# assert solve1(teststr) == 8108

print(solve1('ljoxqyyw'))
