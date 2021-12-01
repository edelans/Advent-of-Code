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
    shifts = sorted(input)
    guards = {}
    # guard_id: {
    #   "shift": [{start: }, {duration: }, ..]
    #   "total_time_asleep" : int
    # }
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

    for id in guards:
        guards[id]["minute_stats"] = {}
        for siesta in guards[id]['shift']:
            for i in range(int(siesta["start"].minute), int(siesta["start"].minute) + int(siesta["duration"].total_seconds()/60)):
                guards[id]["minute_stats"][i] = guards[id]["minute_stats"].get(i, 0) + 1

    max_asleep_minute = (0, 0)  # minute, count
    for k, v in guards.items():
        most_asleep_minute_count = max(v["minute_stats"].items(), key=lambda x: x[1])
        if most_asleep_minute_count[1] > max_asleep_minute[1]:
            print("new max sleeper #{} totaling {} times minute {} asleep".format(k, most_asleep_minute_count[1], most_asleep_minute_count[0]))
            alpha_sleeper_id = k
            max_asleep_minute = most_asleep_minute_count

    return int(alpha_sleeper_id) * max_asleep_minute[0]


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
