#!/usr/bin/env python3
"""
------------------------------------------------------------------------------------------
Elements of AI | Assignment 1 | Part - 3
------------------------------------------------------------------------------------------
Input: [1] A text file with group preferences of each student. This includes preferred
       group size, preferred teammates(friends), students he/she does not want to be
       teamed up with(foes)
       [2] Values for k,m,n
       
Output: Group assignment for each student and the total time requirement for instructors

The search problem was formulated as follows:
Since we do not know in advance which state is a goal state, we need to generate
all possibilites of group assignments and then pick one which has least time requirement
(least cost). This brute-force approach will find the most optimum group allocation, but
will take a long time to complete as the number of successor states will be huge for each
combination, for moderate to large number of students.

The approach adopted here is to return only one successor state at a time, instead of
returning all possible combinations, so that the state space can be reduced. The one state
being returned is the one which has the least cost amongst all the states generated in a
particular run. This is repeated till fringe is empty and we get a single group allocation.

Drawback: The cost of the successor state being chosen is compared only locally and
not globally i.e., finding a state which has the lowest cost only amongst those states
generated during that single pass. This state may not eventually lead to the best state
possible. However, this reduces the time required to find a comparably good state.

------------------------------------------------------------------------------------------

"""

import sys
from itertools import *

# NOTE: Majority of functions are written in a separate file. Importing all of them
from utility_functions import *

"""
A lookup dictionary is created where each key is a student of the class
and the value for that key is his/her preferences. Dictionary was chosen for
reason of quicker read times. This dictionary will be the basis for calculating
cost (time requirement) 

Here is how the dict will look like:
sample_lookup_dict = {
"djcran": {
        "size":3,
        "likes": ["zehzhang","chen464"],
        "dislikes": ["kapadia"]
    }
}
"""
########## Defining variables ########################

# this will be a group assignment where each student is
# in a separate group of their own i.e. singleton groups 
initial_list = []

# Fetching inputs from cmd-line
input_file = str(sys.argv[1])
k = int(sys.argv[2])
m = int(sys.argv[3])
n = int(sys.argv[4])


########## End of defining variables #################


#Reading input and removing terminating characters
with open(input_file) as file:
	raw_input = file.readlines()
	
cleaned_input = [(item.strip()) for item in raw_input]

# Forming the lookup_dict based on input.txt
for entry in cleaned_input:
    friends = []
    foes = []
    
    student_name = entry[0:entry.find(' ')]

    # Populating the initial group assignment i.e, singleton groups
    initial_list.append([student_name]) 
                         
    second_space_index = entry.find(' ', entry.find(' ') +1 )
    third_space_index = entry.find(' ', second_space_index + 1)
                         
    friends.append(entry[second_space_index + 1: third_space_index])
    foes.append(entry[third_space_index + 1:])

    # Populating lookup_dict
    lookup_dict[student_name] = {
        "size": int(entry[entry.find(' ')+1]),
        "likes": friends[0].split(','),
        "dislikes": foes[0].split(',')
        }


"""
Function to generate successors, given a particular group assignment
Returns only one state (which is the one having least cost)

REFERENCES:
[1] Below implementation was discussed with Manjeet Kumar till the comment #END_OF_REF
[2] Method adopted while appending to list_of_successors was taken from the
    approach followed in starter code given for A0 (nqueens assignment)
    i.e., inspired from return statement in add_piece() function
    
"""
def successors(state):
    N = len(state)
    list_of_successors = []
    for i in range(0,N-1):
        if (len(state[i])+len(state[i+1])) < 4:
            if len(state[i]) > 1:
                if initial_list.index([state[i][1]]) < initial_list.index(state[i+1]):
                    list_of_successors.append(state[0:i] + [state[i] + state[i+1]] + state[i+2:])
                else:
                    list_of_successors.append(state[0:i] + [[state[i][0]] + state[i+1] + [state[i][1]]] + state[i+2:])
            else:
                list_of_successors.append(state[0:i] + [state[i] + state[i+1]] + state[i+2:])

        for j in range(i+1,N-1):
            if (len(state[i])+len(state[j+1])) < 4:
                if len(state[i]) > 1:
                    if initial_list.index([state[i][1]]) < initial_list.index(state[j+1]):
                        list_of_successors.append(state[0:i] + [state[i] + state[j+1]] + state[i+1:j+1] + state[j+2:])
                    else:
                        list_of_successors.append(state[0:i] + [[state[i][0]] + state[j+1] + [state[i][1]]] + state[i+1:j+1] + state[j+2:])
                else:
                    list_of_successors.append(state[0:i] + [state[i] + state[j+1]] + state[i+1:j+1] + state[j+2:])
    #END_OF_REF

    # list_of_successors will have all possible combinations of groups
    # Picking only the group which has the least cost amongst these
    best_state, cost = calculate_cost(list_of_successors,k,m,n)
    return [best_state]


def solve(initial_list):
    fringe = [initial_list]
    # Need another list to check if current state is visited or not
    # Also, fringe gets popped, so need this as a temp location to store all states
    visited_fringe = [initial_list]
    
    while(len(fringe) > 0 and fringe[0] is not None):
        for state in successors(fringe.pop(0)):
            # Only if current state has not been seen before, add to fringe
            if state not in visited_fringe and state is not None:
                fringe.append(state)
                visited_fringe.append(state)
                
            # If there are no states left, break from the loop    
            if state is None:
                break
            
    # All iterations done. Find the best state and its cost
    best_state, cost = calculate_cost(visited_fringe,k,m,n)        
    print_according_to_format(best_state,cost)

# Invoking main driver with initial_list of singleton groups
solve(initial_list)
