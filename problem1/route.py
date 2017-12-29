#(1) Which search algorithm seems to work best for each routing options?
"""Implemented the below :
Distance
Time
Segments

Answers to question 1 
1. Astar gave the most fastest route.

(2)Which algorithm is fastest in terms of the amount of computation time required by your 
#program, and by how much, according to your experiments?
#Ans : Astar seems to the fastest in terms of amount of computation needed .

#3: Uniform Cost would take the least amount of memory.

#4 :distance_haversine : We calculated the havershine distance by converting into radians and using the earth's circumference because as earth #
is not a flat surface we will be more accurate if we use the havershine rather than euclidean.
Time Heuristic was calculated by taking the Havershine distance/maxinmum speed limit, which is 65 .
Segments Heuristic was calculated by cost = number of nodes travelled  and heuristic is  1 , which is minimum nodes need to be traversed.

##We cleaned the data by removing the nan's and 0's by replacing with the mean value of the data .

#Class Graph : We created a graph class to get the edges and nodes.
#Saved the distance and time uding the add_node function. """



#!/usr/bin/env python3

import pandas as pd
import math, sys
from collections import deque
import heapq
import itertools
import copy
# from collections import defaultdict



total_distance = 0
total_time = 0

#------------------------------------------------------------------------------------------------
#Worked on the following code with team-mate Paritosh M.
#Closed array for visited states
closed=[]

#Previus dictionary for finding the path
previous={}



city = sys.argv[1]
city2= sys.argv[2]
route=sys.argv[3]
cost_type =sys.argv[4]

City_Gps={}

data=open('city-gps.txt',"r")
for line in data:
    line=map(str,line.split())
    key,val=line[0],line[1:]
    City_Gps[key]=val

Road_Seg= pd.read_csv('road-segments.txt',delimiter=' ',names=['City1','City2','Dist','Speed','HighWay'])


#replace the NaN's and O's

def smean(sumx):
    return ( (sum(Road_Seg['Speed']))/(len(Road_Seg['Speed'])))
    
        

def dmean(sumx):
    return ( (sum(Road_Seg['Speed']))/(len(Road_Seg['Speed'])))
    
    
# Replacing the NAN's and 0's in the Speed column with mean of the Speed column.
Road_Seg['Speed'] = Road_Seg['Speed'].fillna(0)
Road_Seg[Road_Seg["Speed"]==0] = Road_Seg[Road_Seg["Speed"]==0].replace(0,smean(Road_Seg["Speed"]))


# Replacing the NAN's and 0's in the Speed column with mean of the Dist column.

Road_Seg['Dist'] = Road_Seg['Dist'].fillna(0)
Road_Seg[Road_Seg["Dist"]==0] = Road_Seg[Road_Seg["Dist"]==0].replace(0,dmean(Road_Seg["Dist"]))


#Used code from  https://docs.python.org/2/library/heapq.html for implementing priorityQ
#########HeapQ
pq_fringe=[]
pq_finder={}
REMOVED = '<removed-task>'
counter = itertools.count()

def add_task(task, priority=0):
    'Add a new task or update the priority of an existing task'
    if task in pq_finder:
        remove_task(task)
    count = next(counter)
    entry = [priority, count, task]
    pq_finder[task] = entry
    heapq.heappush(pq_fringe, entry)

def remove_task(task):
    'Mark an existing task as REMOVED.  Raise KeyError if not found.'
    entry = pq_finder.pop(task)
    entry[-1] = REMOVED

def pop_task():
    'Remove and return the lowest priority task. Raise KeyError if empty.'
    while pq_fringe:
        priority, count, task = heapq.heappop(pq_fringe)
        if task is not REMOVED:
            del pq_finder[task]
            return task
    raise KeyError('pop from an empty priority queue')
#########HeapQ

#------------------------------------------------------------------------------------------------------------------------

#--------------------------------##--------------------------------------------------------
#Distance using the lat's and long's using havershine
# Modified version of finding havershine distance  https://gist.github.com/rochacbruno/2883505

