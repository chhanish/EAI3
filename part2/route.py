#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: JUSHAH, ADPANDEY, HACHID
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#


# !/usr/bin/env python3

import sys
import numpy as np
import math



##======================================================
## This part of Code written by Aditya Pandey
##======================================================

def get_city_gps(filename):
    city_name = []
    city_latitude = []
    city_longitude = []

    with open(filename) as file:
        for line in file:
            l = line.split()
            city_name.append(l[0])
            city_latitude.append(float(l[1]))
            city_longitude.append(float(l[2]))
            
    return list(zip(city_name, city_latitude, city_longitude))


def get_road_segments(filename):
    first_city = []
    second_city = []
    highway_length = []
    speed_limit = []
    highway_name = []


    with open(filename) as file:
        for line in file:
            l = line.split()
            first_city.append(l[0])
            second_city.append(l[1])
            highway_length.append(l[2])
            speed_limit.append(l[3])
            highway_name.append(l[4])
    return list(zip(first_city, second_city, highway_length,
                    speed_limit, highway_name))


'''
List fo cost function.
It is in terms of distance, time, segments or delivery.
'''
## Cost functions

def distance(segment, curr_cost):
    return float(segment[2])

def time(segment, curr_cost):
    return round(float(segment[2])/float(segment[3]),4)

def segments(segment, curr_cost):
    return float(1)

def delivery(segment, curr_cost):
    if float(segment[3]) < 50:
        p = 0
    else:
        p = math.tanh(float(segment[2])/1000)
    
    return round(float(segment[2])/float(segment[3]) + 2*p*(curr_cost + float(segment[2])/float(segment[3])),4)


# Total Cost required to reach current state
def total_cost(segment, curr_cost,f):
    move_cost = f(segment, curr_cost)
    return move_cost

##======================================================
## Codes Written by Aditya Pandey ends here
##======================================================



##======================================================
## This part of Code written by Jugal Shah
##======================================================
'''This is similar to successor function. For current city
it is gneerating list of all possible cities it can go from there. 
For this, it uses information stored in road_segments data.
Apart from generating name of next city, it is also storing inforamtion such as 
speed and distance require to travel to that city. 
'''


def generate_next_cities(city, road_segments):
    next_cities = []
    for segment in road_segments:
        if city == segment[0]:
            next_cities.append([segment[1], (city, segment[1]), segment[2], segment[3]])
        elif city == segment[1]:
            next_cities.append([segment[0], (city, segment[0]), segment[2], segment[3]])
        else:
            continue
    return next_cities

''' 
Based on given two cities, it is finding name of segments that connects to this
two cities. It returns, name of cities, speed, distance and name of highway connecting
these two cities. '''

def get_segments(cities, road_segments):
    for s in road_segments:
        if (cities[0] == s[0] and  cities[1] == s[1]):
            return s
        elif  (cities[0] == s[1] and  cities[1] == s[0]):

            t = (s[1], s[0], s[2], s[3], s[4])
            return t

'''
Based on solution, it is generating required dictionary that has information 
such as route taken ,number of segments, time taken for trip, distance travelled
as well as delivery time required for this route.
'''
def get_answer(solution, road_segments):
    route_dictionary = {}
    route_pairs = [(i,j) for i,j in zip(solution, solution[1:])]
    segment_pairs = [get_segments(r, road_segments) for r in route_pairs]

    d_trip = [0]
    t_trip = [0]
    t_trip_delivery = [0]
    route_taken = []
    for i,s in enumerate(segment_pairs):
        route_taken.append((s[1], str(s[-1]) + " for " + str(s[2]) + " miles"))

        d_trip.append(distance(s,0))
        t_trip.append(time(s,0))
        t_trip_delivery.append(delivery(s, t_trip[i]))
    
    route_dictionary = {"total-segments" : len(route_taken), 
            "total-miles" : round(sum(d_trip),4), 
            "total-hours" : round(sum(t_trip),4), 
            "total-delivery-hours" : round(sum(t_trip_delivery),4), 
            "route-taken" : route_taken}
    
    return route_dictionary

def get_route(start, end, cost):
    
    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time 
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
        # path + 'city_gps.txt'
    city_gps = get_city_gps('city-gps.txt')
    # path + 'road_segment.txt'
            
    road_segments = get_road_segments('road-segments.txt')
    

    current_city =  start ## Initial state
    goal = end # Target state
    cost_function_dictionary = {"distance" : distance,
                            "time" : time,
                            "delivery" : delivery,
                            "segments" :segments
                            }

    ## Inital costs
    move_cost = 0 
    d_trip = 0
    t_trip = 0
    t_trip_delivery = 0


    visited_cities = [] # List of visited states

    '''
    Fringe stores to items. One is current path travelled and 
    second is total cost to travel so far.
    Path travelled is like below.
    start_city --> city1 --> city2 --> end city
    '''
    fringe=[([current_city], move_cost)] 
    while fringe:
            (curr_path, curr_cost)=fringe.pop(0) 
            curr_city = curr_path[-1] # In current path last city represents current state

            if curr_city not in visited_cities:

                # Generate successors
                new_segments = generate_next_cities(curr_city, road_segments)

                ## loop through each successors
                for s in new_segments:
                    if s[0] not in visited_cities:
                            fringe.append((curr_path +[s[0]], curr_cost + total_cost(s,curr_cost, cost_function_dictionary[cost])))

                            if s[0] == goal:
                                solution = fringe[-1][0]
                                return get_answer(solution, road_segments)

                visited_cities.append(curr_city) # Append curr_city to visited_cities

                # Sort fringe based on cost
                fringe = sorted(fringe, key = lambda x: x[1])

    return (-1,"")   

##======================================================
## Codes from Jugal Shah ends here
##======================================================


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])


