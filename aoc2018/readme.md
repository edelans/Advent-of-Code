# why

just having fun sovling [advent of code](https://adventofcode.com/) puzzles one more year =)


# how to use

virtual env :

    mkvirtualenv --python=/usr/bin/python3 aoc2018

use this lib ?  https://github.com/wimglenn/advent-of-code-data

    pip install advent-of-code-data

use flake8 for linting

    pip install flake8

and atom linter :

    apm install linter-flake8



# Advent of code learnings (snippets)

## parsing


A common & simple strategy is to use use `str.split()` to divide the parent string in chunks, and then `re.findall()` to output the relevant data.  `re.findall(r'-?\d+', string)` is often used to look for numbers (it outputs a list).

Example for parsing this string :

    # [1518-10-21 00:00] Guard #2699 begins shift
    timestamp0, comment0 = shifts[i].split('] ')
    guard_ID = re.findall(r'-?\d+', comment0)[0]

Another method is to use a big regex :

    regex = r"^#(?P<id>\d+)\s@\s(?P<x>\d+),(?P<y>\d+):\s(?P<width>\d+)x(?P<height>\d+)"
    matches = re.search(regex, string)
    if matches:
            id = matches.group('id')



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
