#/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: JUSHAH, ADPANDEY, HACHID
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
#

## Importing necessary libraries
import sys
import time
import numpy as np
import itertools
import random


## This functions read data nand returns list of list for each user/student
def read_data(data):
    records = []
    for item in data:
        records.append(item.split())
    for item in records:
        team_size = len(item[1].split('-'))
        item[1] = item[1].split('-')
        item.append(team_size)
        item[2] = item[2].split(',')
    return records

def user_data_generator(data):
    ''' 
    This functions generate dictionary for each user with their
    inforamtion filled out on survey form.
    '''
    records = read_data(data)
    user_data = {}

    users = [i[0] for i in records]

    for i,u in enumerate(users):
        user_data[u] = {"team_size" : records[i][3], "unwanted" : records[i][2],
                        "requested" : [i for i in records[i][1]] }
    return user_data


def cost_calculator(user_data, groups):
    ''' 
    This functions calcualtes cost for each users based on their current
    assignments in group. It is breakdown cost into detail level such as 
    code sharing cost, incorrect team size cost as well as unwanted/nonpreferred
    person assigned in same group cost.

    Apart from that, it also calcualtes total cost for each formation of teams.


    function returns details for cost for each users, formation of teams and
    overall costs.
    '''         

    users = list(user_data.keys())
    user_actual = {}

    for u in users:
        user_actual[u] = {"unwanted_cost" : 0, "incorrect_teamsize_cost" : 0,
                          "code_sharing_cost" : 0}
        for g in groups:
            temp = g.split("-")
            if u in temp:
                if len(temp) != user_data[u]['team_size']:
                    user_actual[u]["incorrect_teamsize_cost"] = 2
            
                for not_wanted in user_data[u]['unwanted']:
                    if not_wanted in  temp:
                        user_actual[u]["unwanted_cost"] += 10
                for wanted in user_data[u]['requested']:
                    if wanted not in temp and wanted not in ('xxx', 'zzz'):
                        user_actual[u]["code_sharing_cost"] += 3

    code_sharing_cost = sum([i['code_sharing_cost'] for i in user_actual.values()])
    incorrect_teamsize_cost = sum([i['incorrect_teamsize_cost'] for i in user_actual.values()])
    unwanted_cost = sum([i['unwanted_cost'] for i in user_actual.values()])
    grading_cost = len(groups)*5

    total_cost = code_sharing_cost + incorrect_teamsize_cost + unwanted_cost + grading_cost

    return user_actual, groups, total_cost

def get_formatted_groups(teams):
    ''' 
    Function to generate clean human readable format for team names
    '''
    return ["-".join(t) for t in teams]


def get_best_group(user_form_data, group):
    ''' 
    Function analyze all neighboring groups and returns best group based 
    on minimum cost
    '''
    groups = [(i, cost_calculator(user_form_data ,
                                  get_formatted_groups(i))[2]) for i in group]
    return sorted(groups, key = lambda x : x[1])[0][0][0]   

def is_all_asigned(assigned_group, users):
    ''' 
    Function to check if all students are assigned in groups and no one is 
    left out.
    '''
    return len(users) == sum([len(i) for i in assigned_group])

def group_generator2(user_form_data, users):
    ''' 
    This is a successor function which generates groups based on users request 
    as well as available users. 

    It considers users requests for team size and try to allocate users into
    their requested team size. If it is not possible, it is randomly placing them
    in team of 1 or 2 or 3.

    Also, it number of users are more than 50, it will first randomly select 50
    users and then assign them first. After that it will select randomly again
    until all students that are left less than 50.

    '''

    if len(users) > 50:
        users = random.sample(users,50)

    groups = []

    u3 = [u for u in users if user_form_data[u]['team_size'] == 3]
    u2 = [u for u in users if user_form_data[u]['team_size'] == 2]
    # print(len(u3), len(u2))
    if len(u3) > 3:
        groups = [[list(g)] for g in
                  itertools.combinations(u3, random.randint(2,3))]
    elif len(users) > 3 and len(u2) > 2:
        groups = [[list(g)] for g in
                  itertools.combinations(u2, random.randint(1,2))]
    elif len(users) > 3 :
        groups = [[list(g)] for g in
                  itertools.combinations(users, random.randint(2,3))]
    
    elif len(users) > 2 :
        groups = [[list(g)] for g in
                  itertools.combinations(users, random.randint(1,2))]
    else:
        groups.append(list(users))

    if len(groups) == 0:
        print("Null")
    
    return groups

def local_search2(user_form_data):

    ''' 
    This is a main search function which arrange users in group based on 
    their cost. It try to arrange users such a way that group with minimum cost
    takes priority. After that, it generates new group from remaining users 
    and again picks group with lowest cost.

    It will keep searching and forming groups of users/students until all users 
    are assigned into some group.

    Function returns assigned groups for all students.
    
    '''

    #Search initiated
    all_assigned = False
    assigned_user = []
    not_assigned_user = []
    assigned_groups = []
    users = list(user_form_data.keys())

    while all_assigned == False:

        if is_all_asigned(assigned_groups, users):
            all_assigned = True
            return assigned_groups

        not_assigned_user = [u for u in users if u not in assigned_user]

        # print("Ungrouped : ", not_assigned_user)
        #Generate the successors here.
                
        groups = group_generator2(user_form_data, not_assigned_user)
        # print(groups)
        
        #get the min cost successor
        if len(groups) > 1:

            best_group = get_best_group(user_form_data, groups)
            # print(best_group)
        else:
            best_group = groups[0]

        #Add the min cost successor to the final list
        if len(not_assigned_user) == 1:
            assigned_user.append(not_assigned_user[0])
            assigned_groups.append(best_group)
        else:
            for s in best_group:
                assigned_user.append(s)
            assigned_groups.append(best_group)
        # print(assigned_groups)
        
        del groups[:]
        del not_assigned_user[:]
  
def solver(input_file):
    """
    1. This function should take the name of a .txt input file in the format indicated in the assignment.
    2. It should return a dictionary with the following keys:
        - "assigned-groups" : a list of groups assigned by the program, each consisting of usernames separated by hyphens
        - "total-cost" : total cost (time spent by instructors in minutes) in the group assignment
    3. Do not add any extra parameters to the solver() function, or it will break our grading and testing code.
    4. Please do not use any global variables, as it may cause the testing code to fail.
    5. To handle the fact that some problems may take longer than others, and you don't know ahead of time how
       much time it will take to find the best solution, you can compute a series of solutions and then
       call "yield" to return that preliminary solution. Your program can continue yielding multiple times;
       our test program will take the last answer you 'yielded' once time expired.
    """
    ## Reading Text file and generating user data from it.
    with open(input_file) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]

    user_form_data = user_data_generator(lines)

    # Intial cost. It is very high value. We will update it if find better 
    # cost during our search. 
    best_cost = 1e9

    while True:

        ## Generating groups info and cost info
        new_groups = get_formatted_groups(local_search2(user_form_data))
        new_cost = cost_calculator(user_form_data, new_groups)[2]

        # compare if new cost is better than best cost.
        # If yes, we will update it to best cost 
        if new_cost < best_cost:
            best_cost = new_cost
            best_groups = new_groups.copy()

        # Thinking time :) 
        time.sleep(2)

        # Yields results 
        yield ({"assigned-groups": best_groups,
                "total-cost" : best_cost})

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])
    
