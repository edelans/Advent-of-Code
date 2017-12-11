def Input(day):
    "Open this day's input file."
    filename = './input_files/input{}.txt'.format(day)
    return open(filename)


def shift_list(l, cur, skip_size, length):

    print("\n\nnew iteration with list {}, cur {}, length {}".format(l, cur, length))
    print(l[:cur])
    print((l[cur:cur + length]))
    print(l[cur + length:])
    if cur + length < len(l):
        # no wrap
        new_list = l[:cur] + list(reversed(l[cur:cur + length])) + l[cur + length:]
    else:
        # wrap
        print("\nwrap")
        print(list(reversed(l[cur:length + 1])))
        print(l[((cur + length) % len(l)):cur])
        print(list(reversed(l[:length - ((cur + length) % len(l))])))
        new_list = list(reversed(l[cur:length + 1])) + l[((cur + length) % len(l)):cur] + list(reversed(l[:length - ((cur + length) % len(l))]))

    print(new_list)
    new_cur = (cur + skip_size + length) % len(l)
    print(new_cur)
    new_skip_size = skip_size + 1
    print(new_skip_size)
    return new_list, new_cur, new_skip_size

assert shift_list([0, 1, 2, 3, 4], 0, 0, 3) == ([2, 1, 0, 3, 4], 3, 1)
assert shift_list([2, 1, 0, 3, 4], 3, 1, 4) == ([4, 3, 0, 1, 2], 3, 2)
assert shift_list([4, 3, 0, 1, 2], 3, 2, 1) == ([4, 3, 0, 1, 2], 1, 3)
assert shift_list([4, 3, 0, 1, 2], 1, 3, 5) == ([3, 4, 2, 1, 0], 4, 4)


print(solve_part_2(Input(9).readline()))
