pattern = '.#./..#/###'.split('/')

def grouper(l, n):
    parts = len(l) // n
    for i in range(parts):
        for j in range(parts):
            yield i, j, tuple(c[j*n:(j+1)*n] for c in l[i*n:(i+1)*n])

def transpose(l):
    return list(''.join(c) for c in zip(*l))

def combos(l, flip=True):
    tl = transpose(l)
    yield l # original
    yield [r[::-1] for r in tl] # rotate clockwise 90
    yield [r[::-1] for r in l[::-1]] # rotate clockwise 180
    yield [r for r in tl[::-1]] # rotate clockwise 270
    if flip:
        fv = l[::-1] # flip vertically
        yield fv
        fh = [r[::-1] for r in l] # flip horizontally
        yield fh
        # rotate the flips
        yield from combos(fv, False)
        yield from combos(fh, False)

def enhance(p):
    size = 2 if len(p) % 2 == 0 else 3
    grouped = list(grouper(p, size))
    new_size = int(len(grouped)**0.5)*(size+1)
    enhanced = [[' '] * new_size for _ in range(new_size)]

    for r, c, rows in grouped:
        enh = rules[rows]
        for i, er in enumerate(enh):
            for j, val in enumerate(er):
                enhanced[r*len(enh) + i][c*len(enh) + j] = val

    enhanced = [''.join(r) for r in enhanced]
    return enhanced

rules = {}
with open('input_files/input21.txt') as f:
    for line in f:
        rule_in, rule_out = [r.split('/') for r in line.strip().split(' => ')]
        for comb in combos(rule_in):
            rules[tuple(comb)] = rule_out

for _ in range(5):
    pattern = enhance(pattern)

print("solution for part 1 is : {}".format(sum(r.count('#') for r in pattern)))


pattern = '.#./..#/###'.split('/')
for _ in range(18):
    pattern = enhance(pattern)

print("solution for part 2 is : {}".format(sum(r.count('#') for r in pattern)))
