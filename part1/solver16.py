#!/usr/bin/python
# solver16.py : Circular 16 Puzzle solver
# Based on skeleton code by D. Crandall, September 2018
#
from Queue import PriorityQueue
from random import randrange, sample
import sys
import string

# implement fringe as a priority queue in order to execute a* search
fringe=PriorityQueue()

def shift_row(state, row, dir):
    change_row = state[(row*4):(row*4+4)]
    return ( state[:(row*4)] + change_row[-dir:] + change_row[:-dir] + state[(row*4+4):], ("L" if dir == -1 else "R") + str(row+1) )

# shift a specified col up (1) or down (-1)
def shift_col(state, col, dir):
    change_col = state[col::4]
    s = list(state)
    s[col::4] = change_col[-dir:] + change_col[:-dir]
    return (tuple(s), ("U" if dir == -1 else "D") + str(col+1) )

# pretty-print board state
def print_board(row):
    for j in range(0, 16, 4):
        print('%3d %3d %3d %3d' % (row[j:(j+4)]))

# return a list of possible successor states
def successors(state):
    return [ shift_row(state, i, d) for i in range(0,4) for d in (1,-1) ] + [ shift_col(state, i, d) for i in range(0,4) for d in (1,-1) ] 

# just reverse the direction of a move name, i.e. U3 -> D3
def reverse_move(state):
    return state.translate(string.maketrans("UDLR", "DURL"))

# check if we've reached the goal
def is_goal(state):
    return sorted(state) == list(state)

# define a function to calculate the total heuristic value of the board, where the heuristic is the sum of manhattan distances of all the elements on the board.
def heuristic(board):
	h=0
	for item in range(16):
		h+=distance(board[item],item)   # this gives the heuristic values for each element and sums them up
	return h   # returns the total heuristic value of the board

def distance(j,i):    # here, i is the current position (index) of an element on the board and j is the position where it should be when it is sorted
	j-=1
	if i==j:    # if the current position and the goal position is the same, then the manhattan distance should be zero
		return 0
	count=0
	# the following 4 if conditions are for wrapping the board so that, for example, if an element has to travel from the first row to the last row, it should be counted as one step.
	if i in [0,1,2,3] and j in [12,13,14,15]:
		i+=12
		count+=1
	if i in [12,13,14,15] and j in [0,1,2,3]:
		i-=12
		count+=1
	if i in [0,4,8,12] and j in [3,7,11,15]:
		i+=3
		count+=1
	if i in [3,7,11,15] and j in [0,4,8,12]:
		i-=3
		count+=1
	# now, we have to move the element to the same row as the goal position
	c=i//4
	d=j//4
	if c<d:
		i=i+((d-c)*4)
		count+=(d-c)
	else:
		i=i-((c-d)*4)
		count+=(c-d)
	# now the element is in the same row. Next, we have to calculate the number of steps to take it to the goal position.
	if i<j:
		while i!=j:
			i+=1
			count+=1
	else:
		while i!=j:
			i-=1
			count+=1
	return count


# The solver!
def solve(initial_board):
    fringe.put((1,initial_board, ""))    # here, i gave 1 as heuristic since it doesnt matter as it will be the only member in the queue and will be popped anyway
    while not fringe.empty():
        (h1,state, route_so_far) = fringe.get()    # here, the node with the least heuristic value (priority) will be popped, with the heuristic value of the board being stored in h1
        for (succ,move) in successors( state ):
            h2=h1+heuristic(succ)    # h2 will store the cost of the path followed till now + the cost to reach from current state to goal state
            if is_goal(succ):
                return( route_so_far + " " + move )
            fringe.put((h2, succ, route_so_far + " " + move  ))   # the board is put into the stack with heuristic value as the priority
    return False

# test cases
start_state = []
with open(sys.argv[1], 'r') as file:
    for line in file:
        start_state += [ int(i) for i in line.split() ]

if len(start_state) != 16:
    print("Error: couldn't parse start state file")

print("Start state: ")
print_board(tuple(start_state))

print("Solving...")
route = solve(tuple(start_state))

print("Solution found in " + str(len(route)/3) + " moves:" + "\n" + route)