def distance_haversine(start_city, goal_city):

    if (start_city in City_Gps )and(goal_city in City_Gps):
        lat1,long1=(City_Gps[start_city])
        lat2,long2=City_Gps[goal_city]

        lat1=float(lat1)
        long1=float(long1)


        lat2=float(lat2)
        long2=float(long2)

        radius = 3596 # radius of earth in  miles
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(long2 - long1)
        a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
                                                      * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(
            dlon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = radius * c
        if cost_type=="distance":
            return d
        elif cost_type=="time":
            return (d/65)-2
        elif cost_type=="segments":
            return 1

    return 99999.0

#--------------------------------##--------------------------------------------------------
#Finding time
Road_Seg["time"]= Road_Seg["Dist"]/Road_Seg["Speed"]

class Graph:
    #Initiating graph
    
    def __init__(self):
        self.__graph_dict = {}
        self.__edge_dict = {}


    def add_node(self,fromc,toc,dist,time):
        # new_node = toc
        if fromc not in self.__graph_dict:
            self.__graph_dict[fromc] = set()
            self.__graph_dict[fromc].add(toc)
        else:
            self.__graph_dict[fromc].add(toc)
        if toc not in self.__graph_dict:
            self.__graph_dict[toc] = set()
            self.__graph_dict[toc].add(fromc)
        else:
            self.__graph_dict[toc].add(fromc)
        edge_key = frozenset((fromc,toc))
        if edge_key not in self.__edge_dict:
            # self.__edge_dict[edge_key] = []
            self.__edge_dict[edge_key] = [dist, time]

    def print_graph(self):
        print (self.__graph_dict)

    def get_graph(self):
        return self.__graph_dict

    def get_edges(self):
        return self.__edge_dict
            
graph=Graph()

#storing both the from and to city names , distances, time in the graph
for i in range (len(Road_Seg)):
    graph.add_node(Road_Seg['City1'][i],Road_Seg['City2'][i],Road_Seg['Dist'][i],Road_Seg['time'][i])

test_graph = graph.get_graph()
edges = graph.get_edges()

def cost_from_start(path,cost_type):
    cost=0

    if cost_type== 'distance':
        for i in range(len(path) - 1):
            edge = frozenset((path[i], path[i + 1]))
            cost += edges[edge][0]

    if cost_type=='time':
        for i in range(len(path) - 1):
            edge = frozenset((path[i], path[i + 1]))
            cost += edges[edge][1]

    if cost_type=='segments':
        cost=len(path)

    return cost


def dfs(graph, start, goal):
    dfs_stack = [(start, [start])]
    while dfs_stack:
        (node, path) = dfs_stack.pop()
        for next in graph[node] - set(path):
            if next == goal:
                return path + [next]
            else:
                dfs_stack.append((next, path + [next]))
    return None

def bfs(graph, start, goal):
    bfs_queue = deque([(start, [start])])
    while bfs_queue:
        (node, path) = bfs_queue.popleft()
        for next in graph[node] - set(path):
            if next == goal:
                return path + [next]
            else:
                bfs_queue.append((next, path + [next]))
    return None

def a_star(graph, start, goal, cost_type):

    previous[start]=[start,[start],0]
    add_task(start,distance_haversine(start,goal))
    visited=[]
    while len(pq_fringe)>0:

        curr_state=pop_task()
        closed.append(curr_state)

        visited.append(curr_state)

        if curr_state ==goal:
            return previous[curr_state][1]


#        print path
        for s in graph[curr_state] - set(visited):
            start_to_end_path=copy.deepcopy(previous[curr_state][1])
            start_to_end_path.append(s)

            heuristic=distance_haversine(s, goal)
            previous[s]=[s,start_to_end_path,heuristic]
            cost_start_to_succ = cost_from_start(start_to_end_path, cost_type)

            if(route=="uniform"):
                cost_start_to_succ=1+len(previous[curr_state][1])
                heuristic=0

            f= cost_start_to_succ + heuristic

            if(s in closed):
                continue
            if s in pq_finder:
                entry=pq_finder[s]
                if entry[0]>f:
                    remove_task(s)

            if not(s in pq_finder):
                add_task(s,f)
                previous[s]=[curr_state,start_to_end_path,cost_start_to_succ]




def print_path():
    total_distance=0
    total_time=0
    for i in range(len(path) - 1):
        edge = frozenset((path[i], path[i + 1]))
        total_distance += edges[edge][0]
        total_time += edges[edge][1]
        s=""
        for p in path:
            s+=p+" "
    print total_distance, total_time, s  # Printing the required format



#Routing based on the algorithm value
if  route == 'bfs':
    path = bfs(test_graph,sys.argv[1],sys.argv[2])
elif route == 'dfs':
    path = dfs(test_graph,sys.argv[1],sys.argv[2])
elif route == 'astar' or route=='uniform':
    path = a_star(test_graph, city, city2, cost_type)

if path is None:
    print ('No path found')
else:    print_path()

	
