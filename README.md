# Assignment 1 
Students name :
Jugal Shah, 
Aditya pandey,
Hanish Chidipothu
## Part 1: The 2021 Puzzle

### Problem Statement:

As per the assignment, the problem given to us is a search problem, in which we have to find the goal state from the initial state by given conditions of the tiles. In the real world, we can thought it of as a rubic cube in a 2D world. 

### State Space
State space of problem is defined as arrangment of tiles from 1 to 25 on board at any given point.

### Initial State
Initial arrangement of tiles (numbers from 1 to 25) on board.

### Successor Function and Valid state
Successor function is defined as valid moves performed on board. The board size given for this problem is 5x5. for each board position, there are 24 possible moves. 5 up, 5 down, 5 right, 5 left , 2 moves for Outer ring (CW or CCW) and 2 moves for inner ring (CW or CCW). Also states that are already visited are not valid states. 

### Goal State
Goal state for this problem is all numbers from 1 to 25 should be arranged sequentially on board. 

### Cost Function
Cost function is defined as sum of cost to reach current state and approximate heuristic cost to reach goal state from current state.

f(s) = g(s) + h(s->s*) where g(s) represents cost to reach current state from initial state and h(s) represents heuristic cost to reach to goal state from current state.

Cost to travel current state is defined as total number of moves performed from intial position to current position.

Heuristic Fucntion defined as several ways
* Number of misplaced tiles - It is defined as count of number of misplaced tiles from their target position.
* Manhatten distance from current position of tile to goal position- It is defined as manhatten distance each tile need to travel from current position to target position. Sum of manhatten distance of each tile is heuristic function.
* Inversed tiles - This Heuristic was not implented in this problem. However it is calulated as number tiles value less than current tile value on right side. For example, given number 21345 we can see that for tile number 2, tile number 1 is on right side. All other tiles are arranged correctly. So Heuristic for this would be one. 

**Why Heuristic is admissible**

A heuristic is admissible if it never overestimates the minimum cost of reaching the goal state from some node s, and its value must remain lower or equal than the cost of the shortest path from s to the goal state. The Misplaced Tiles heuristic is admissible since every tile out of place must be moved at least once in order to arrange them into the goal state. Manhatten distance is another admissible Heuristic as tile can only move one position from its current position (up, down, right or left). So Manhatten distance is always 1 and it is never going to overestimate.

### Methodology:

As it is a search problem, the first idea comes in my mind is using BFS algorithm. As it is complete and optimal. But as it is a blind search, I tend to skip that and jump to the A* search which is the combination of heuristic and the given cost. This will reduct the time of searching as well as give us the optimal solution given that we can able to find the admissible heuristic which is admissible (means not overestimating the cost)!!

We have combined different heuristics. (manhattan distance of current state to goal state of a tile + number of misplaced tiles from the goal state).

In this way, with the logic of A* search, we were able to solve the problem within a given time interval.

### Problem with high number of moves and creative way to solve it
One observation was that, in given assignment board1.txt whih required 11 moves. One thing we have observed is that, with current cost function (g(s) + h(s)), When solver goes into too deep node, it was not able to backtrck efficiently. 
We have tried following approach to solve it. However, it is noted that in current version it is not implemented as we are not sure if it is admissible or not.

Total cost = (Move Cost)^2 + (misplaced tiles + Manhatten Distance + Inversed Tiles).
It was able to solve problem board1.txt in 12 moves but it was not optimal. Idea was to penalize solver if it goes to deep into search and backtrack. 

### Additional Questions
#### In this problem, what is the branching factor of the search tree?
The board size given for this problem is 5x5. for each board position, there are 24 possible moves. 5 up, 5 down, 5 right, 5 left , 2 moves for Outer ring (CW or CCW) and 2 moves for inner ring (CW or CCW). 

So branching factor for this search tree is 24.

#### If  the  solution  can  be  reached  in  7  moves,  about  how  many  states  would  we  need  to  explore  before  wefound it if we used BFS instead of A* search?  A rough answer is fine.

The space complexity for BFS is O(b^d) where b represents branching factor and d represents depth of number of moves to travel to reach solution. 
So we need to explore approximately 24^7 states before reaching solution. 

---

## Part 2: Road Trip

### Problem Statement:

It is problem of finding optimal route between two cities for a given cost function.Cost function can be optimal number of road segments, optimal time taken, optimal distance distance and optimal delivery time from start city to the end city.

### State Space
State space of problem is defined as location of driver in a city / segments mentioned in problem at any given point.

### Initial State
Initial state is defined as driver location in start city


### Successor Function and Valid state
The successor funtion of the problem will be the given the city, what will be the direct cities connected to it in the road-segments.txt file. We are considering those cities as our successor states. In crisp words, successor cities will be all the possible cities which are directly connected to the given city. Any city / road segment that is already visited is not a valid state. We also assume all roads are bi-directional. 

### Goal State
Goal state is defined as location of driver in end city.

### Cost Function
Cost function for this problem is defined as cost required to travel from intial state to current state. Cost function can be calcualted based on defined problem. It can be either distance travelled so far, number segments visited to reach current state, time taken to reach current state or delivery time taken to reach current state. 
We have used uniform cost search method and hence, heuristic for each node is assumed to be zero. It is still admissible. 

### Methodology:

We are given with data which contains two text files. One contains city name with its coordinates and second one contains the unique pair of two cities with length of road segment, speed limit and name of the highway.

Our first task is to read these files and try to find out the discrepency in it. 

As road-segments.txt file also have highway names, its coordinate is not given in the city-gps.txt file. So, we will have to deal with it.

We have used the shortest path algorithm (dijkstra algorithm) for solving our problem. This is called as uniform cost search!! By this, we achieved our goal of optimizing the distance travelled, time taken, optimal number of road segments taken and optimal number of delivery time between two cities!!

---

## Part 3 Choosing teams

### Problem Statement:

In a certain course, students needs to assigned into group of 1,2 or 3 for their homework. Students are asked to fill survey to know their preference. Based on this survey, teams can be formed. However, it is impossible to satisfy each student needs. Wrong formation of team costs some time to course staff. Goal is to distribute students in teams such that they can be formed in teams which minimize staff's time.


### State Space

State space is defined as current groups of students in any given point. All students must be assigned to only one group and no student should left alone.

### Initial State

No groups has been formed. All students are unassigned.

### Goal state

All students are assigned to one and only one group. 

### Successor function 

Group of studnets formed with various combinations. Successor function keep assigning unassigned students into groups until no students is left.

### Cost function

Cost function defined as total time it wil take instructor to review student's complain plus grading time.
For given number of students, first group is formed using various combinations(nCr). After that best group is selected among this combinations using least cost method. Once first group selected with least cost and process is repeated for remaining students. 

### Methodology

There are several ways to design and solve this problem. This is a local search problem. We have seperated students who wanted to work in team of 2 or 3. For each successor, we will keep forming groups with minimum costs until all students are assigned into group. Total cost is reported. If it is better than previous cost, it is recorded and newly formed group becomes best group. Process will keep yielding groups and costs until program times out. However, it will only update best group if it founds better cost. 



