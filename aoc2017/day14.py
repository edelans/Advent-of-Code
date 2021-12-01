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
    for i in range(0, 128):
        matrix.append([x for x in h_to_bin(hash(input + '-' + str(i)))])
    return matrix


def create_bit_dict(input):
    bit_dict = {}
    for i in range(0, 128):
        h = h_to_bin(hash(input + '-' + str(i)))
        for j in range(0, 128):
            bit_dict[(i, j)] = h[j]
    return bit_dict


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

# print(solve1('ljoxqyyw'))


def neighbors_4(pos):
    return [(pos[0]-1, pos[1]), (pos[0]+1, pos[1]), (pos[0], pos[1]-1), (pos[0], pos[1]+1)]


def solve2(input):
    bit_dict = {}

    for i in range(0, 128):
        h = h_to_bin(hash(input + '-' + str(i)))
        for j in range(0, 128):
            if int(h[j]) == 1:
                bit_dict[(i, j)] = h[j]

    colored_dict = {}
    positions_to_color = set(list(bit_dict.keys()))
    print("positions_to_color : {}".format(positions_to_color))
    print("init complete, starting coloration")

    color = 0
    while len(positions_to_color) > 0:
        print("updating color to : {}".format(color))
        color += 1
        print("startin coloration for color {}".format(color))
        points_to_color_in_that_color = set()
        points_to_color_in_that_color.add(positions_to_color.pop())

        while len(points_to_color_in_that_color) > 0:
            point_to_color = points_to_color_in_that_color.pop()

            # color the point
            print("coloring point {}".format(point_to_color))
            colored_dict[point_to_color] = color
            if point_to_color in positions_to_color:
                positions_to_color.remove(point_to_color)

            # look for neighbors to color
            for neighbor in neighbors_4(point_to_color):
                print("neighbor is {} has value {}".format(neighbor, bit_dict.get(neighbor, 0)))
                if int(bit_dict.get(neighbor, 0)) == 1:
                    if neighbor not in colored_dict:
                        print("neighbor is {} colorable".format(neighbor))
                        points_to_color_in_that_color.add(neighbor)
    return color, colored_dict


res, colored_dict = solve2('ljoxqyyw')

# for i in range(0, 128):
#     line = []
#     for j in range(0, 128):
#         line.append(colored_dict.get((i,j), 0))
#     print(line)

print(res)
