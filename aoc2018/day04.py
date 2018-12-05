#!/usr/bin/env python3
"""Template file to be used as boilerplate for each day puzzle."""
from aoc_utilities import Input
import aocd
import datetime
import re
import sys
# import itertools

# day must be 2 digit
DAY = '04'


"""
PART1
"""

"""
[1518-11-22 00:49] wakes up
[1518-05-18 00:01] Guard #1171 begins shift
[1518-11-20 00:28] wakes up
[1518-10-27 00:37] wakes up
[1518-08-14 00:39] falls asleep
[1518-09-08 00:51] falls asleep
[1518-07-27 00:57] wakes up
[1518-10-21 00:00] Guard #2699 begins shift
[1518-09-09 00:16] falls asleep
[1518-03-21 00:51] wakes up
[1518-05-21 23:59] Guard #863 begins shift
"""
"""
shifts = {} # id: [{day: }, {start: }, {end: }, {duration: }]

{day: {start: end: }, {duration: }, {id: } }

{
  "1518-03-21" : {
    "start": "1518-03-21 00:10"
    "end":"1518-03-21 00:51"
    "duration": 41
    "id": 863
  }
}

datetime.datetime.strptime('2012-07-22 16:19', '%Y-%m-%d %H:%M')
"""


# def solve1(input):
#     """Solves part 1."""
#     shifts = {}
#     for line in input:
#         timestamp, comment = line.split('] ')
#         timestamp = datetime.datetime.strptime(timestamp[1:], '%Y-%m-%d %H:%M')
#         d = datetime.timedelta(hours=1)
#         day = shift[(timestamp + d).strftime('%Y-%m-%d')]
#         if 'asleep' in comment:
#             shift[day]["start"] = timestamp
#         if 'wakes' in comment:
#             shift[day]["end"] = timestamp
#         if 'Guard' in comment:
#             shift[day]["id"] = timestamp
#         if 'end' in shift[day].values() and 'start' in shift[day].values():
#

def solve1(input):
    """Solves part 1."""
    shifts = sorted(input)
    guards = {}  # id: [{day: }, {start: }, {end: }, {duration: }]
    i = 0
    while i < len(shifts):
        timestamp0, comment0 = shifts[i].split('] ')
        guard_ID = re.findall(r'-?\d+', comment0)[0]
        while 'asleep' in shifts[i+1]:
            timestamp1, comment1 = shifts[i+1].split('] ')
            timestamp2, comment2 = shifts[i+2].split('] ')
            duration = datetime.datetime.strptime(timestamp2[1:], '%Y-%m-%d %H:%M') - datetime.datetime.strptime(timestamp1[1:], '%Y-%m-%d %H:%M')
            if guard_ID in guards:
                guards[guard_ID]["shift"] += [{"start": datetime.datetime.strptime(timestamp1[1:], '%Y-%m-%d %H:%M'), "duration": duration}]
            else:
                guards[guard_ID] = {"shift": [{"start": datetime.datetime.strptime(timestamp1[1:], '%Y-%m-%d %H:%M'), "duration": duration}], "total_time_asleep": 0}
            guards[guard_ID]["total_time_asleep"] += duration.total_seconds()
            i = i + 2
            if i+1 >= len(shifts):
                break
        i = i + 1

    max_sleep = 0
    for k, v in guards.items():
        # print(guards[guard])
        if int(v["total_time_asleep"]) > max_sleep:
            print("new max sleeper #{} totaling {} asleep".format(k, int(v["total_time_asleep"])))
            alpha_sleeper_id = k
            max_sleep = v["total_time_asleep"]

    minute_stats = {}
    for siesta in guards[alpha_sleeper_id]['shift']:
        for i in range(int(siesta["start"].minute), int(siesta["start"].minute) + int(siesta["duration"].total_seconds()/60)):
            minute_stats[i] = minute_stats.get(i, 0) + 1

    chosen_minute = max(minute_stats, key=minute_stats.get)

    return int(alpha_sleeper_id) * chosen_minute







"""
PART 2
"""


def solve2(input):
    """Solves part2."""

    # must parse "#id @ x,y: widthxheight" as in following example :
    # 1 @ 1,3: 4x4
    regex = r"^#(?P<id>\d+)\s@\s(?P<x>\d+),(?P<y>\d+):\s(?P<width>\d+)x(?P<height>\d+)"

    # Store the mapping in a dict. Key is coordinates (tuple), value is a list of ID claims.
    mapping = {}

    # store claim ids in a set so we can purge him from overlaping ids later
    id_set = set([])

    for claim in input:
        matches = re.search(regex, claim)
        if matches:
            id = matches.group('id')
            x, y = int(matches.group('x')), int(matches.group('y'))
            width, height = int(matches.group('width')), int(matches.group('height'))
            id_set.add(id)
            for i in range(x, x + width):
                for j in range(y, y + height):
                    mapping[(i, j)] = mapping.get((i, j), []) + [id]


    # part 2 really starts here

    overlaping_ids = set([l for k in mapping.values() if len(k) >= 2 for l in k])

    # Tip : remember that nested comprehension list follow the same order of the corresponding for loop
    # see https://spapas.github.io/2016/04/27/python-nested-list-comprehensions/
    # for k in mapping.values():
    #     if len(k) >= 2:
    #         for l in k:
    #             l

    for overlap_id in overlaping_ids:
        id_set.discard(overlap_id)

    return id_set.pop()


"""
Use script args to execute the right function.
"""
if __name__ == '__main__':
    if sys.argv[1] == '1':
        res = solve1((Input(DAY).readlines()))
        print(res)
        if len(sys.argv) == 3:
            if sys.argv[2] == 's':
                print("attempting to submit the response '{}' to part 1: \n\n".format(res))
                aocd.submit1(res)

    if sys.argv[1] == '2':
        res = solve2((Input(DAY).readlines()))
        print(res)
        if len(sys.argv) == 3:
            if sys.argv[2] == 's':
                print("attempting to submit the response '{}' to part 2: \n\n".format(res))
                aocd.submit2(res)
