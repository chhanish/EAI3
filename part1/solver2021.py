#!/usr/local/bin/python3
# solver2021.py : 2021 Sliding tile puzzle solver
#
# Code by: name IU ID - JUSHAH, ADPANDEY, HACHID
#
# Based on skeleton code by D. Crandall & B551 Staff, September 2021
#

import sys
import numpy as np

ROWS=5
COLS=5

def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]

## ==========================================================================
##### Note - Below code snippet is taken from test_a1p1.py given as part of assignment. 
### It contained useful functions to move tiles which is required to generate successors.
##=============================================================================

def move_right(board, row):
  """Move the given row to one position right"""
  board[row] = board[row][-1:] + board[row][:-1]
  return board

def move_left(board, row):
  """Move the given row to one position left"""
  board[row] = board[row][1:] + board[row][:1]
  return board

def rotate_right(board,row,residual):
    board[row] = [board[row][0]] +[residual] + board[row][1:]
    residual=board[row].pop()
    return residual

def rotate_left(board,row,residual):
    board[row] = board[row][:-1] + [residual] + [board[row][-1]]
    residual=board[row].pop(0)
    return residual

def move_clockwise(board):
    """Move the outer ring clockwise"""
    board[0]=[board[1][0]]+board[0]
    residual=board[0].pop()
    board=transpose_board(board)
    residual=rotate_right(board,-1,residual)
    board=transpose_board(board)
    residual=rotate_left(board,-1,residual)
    board=transpose_board(board)
    residual=rotate_left(board,0,residual)
    board=transpose_board(board)
    return board

def move_cclockwise(board):
    """Move the outer ring counter-clockwise"""
    board[0]=board[0]+[board[1][-1]]
    residual=board[0].pop(0)
    board=transpose_board(board)
    residual=rotate_right(board,0,residual)
    board=transpose_board(board)
    residual=rotate_right(board,-1,residual)
    board=transpose_board(board)
    residual=rotate_left(board,-1,residual)
    board=transpose_board(board)
    return board

def transpose_board(board):
  """Transpose the board --> change row to column"""
  return [list(col) for col in zip(*board)]


def movement(board, direction, index):
    if direction == "R":
        board = move_right(board, index)
    elif direction == "L":
        board = move_left(board, index)
    elif direction == "U":
        board = transpose_board(move_left(transpose_board(board), index))
    elif direction == "D":
        board = transpose_board(move_right(transpose_board(board), index))
    elif direction == 'Oc':
        board = move_clockwise(board)
    elif direction == 'Occ':
        board = move_cclockwise(board)
    elif direction == 'Ic':
        board=np.array(board)
        inner_board=board[1:-1,1:-1].tolist()
        inner_board = move_clockwise(inner_board)
        board[1:-1,1:-1]=np.array(inner_board)
        board=board.tolist()
    elif direction == 'Icc':
        board=np.array(board)
        inner_board=board[1:-1,1:-1].tolist()
        inner_board = move_cclockwise(inner_board)
        board[1:-1,1:-1]=np.array(inner_board)
        board=board.tolist()
    return board
## =========================================================
#### Code Snippet taken from test_a1p1.py ends here.
## =========================================================

# return a list of possible successor states
def successors2(board):
    successor_boards = []

    for i in range(len(board)):
        successor_boards.append((movement(board.copy(), 'L', i), 'L'+ str(i+1)))
        successor_boards.append((movement(board.copy(), 'R', i), 'R'+ str(i+1)))
        successor_boards.append((movement(board.copy(), 'U', i), 'U'+ str(i+1)))
        successor_boards.append((movement(board.copy(), 'D', i), 'D'+ str(i+1)))
    successor_boards.append((movement(board.copy(), 'Oc', 0), 'Oc'))
    successor_boards.append((movement(board.copy(), 'Occ', 0), 'Occ'))
    successor_boards.append((movement(board.copy(), 'Ic', 0), 'Ic'))
    successor_boards.append((movement(board.copy(), 'Icc', 0), 'Icc'))
    return successor_boards

## ========================================================================
########    List of Heuristics developed as part of assignments.
########    Currently sum of Manhatten + misplaces tiles used as heuristics
##=========================================================================

## This code is referenced from https://github.com/xtine/8puzzle/blob/master/8puzzle.py
def heuristic_misplaced(board, goal):
    """
    Counts the number of misplaced tiles
    """
    misplaced = 0

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != goal[i][j]:
                misplaced += 1

    return misplaced
## Code reference ends here.


def get_coordinates(tile, board):
    """
    Returns the i, j coordinates for a given tile
    """
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == tile:
                return i, j

def heuristic_manhattan_distance(board, goal):
    """
    Counts how much is a tile misplaced from the original position
    """
    distance = 0
    distance_list = []

    for i in range(len(board)):
        for j in range(len(board[0])):
            i1, j1 = get_coordinates(board[i][j], goal)
            distance += abs(i - i1) + abs(j - j1)
            distance_list.append(abs(i - i1) + abs(j - j1))

    return distance

## ========================================================================

## Below function combines two or more heuristics
def h1(board, goal):
    # total_h =  max(heuristic_linear_conflict(board, goal), heuristic_manhattan_distance(board, goal), Inversed_tiles(board, goal))
    total_h = heuristic_misplaced(board, goal)    + heuristic_manhattan_distance(board, goal) #+  Inversed_tiles(board, goal) 
    return total_h

## Below function comutes total cost. It is sum of cost of traversing so far + cost to goal from current state
def cost_to_solution(board, goal, move):
    return move + h1(board, goal)

## ========================================================================

# check if we've reached the goal
def is_goal(state, goal):
    return h1(state, goal) == 0

def solve(initial_board):
    """
    1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
    2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
       For testing we will call this function with single argument(initial_board) and it should return 
       the solution.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

        # DEfine Final target arrangement for board
    goal = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20], [21, 22, 23, 24, 25]]

        # Defining current state of board
    board = [list(i) for i in list(np.array(initial_board).reshape(5,5))]
    cstate =  list(board).copy()
    move = 0  # Initial move cost
    visited_boards = []

    ''' Fringe contains following
    1. Current path travelled  with movement indicators
    2. number of moves made so far
    3. Cost to solution from current state
    '''

    fringe=[([(cstate, "")], move, cost_to_solution(cstate, goal, move))]

    while fringe:
            (curr_path, curr_move,  curr_cost)=fringe.pop(0)
            curr_board = curr_path[-1][0] # Last item in current path is current state

            if curr_board not in visited_boards: # Check if state is already visited
                move = curr_move + 1 # Add one move
                new_boards = successors2(curr_board ) # Geenrate successors

                    ## We will loop through each successors and calcualte cost
                    ## if successor is goal state, we will return solution
                for b in new_boards:
                        fringe.append((curr_path+[b], move, cost_to_solution(b[0], goal, move)))

                        if is_goal(b[0],goal):
                            fringe = sorted(fringe, key = lambda x: x[2])
                                # display(fringe[0])
                            return [i[1] for i in fringe[0][0]][1:]

                    ## Append curr_board to visited_board
                visited_boards.append(curr_board)

                    ## Sort fringe by minimum cost
                fringe = sorted(fringe, key = lambda x: x[2])
    return (-1,"")  


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
