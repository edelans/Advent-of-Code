# why

Just having fun sovling [advent of code](https://adventofcode.com/) puzzles one more year =)


# how to use

virtual env :

    mkvirtualenv --python=/usr/bin/python3 aoc2020

use this lib ?  https://github.com/wimglenn/advent-of-code-data

    pip install advent-of-code-data

use flake8 for linting

    pip install flake8



# Advent of code learnings (snippets)

## parsing


A common & simple strategy is to use use `str.split()` to divide the parent string in chunks, and then `re.findall()` to output the relevant data.  `re.findall(r'-?\d+', string)` is often used to look for numbers (it outputs a list) of **strings** :

    lines = [[int(i) for i in re.findall(r'-?\d+', l)] for l in lines]

Other example for parsing this string :

    # [1518-10-21 00:00] Guard #2699 begins shift
    timestamp0, comment0 = shifts[i].split('] ')
    guard_ID = re.findall(r'-?\d+', comment0)[0]

Another method is to use a big regex :

    regex = r"^#(?P<id>\d+)\s@\s(?P<x>\d+),(?P<y>\d+):\s(?P<width>\d+)x(?P<height>\d+)"
    matches = re.search(regex, string)
    if matches:
            id = matches.group('id')

Other example below : 

	# this is the line to parse : 
	# 1-3 a: abcde
        
	# Strategy with split() :
        split = re.split('-|\s|: ', line)

        lower    = int(split[0])
        upper    = int(split[1])
        key      = split[2]
        password = split[3]

	# Strategy with regex ang groups : 
	regex = re.compile('(\d+)-(\d+)\s(\w):\s(\w+)')
        for group in regex.findall(line):
            lower = int(group[0])
            upper = int(group[1])
            letter = group[2]
            check_me = group[3]

	# or again :
	(min, max, letter, password) = re.findall(r'([0-9]+)-([0-9]+) ([a-z]): ([a-z]+)', line.strip())[0] 
	

## formating
use 'str.format()'

    print("new max sleeper #{} totaling {} times minute {} asleep".format(k, most_asleep_minute_count[1], most_asleep_minute_count[0]))


## dictionnary

### get the minimum or maximmum
get the key and value of the biggest value

    (key, value) = max(dict.items(), key=lambda i: i[1])   # use key=lambda i: i[0] to get max of keys

### default values

The getter has an handy second argument to use a default value if the key is not set yet :

    dict = {"a": 1, "b": 2}
    dict["c"] = dict.get("c", 0) + 1
    dict  #  {"a": 1, "b": 2, "c": 1}

There is also a default setter :

    for i in range(start, stop):
        guards.setdefault(current_guard, []).append(i)

There is also the defaultdict from the collections module : defaultdict is a subclass of the built-in dict class.

    from collections import Counter, defaultdict
    d = defaultdict(list)

When each key is encountered for the first time, it is not already in the mapping; so an entry is automatically created using the default_factory function (`list`) which returns an empty list.    

    from collections import Counter, defaultdict
    d = defaultdict(int)

When a letter is first encountered, it is missing from the mapping, so the default_factory function calls int() to supply a default count of zero.


### count the occurences of something (distribution)
-- day 3 and 4

[Counter](https://docs.python.org/3.6/library/collections.html#collections.Counter) is a class within the python "Collections" module. The underlying implementation is basically a dict where the keys are the values you pass to the counter, and the dict's values are the counts.

The update method on a counter works to update the count instead of overwrite the key's value, as it would in a normal dict.

    from collections import Counter, defaultdict
    guards = defaultdict(Counter)
    guards[guard_id].update([x for x in range(start_sleep, end_sleep)])

There is also a handy `.most_common(n)` method to return a list of the n most common elements and their counts from the most common to the least.

    Counter('abracadabra').most_common(3)
    [('a', 5), ('r', 2), ('b', 2)]


## lists

### slicing

	>>> hgt = "176cm"
	>>> hgt[:-2]
	176

### copying list to record its state


    a=['help', 'copyright', 'credits', 'license']
    b=a
    b.append('XYZ')
    b
    ['help', 'copyright', 'credits', 'license', 'XYZ']
    a
    ['help', 'copyright', 'credits', 'license', 'XYZ']

The assignment just copies the reference to the list, not the actual list, so both `a` and `b` refer to the same list after the assignment.

From [python official FAQ](https://docs.python.org/3/faq/programming.html#why-did-changing-list-y-also-change-list-x), there are 2 factors that produce this result :

1. Variables are simply names that refer to objects. Doing `y = x` doesn’t create a copy of the list – it creates a new variable y that refers to the same object `x` refers to. This means that there is only one object (the list), and both `x` and `y` refer to it.
2. Lists are mutable, which means that you can change their content.

If we instead assign an immutable object to `x`:


    >>> x = 5  # ints are immutable
    >>> y = x
    >>> x = x + 1  # 5 can't be mutated, we are creating a new object here
    >>> x
    6
    >>> y
    5

we can see that in this case x and y are not equal anymore. This is because integers are immutable, and when we do `x = x + 1` we are not mutating the int `5` by incrementing its value; instead, we are creating a new object (the int `6`) and assigning it to `x` (that is, changing which object `x` refers to). After this assignment we have two objects (the ints `6` and `5`) and two variables that refer to them (`x` now refers to `6` but `y` still refers to `5`).

Some operations (for example `y.append(10)` and `y.sort()`) mutate the object, whereas superficially similar operations (for example `y = y + [10]` and `sorted(y)`) create a new object. In general in Python (and in all cases in the standard library) a method that mutates an object will return `None` to help avoid getting the two types of operations confused. So if you mistakenly write `y.sort()` thinking it will give you a sorted copy of `y`, you’ll instead end up with `None`, which will likely cause your program to generate an easily diagnosed error.

If the list has only 1 level, you can use the builtin `list.copy()` method (available since python 3.3):

    new_list = old_list.copy()

Or you can use the built in `list()` function:

    new_list = list(old_list)

If the list contains objects and you want to copy them as well, use generic  `copy.deepcopy()`. The slowest and most memory-needing method, but sometimes unavoidable.

    from copy import deepcopy
    b = deepcopy(a)


### cycle through an iterable

    import itertools
    input = [0, 1]
    itertools.cycle(input)
    for delta in itertools.cycle(input):
        # infinite loop of 0 and 1

index of minimum element

    values.index(min(values))

### list comprehension + 'not in'

    [x for x in t if x not in s]

### get max x from list of coordinates

Say you have a list of `x, y` coordinates in a file :

    353, 177
    233, 332
    178, 231
    351, 221

use `zip` to get a "transverse" list :

    data = [map(int, i.split(', ')) for i in open('../input/6.in').readlines()]
    max_x = max(zip(*data)[0])


## deque

A "deque" is short for "double-ended queue," which Python implements internally as a doubly-linked list in C (also why it's generally faster than trying to make your own).

Whenever you're moving around a circle and adding/removing items as you go, a deque is oftentimes a good fit -- especially since it can do all these things in constant time by moving pointers around. See https://wiki.python.org/moin/TimeComplexity for a nice overview over the complexities of different operations on different Python data-structures

    >>> from collections import deque
    >>> circle = deque([1,2,3,4])

    >>> circle.rotate(1)
    >>> circle
    deque([4, 1, 2, 3])

    >>> circle.pop()
    3

    >>> circle.append(5)
    >>> circle
    deque([4, 1, 2, 5])
