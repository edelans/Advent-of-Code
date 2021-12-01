#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
import numpy as np
import math
import re

from collections import defaultdict

from aoc_utilities import Input, test_input

from functools import reduce
import operator

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def parser(data):
    tiles = {}
    raw_tiles = data.strip().split("\n\n")
    for tile in raw_tiles:
        tile = tile.splitlines()
        tile_id = tile[0].split(' ')[1][:-1]
        tiles[tile_id] = [[char for char in line] for line in tile[1:]]
    return tiles


def borders(tile_content):
    transpose = list(zip(*tile_content))
    # as images can be rotated **or flipped**, we have to consider each border in each direction...
    return [
        tile_content[0], tile_content[0][::-1],
        list(transpose[-1]),
        list(transpose[-1][::-1]), tile_content[-1][::-1], tile_content[-1],
        list(transpose[0][::-1]),
        list(transpose[0])
    ]


def get_corners(tiles):
    """Solves part 1."""

    # border_count references how many times (values) each border line (keys)
    # is found in all the images
    border_count = {}
    for id, content in tiles.items():
        for b in borders(content):
            border_count[str(b)] = border_count.get(str(b), 0) + 1

    # tile_border_count references the sum of border_count for each of its borders
    # it gives an idea of how many adjacent tiles this tile have
    tile_border_count = {}
    for id, content in tiles.items():
        tile_border_count[id] = sum(
            [border_count[str(b)] for b in borders(content)])

    # corner tiles are the tiles which sum of border counts is the minimum
    corners = []
    for id in tiles.keys():
        if tile_border_count[id] == min(tile_border_count.values()):
            corners.append(id)

    return corners


def solve1(data):
    tiles = parser(data)
    corners = get_corners(tiles)
    return reduce(operator.mul, map(int, corners), 1)


def pprint(tile):
    for line in tile:
        print(''.join(line))
    return


def find_tile_below(next_tile_id, bottom_line, tiles):
    # we have identified the rigth tile
    # we need to put it in the right orientation (flip + rotate)
    tile = np.array(tiles[next_tile_id])
    r = 0
    while not np.array_equal(tile[0], bottom_line):
        if r < 4 or (4 < r < 10):
            tile = np.rot90(tile)
        elif r == 4:
            tile = np.flip(tile, 0)
        else:
            break
        r += 1
    return tile


def find_tile_right(next_tile_id, right_col, tiles):
    # we have identified the rigth tile
    # we need to put it in the right orientation (flip + rotate)
    tile = np.array(tiles[next_tile_id])
    r = 0
    while not np.array_equal(tile[:, 0], right_col):
        if r < 4 or (4 < r < 10):
            tile = np.rot90(tile)
        elif r == 4:
            tile = np.flip(tile, 0)
        else:
            break
        r += 1
    return tile


def border2tile(tiles):
    b2t = defaultdict(set)
    for tid, content in tiles.items():
        for b in borders(content):
            border_string = ''.join(b)
            b2t[border_string].add(tid)
    return b2t


def count_sea_monsters(img):
    pattern = ".{18}#.{1}" + "." * (len(img) -
                                    20) + "#.{4}##.{4}##.{4}###" + "." * (
                                        len(img) - 20) + ".#..#..#..#..#..#..."
    img_str = ''.join([''.join(line) for line in img])
    matches = re.findall(pattern, img_str)
    for m in matches:
        print(m)
        # print(m.start() % len(img) < (len(img) - 20))
    return len(matches)


def count_sea_monsters2(img):
    monster = np.array(\
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1],
        [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]]
        )

    img01 = np.where(img == "#", 1, img)
    img01 = np.where(img01 == ".", 0, img01)
    img01 = img01.astype(int)
    monstercount = 0
    for y in range(len(img) - 3):
        for x in range(len(img) - 20):
            if np.array_equal(np.multiply(monster, img01[y:y + 3, x:x + 20]),
                              monster):
                monstercount += 1
    return monstercount


