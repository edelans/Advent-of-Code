# Why

Just having fun sovling [advent of code](https://adventofcode.com/) puzzles one more year =)

# Goal of this year

Get to know Pycharm. 

# Repos to watch for instpiration

- https://github.com/mebeim/aoc/tree/master/2021

# Learnings

## Pycharm

- Navigate/select occurrences : 
  - command+G = go to next occurrence
  - command+ctrl+g = go to previous 
  - and ctrl+G = select next occurrence


## Python 

### String formatting 

Use f-strings : 
 
    print(f"most common bit for column n°{index} is 1")


### copying objects inside a loop

Problem : When you do `b = a` directly, `a` and `b` have the **same reference**, changing a is even as changing b.

- `list()`, 
- `[:]`, 
- `copy.copy()` 

are all shallow copy. They don't recursively make copies of the inner objects. It only makes a copy of the outermost list, while still referencing the inner lists from the previous variable, hence, when you mutate the inner lists, the change is reflected in both the original list and the shallow copy.If an object is nested, they are all **not suitable**. You need to use `copy.deepcopy()`.


See day4 to learn the hard way about object copy. 

    >>> a = [[1, 2, 3], [4, 5, 6]]
    >>> b = list(a)
    >>> a
    [[1, 2, 3], [4, 5, 6]]
    >>> b
    [[1, 2, 3], [4, 5, 6]]
    >>> a[0][1] = 10
    >>> a
    [[1, 10, 3], [4, 5, 6]]
    >>> b   # b changes too -> Not a deepcopy.
    [[1, 10, 3], [4, 5, 6]]

If you want 2 independant objects, use `deepcopy` : 

    >>> import copy
    >>> b = copy.deepcopy(a)
    >>> a
    [[1, 10, 3], [4, 5, 6]]
    >>> b
    [[1, 10, 3], [4, 5, 6]]
    >>> a[0][1] = 9
    >>> a
    [[1, 9, 3], [4, 5, 6]]
    >>> b    # b doesn't change -> Deep Copy
    [[1, 10, 3], [4, 5, 6]]


### How to fix performance problems ?

- if the computation takes too long, chances are you are not using the right data structure. 
- try to batch things (day06)


