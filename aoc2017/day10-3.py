input = """83,0,193,1,254,237,187,40,88,27,2,255,149,29,42,100"""



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

#part1
lengths = list(map(int,input.split(",")))
numbers = [x for x in range(0,256)]
curr_pos = 0
skip_size = 0

for l in lengths:
  numbers = reverse_sublist(numbers,curr_pos,curr_pos+l-1)
  curr_pos += (l+skip_size)
  skip_size += 1

print(numbers[0] * numbers[1])

#part2
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
print(final)
