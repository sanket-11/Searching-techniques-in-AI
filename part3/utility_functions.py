#!/usr/bin/env python3
"""
This file contains all the utility functions
used in assign.py for A1 of Elements of AI

"""
lookup_dict = {}
state_and_complaints_dict = {}


# Group that calculates cost for a given set of states.
# Passes through multiple functions for each category
# and updates state_and_complaints_dict accordingly.
#
# The dict has states as keys and values are the respective cost for
# each category of complaint

def calculate_cost(states,k,m,n):
    
    group_discrepency(states)
    not_assigned_to_friends(states,n)
    assigned_to_enemies(states,m)
    time_to_grade(states,k)
    best_state, least_cost = find_lowest_cost_group(state_and_complaints_dict)

    return best_state, least_cost


"""
Here is how the state_and_complaints_dict looks like:

sample_state_and_complaints_dict = {
    "[['c'],['a','b']]" : {
            'size_complaints' : 2,
            'friend_complaints': 0,
            'enemy_complaints' : 1,
            'time_to_grade' : 2,
            'total_cost': 5,
            'state' : [['c'],['a','b']]
        }
    }
"""

# Function to calculate cost for group size discrepency
# Checks whatever preference each group member had given for their group size
# with their actual group's size and increments a count
# Updates state_and_complaints_dict with the appropriate value

def group_discrepency(set_of_states):
    for state in set_of_states:
        group_size_complaint_count = 0
        for group in state:
            for person in group:
                group_size_requested = lookup_dict[person]['size']
                actual_size = len(group)
                if(actual_size != group_size_requested and group_size_requested != 0):
                    group_size_complaint_count = group_size_complaint_count+1

        state_and_complaints_dict[str(state)] = {
            'size_complaints' : group_size_complaint_count,
            'state': state
            }


# Function to calculate cost when person is assigned to
# somebody other than their friend.
# Gets a list of each person's teammates and compares each with
# their provided friend list. If any member of friend list is not present
# in teammates list, increment a count.
#
# Final cost will be multiplied by n
    
def not_assigned_to_friends(set_of_states,n):
    for state in set_of_states:
        friends_complain_count =0
        for group in state:
            for person in group:     
                teammates_of_person = list(set(group).symmetric_difference(set([person]))) 
                for friend in lookup_dict[person]['likes']:
                    if friend not in teammates_of_person and friend!= '_':
                        friends_complain_count = friends_complain_count +1
                        
        state_and_complaints_dict[str(state)]['friend_complaints'] = n*friends_complain_count
            


# Function to calculate cost when a person is assigned to
# someone mentioned in their dislikes list
# Similar logic to above function is implemented
#
# Final cost will be multiplied by m

def assigned_to_enemies(set_of_states,m):
    for state in set_of_states:
        enemy_complain_count = 0
        for group in state:
            for person in group:
                teammates_of_person = list(set(group).symmetric_difference(set([person]))) 
                for enemy in lookup_dict[person]['dislikes']:
                    if enemy in teammates_of_person and enemy != '_':
                        enemy_complain_count = enemy_complain_count +1
                        
        state_and_complaints_dict[str(state)]['enemy_complaints'] = m*enemy_complain_count



# Function to calculate how long it takes to grade
# each assignment. It is equivalent to how many groups have been formed
#
# Cost is multiplied by k

def time_to_grade(set_of_states,k):
    for state in set_of_states:
        state_and_complaints_dict[str(state)]['time_to_grade'] = k*len(state)



# Function finds the group which has the least total_cost
# by iterating through state_and_complaints_dict after each complaint
# function has been executed.
#
# Returns the group as well as its cost

def find_lowest_cost_group(d):
    minimum = 99999
    for group, group_costs in d.items():
        curr_state = group_costs.pop('state', None)
        d[group]['total_cost'] = sum(group_costs.values())
        if(group_costs['total_cost'] < minimum):
            minimum = group_costs['total_cost']
            curr_min_group = curr_state
    return curr_min_group, minimum



# Function to print groups per line and total cost at the end
# Removes unwanted characters such as commas, brackets, apostrophes

def print_according_to_format(best_state,cost):
    for group in best_state:
        converted = str(group)
        converted = converted.replace(',','').replace('[','').replace(']','').replace("'",'')
        print(converted)
    print(cost)
  
