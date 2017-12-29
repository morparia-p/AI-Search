# Paritosh Morparia
# pmorpari@iu.edu
"""
Problem description:

Initial state: Given input state

State Space: A valid state is one that has tiles 0 to 15 in 15 puzzle problem.
    The given state must be solvable to be a valid state. That is it should satisfy inversion condition
    for given size of puzzle.
    In this case, as size =4(even):
        If tile 0 is in even row from bottom, sum of inversions must be odd.
        If tile 0 is in odd row from bottom,sum of inversions must be odd.

Successor function: A valid successor in this problem is one that replaces tile 0.This is a special case
    of 15 puzzle problem. A successor can move 2 or 3 blocks in either UP, DOWN, LEFT or RIGHT direction.

Edge weights: Each move will cost 1 unit.

Goal State: Here goal state will be canonical state of 15 puzzle problem.
                            1 2 3 4
                            5 6 7 8
                            9 10 11 12
                            13 14 15 0
Heuristic function:
    Here ceiling(manhattan-distance/3) in combination with linear conflict.
    Admissibility:
    1.Manhattan-distance/3- Manhattan distance was admissible for simple 15 puzzle problem.
        For this special case it is not as we can move 2 or 3 tiles in a single move.
        But if we divide manhattan by 3, heuristic cost will be at most 2. Which is less than or equal to
        the number of actual moves.
    2. Liner conflict checks for swapped positions in a line. Minimum of 2 moves are required
        for resolving conflicts.

------------------------
Search Algorithm #3

The program uses search algorithm 3 from the lecture slides of Dr. Crandall.
It uses consistency of heuristic to avoid visiting already visited nodes.
It checks for 3 conditions,
    1. if node is already a visited state, it will avoid the state,
    2. if a node with higher cost is in fringe it replaces it in fringe.
    3. if node is not in fringe, it will add it to fringe.

------------------------
Design decisions:

Choosing heuristic funtion:
Tried and tested several heuristic as
1.Number of tiles not in intended row and column
2.Number of tiles not in position(not admissible)
3.Two moves if number of tiles not in row and column+ One move if not in row or column
4.Manhattan/3
5. Manhattan/3 in combination with linear conflict.

Out of all of these. option 5 gave shortest solution visiting the least number of nodes.
"""


#The function successors,solver have been referred from a0.py  by djCrandall
import numpy as np
import sys
from copy import deepcopy
import heapq
import itertools
import time
import math

#Canonical state for comparison
canonical=np.asarray([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]])

#Closed array for visited states
closed=[]

#Previus dictionary for finding the path
previous={}



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

#Converting list to tuple for using it as key in dictionary
def to_tuple(s):
    tuple_of_tuple=tuple(tuple(x) for x in s)
    return tuple_of_tuple

#successors gives possible successors to the given state
def successors(curr_state):
    pos=pos_n(curr_state, 0)
    i=pos[0]
    j=pos[1]
    succ=[]

# Swap tile downwards
    s=deepcopy(curr_state)
    for k in range(i-1,-1,-1):
        s=swap(k ,j ,k+1 ,j ,s)
        succ.append(s)

# Swap tile to right
    s=deepcopy(curr_state)
    for k in range(j-1,-1,-1):
        s=swap(i ,k ,i ,k+1 ,s)
        succ.append(s)

# Swap tile downwards
    s = deepcopy(curr_state)
    for k in range(i+1, 4):
        s = swap(k,j,k-1,j,s)
        succ.append(s)

# Swap tile to left
    s = deepcopy(curr_state)
    for k in range(j+ 1,4):
        s = swap(i, k, i, k -1 , s)
        succ.append(s)
    return succ

#swaps the given elements of given state and returns a new state
def swap(i1,j1,i2,j2,state):
    new_state=deepcopy(state)
    temp=new_state[i1][j1]
    new_state[i1][j1]=new_state[i2][j2]
    new_state[i2][j2]=temp
    return new_state

#checks for goal state
def is_goal(state):
    return (state==canonical).all()

