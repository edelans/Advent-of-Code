#!/usr/bin/env python3
"""This script solves puzzles of https://adventofcode.com/"""

import os
import sys
import copy
from aoc_utilities import Input, test_input

# 2 digit day fetched from filename
DAY = os.path.basename(__file__)[3:5]


def parser(data):
    data = data.split("\n\n")
    draws = [int(x) for x in data[0].split(",")]
    boards = [boardParser(x) for x in data[1:]]
    return draws, boards

def boardParser(boardString):
    """
    takes a board as a string, return a board as a list of list
    
    14 33 79 61 44
    85 60 38 13 48
    51 34 11 19  7
    21 30 73  6 76
    41  4 65 18 91

    ->
    
    [[22, 13, 17, 11, 0], [8, 2, 23, 4, 24], [21, 9, 14, 16, 7], [6, 10, 3, 18, 5], [1, 12, 20, 15, 19]]
    """
    lines = boardString.splitlines()
    board = []
    for line in lines:
        boardline = []
        for n in line.split():
            boardline.append(int(n))
        board.append(boardline)
    return board


def sumUnmarked(board, thisBoardMarks):
    sum = 0
    for l in range(5):
        for c in range(5):
            if thisBoardMarks[l][c] == 0:
                sum += board[l][c]
    return sum



def solve1(data):
    """Solves part 1."""
    draws, boards = parser(data)
    boardMarks = [[[0 for i in range(5)] for j in range(5)] for k in range(len(boards))]
    print(draws)
    print(boardMarks)

    for d in draws:
        for index, board in enumerate(boards):
            for i in range(5):
                for j in range(5):
                    if board[i][j] == d:
                        print(f"mark for draw {d} on board {index} at line {i} and column {j}")
                        boardMarks[index][i][j] = 1

                        # test if we have a full line or full column
                        if (sum(boardMarks[index][i][k] for k in range(5)) == 5) or (sum(boardMarks[index][k][j] for k in range(5)) == 5):
                            return sumUnmarked(board, boardMarks[index]) * d




def solve2(data):
    """Solves part2."""
    draws, boards = parser(data)
    boardMarks = [[[0 for i in range(5)] for j in range(5)] for k in range(len(boards))]
    winningBoard = []
    winningBoardMark = []
    winningDraw = 0
    indexOBoardsWhoWon = set()
    print(draws)
    print(boardMarks)

    for d in draws:
        for index, board in enumerate(boards):
            for i in range(5):
                for j in range(5):
                    if board[i][j] == d:
                        print(f"mark for draw {d} on board {index} at line {i} and column {j}")
                        boardMarks[index][i][j] = 1

                        # test if we have a full line or full column
                        if ((sum(boardMarks[index][i][k] for k in range(5)) == 5) or (sum(boardMarks[index][k][j] for k in range(5)) == 5)) and index not in indexOBoardsWhoWon :
                            print("new win !")
                            winningBoard = board
                            winningBoardMark = copy.deepcopy(boardMarks[index])
                            winingIndex = index
                            winningDraw = d
                            indexOBoardsWhoWon.add(index)
                            print(winningBoardMark)

    print(f"winning board index is {winingIndex}, winning draw is {winningDraw} and wining board is {winningBoard} and wining board mark is {winningBoardMark}")
    return sumUnmarked(winningBoard, winningBoardMark) * winningDraw



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