def solve2(data):
    """Solves part2."""
    tiles = parser(data)

    # border_count references how many times (values) each border line (keys)
    # is found in all the images
    border_count = {}
    for id, content in tiles.items():
        for b in borders(content):
            border_count[str(b)] = border_count.get(str(b), 0) + 1

    # tile_border_count references the sum of border_count for each of its borders
    # it gives an idea of how many adjacent tiles this tile have
    tile_border_count = {}
    for id, content in tiles.items():
        tile_border_count[id] = sum(
            [border_count[str(b)] for b in borders(content)])

    # corner tiles are the tiles which sum of border counts is the minimum
    corners = []
    for id in tiles.keys():
        if tile_border_count[id] == min(tile_border_count.values()):
            corners.append(id)

    # we start with one random corner, and rotate it until we make it the
    # top left corner.
    b2t = border2tile(tiles)
    top_left = np.array(tiles[corners[0]])
    while not (len(b2t[''.join(top_left[0])]) == 1
               and len(b2t[''.join(top_left[:, 0])]) == 1):
        top_left = np.rot90(top_left)

    # We are then gonna build the first columns from top to bottom
    img_side_size = int(math.sqrt(len(tiles)))

    col1 = [top_left]
    col1_id = [corners[0]]
    for _ in range(img_side_size - 1):
        #print("looping")
        #print(list(col1[-1][-1]))
        #print(b2t[''.join(col1[-1][-1])])
        #print(col1_id)

        next_tile_id = (b2t[''.join(col1[-1][-1])] - set([col1_id[-1]])).pop()
        # print(b2t[''.join(col1[-1][-1])])
        tile = find_tile_below(next_tile_id, col1[-1][-1], tiles)
        col1.append(tile)
        col1_id.append(next_tile_id)

    # Now we are going to build each tile line
    img = []
    for i in range(img_side_size):
        # print("\n\n")
        # print("Starting a new line with: ")
        line = col1[i]
        # pprint(line)
        line_id = [col1_id[i]]
        for j in range(img_side_size - 1):
            # print(b2t[''.join(line[:, -1])] - set([line_id[-1]]))
            next_tile_id = (b2t[''.join(line[:, -1])] -
                            set([line_id[-1]])).pop()
            # print("last col is : {}".format(line[:, -1]))
            tile = find_tile_right(next_tile_id, line[:, -1], tiles)

            # print("Adding a new tile to the line : ")
            # pprint(tile)
            # delete the common column
            line = np.delete(line, -1, 1)
            tile = np.delete(tile, 0, 1)

            # horizontal stack the tile on the line
            line = np.hstack((line, tile))
            line_id.append(next_tile_id)

        # print("new line : ")
        # pprint(line)
        if i == 0:
            img = line
        else:
            # delete the common line
            img = np.delete(img, -1, 0)
            line = np.delete(line, 0, 0)

            # vertical stack the tile on the line
            img = np.vstack((img, line))

    # delete external borders :
    img = np.delete(img, 0, 0)
    img = np.delete(img, -1, 0)
    img = np.delete(img, 0, 1)
    img = np.delete(img, -1, 1)

    # print()
    # print("image : ")
    # pprint(img)

    r = 0
    sea_monsters = count_sea_monsters2(img)
    while sea_monsters == 0:
        if r < 4 or (4 < r < 10):
            print("rotate")
            img = np.rot90(img)
        elif r == 4:
            print("flip")
            img = np.flip(img, 0)
        else:
            break
        r += 1
        sea_monsters = count_sea_monsters2(img)
    print(f'found {sea_monsters} sea_monsters !!')
    sharps = np.count_nonzero(img.flatten() == "#")
    print(f'there are {sharps} sharps')
    return sharps - 15 * sea_monsters


"""
Use script args to execute the right function.
"""
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '1':
        res = solve1((Input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '1t':
        res = solve1((test_input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        res = solve2((Input(DAY).read()))
        print(res)
    if len(sys.argv) > 1 and sys.argv[1] == '2t':
        res = solve2((test_input(DAY).read()))
        print(res)