#Returns position of empty tile
def pos_n(data, n):
    var = np.where(data == n)
    i=var[0][0]
    j=var[1][0]
    return [i,j]

#Gives the move from old position to new: Eg: R12
def get_move(old,new):
    zero_new=pos_n(new,0)
    zero_old=pos_n(old,0)

    i=zero_old[0]
    j=zero_old[1]
    p=zero_new[0]
    q=zero_new[1]
    result=""

    if(i-p>0):
        result+="D"
        result+=str(abs(i-p))
        result+=str(j)

    elif(i-p<0):
        result+="U"
        result+=str(abs(i-p))
        result+=str(j)

    elif(j-q>0):
        result+="R"
        result+=str(abs(j-q))
        result+=str(i)

    elif(j-q<0):
        result+="L"
        result+=str(abs(j-q))
        result+=str(i)

    else:
        result+="---"

    return result

def cost_2(s):
    i=0
    a=deepcopy(s)
    while (previous[to_tuple(a)][0]==0).all():
        a=previous[to_tuple(a)]
        i+=1

    return i

def g(s):
    if is_goal(s):
        return 0
    else:return 1


#Checks if element is in the in intended row and col
def check_r_c(element, r, c):
    index=np.where(canonical==element)
    if (not (index[0][0]==r) and not(index[1][0]==c) ):
        return True
    return False

def heuristic_2(s):
    sum=0
    for r in range(1,16):
        old=pos_n(s,r)
        new=pos_n(canonical,r)

        manhattan=abs(old[0]-new[0])+abs(old[1]-new[1])
        sum+=manhattan

    sum=sum/3.0

    x=linear_conflict(s)
    sum=sum+x

    return math.ceil(sum)

#Checks number of linear conflict
#Concept from https://heuristicswiki.wikispaces.com/Linear+Conflict
def linear_conflict(s):

    heuristic=0
    for r in range(0,len(s)):
        for c in range(0,3):
            if s[r][c]!=0:
# If row of element is same as its canonical row
                if pos_n(canonical,s[r][c])[0]==r:
                    for k in range(c+1,4):
                        if (pos_n(canonical,s[r][k])[0]==r)and s[r][k]!=0:
                            if s[r][c]>s[r][k]:
                                heuristic+=2

# If column of element is same as its canonical column
                if pos_n(canonical,s[r][c])[1]==c:
                    for k in range(r+1,4):
                        if (pos_n(canonical,s[k][c])[1]==c) and (s[r][k]!=0):
                            if s[r][c]>s[k][c]:
                                heuristic+=2
    return heuristic


def path(s,init):
    path123=" "
    if (s==init).all():
        return ""
    return path(previous[to_tuple(s)][0],init)+get_move(previous[to_tuple(s)][0],s)+" "

#Search Algo_3
def solver(init_state):
    previous[to_tuple(init_state)]=[init_state,0]
    add_task(to_tuple(init_state),heuristic_2(init_state))

    while len(pq_fringe)>0:

        curr_state=pop_task()
        closed.append(curr_state)
#        prev_state=previous[curr_state][0]
        curr_state=np.asarray(curr_state)

        if is_goal(curr_state):
            return curr_state

        b=cost_2(curr_state)
        for s in successors(curr_state):
            f=b+heuristic_2(s)

            if (to_tuple(s) in closed):
                continue

            if to_tuple(s) in pq_finder:
                entry=pq_finder[to_tuple(s)]
                if entry[0]>f:
                    remove_task(to_tuple(s))

            if not (to_tuple(s) in pq_finder):
                add_task(to_tuple(s), f)
                previous[to_tuple(s)]=[curr_state,b]

    return None

def main():
    filename = str(sys.argv[1])
    data = np.loadtxt(filename)
    data = data.astype(int)
    global initial_node
    #print linear_conflict(data)
    start=time.time()
    final_state= solver(data)
    total=time.time()-start

    print "Time-Taken: "+str(total)
    print "Visited nodes= "
    print len(closed)
    print path(final_state,data)

main()