### [Part 3: Choosing teams](https://github.iu.edu/cs-b551-fa2021/aganapa-jdevanir-sinhabhi-a1/tree/master/part3)
***

### Problem Analysis
 ==================

#### Problem Statement:

In a certain Computer Science course, students are assigned to groups according to preferences that they specify. Unfortunately - and as we already discovered while assigning teams for Assignment 1 : the student preferences may not be compatible with each other: student A may request working with student B, but B may request not to work with A, for example. Students are going to complain, so the course staff decides to minimize their own work. They estimate that the following 4 components will determine the total time spent by the course staff: 1. number of groups, 2 number of students who were not assigned their requested group size, 3. number of students who were not assigned to someone they requested and 4. Number of students who were assigned to someone they requested not to work with.

The goal is to write a program to find an assignment of students to teams that minimizes the total amount of work the staff needs to do, subject to the constraint that no team may have more than 3 students.

#### Inputs:

Input-file is a text file that contains each student's response to these questions on a single line, separated by spaces
ex:
sahmaini sahmaini _
sulagaop sulagaop-xxx-xxx _
fanjun fanjun-xxx nthakurd
nthakurd nthakurd djcran,fanjun
vkvats vkvats-sahmaini _

#### Expected Output:

A list of valid groups (each named
according to the students in the group, separated by hyphens), and the total cost (time spent by instructors in minutes)
ex:
["djcran-vkvats-nthakurd", "sahmaini", "sulagaop-fanjun"]

#### Command:

<code> python3 ./assign.py [input-file] </code>

***
### Final Output
  =============

The output is as follows:

#### 1. Test 1
    Input:
    djcran djcran-vkvats-nthakurd sahmaini
    sahmaini sahmaini _
    sulagaop sulagaop-xxx-xxx _
    fanjun fanjun-xxx nthakurd
    nthakurd nthakurd djcran,fanjun
    vkvats vkvats-sahmaini _

 ####  Output:
  {'assigned-groups': ['nthakurd-sahmaini-sulagaop', 'fanjun-vkvats-djcran'], 'total-cost': 24.0}

#### 2. Test 2
    Input:
    djcran djcran-vkvats-nthakurd sahmaini
    sahmaini sahmaini _
    sulagaop sulagaop-xxx-xxx _
    fanjun fanjun-xxx nthakurd
    nthakurd nthakurd djcran,fanjun
    vkvats vkvats-sahmaini _
    zhao zhao-qian-xxx _
    qian qian-xxx-xxx zhao
    sun sun-qian-xxx zhao
    li li-sun-qian _
    zhou zhou-xxx zhao
    wu wu-xxx zhou
    zheng zheng-li-xxx _

#### Output:
    {'assigned-groups': ['nthakurd-wu', 'sahmaini-zhao-zheng', 'fanjun-zhou', 'vkvats-djcran-sulagaop', 'li-qian-sun'], 'total-cost': 43.0}

#### 3. Test 3
    Input:
    djcran djcran-vkvats-nthakurd sahmaini
    sahmaini sahmaini _
    sulagaop sulagaop-zzz-zzz _
    fanjun fanjun-zzz nthakurd
    nthakurd nthakurd djcran,fanjun
    vkvats vkvats-sahmaini _
    zhao zhao-qian-zzz _
    qian qian-zzz-zzz zhao
    sun sun-qian-zzz zhao
    li li-sun-qian _
    zhou zhou-zzz zhao
    wu wu-zzz zhou
    zheng zheng-li-wang zhang
    wang wang-zzz zhao
    feng feng-zhao _
    chen chen-zzz _
    zhang3 zhang3-zzz-zzz _
    li4 li4-zhang3-zzz _
    wang5 wang5-fanjun-zzz _
    zhang zhang-zzz-zzz _

#### Output:
  {'assigned-groups': ['nthakurd-li4-qian', 'sahmaini-sulagaop-sun', 'chen-fanjun', 'feng-wu-zhao', 'vkvats-djcran-li', 'wang-zhou-zheng', 'wang5-zhang-zhang3'], 'total-cost': 76.0}

***

### Info:
1. In this problem, what is the branching factor of the search tree?
- The program is designed to find the a combination of students such that the cost function "cost(groups, requestedGroups)" is minimum.
- State Space: The state space is the set of all possible partitions of the set of students such that no subset can have more than 3 students.
- Successor Function: To find all possible states, I calculate all the possible partitions of the set of students such that the maximum number of students in a subset is 3. I do this by starting with one student, say 'a'. I add a new student 'b' and calculate all the possible sets for the 2 students. The key idea here is that the new student can either go inside an existing subset, or go into a new subset. So the new state space is: [[['a','b']], [['a'], ['b']]]. Now we aadd a third student 'c' as follows: 1. inside: ['a', 'b', 'c'] or ['a', 'c'] or ['b', 'c']. 2. outside: ['c']. So the new state space becomes:
[[['a', 'b', 'c']], [['a', 'c'], [b]], [['b', 'c'], [a]], [['a'], ['b'], ['c']]] and so on.
I do this till all the students have been added. Problem here is that the number of partitions increases very quickly as we add new elements. And this leads to an exponential increase in time and space complexity for computations. So, I decided use the Beam search technique and keep a fixed number of states in the fringe.
- Cost funtion: I assign weights to the 4 components based on the time time it takes the instructors to manage them
  a. number of groups - 5
  b. number of students who were not assigned their requested group size - 2
  c. number of students who were not assigned to someone they requested - 0.05*60
  d. Number of students who were assigned to someone they requested not to work with - 10
- Goal state: The goal state is when a state has all the students in it, and the cost function is minimum.
- Search algorithm: I use Simulated Annealing Local Search algorithm to find the local minimum of the cost function. For smaller input sizes, I crawl through the entire state space, so the code finds the optimum solution. For larger inputs, I put a limit on the number of states in the fringe. For simulated Annealing, here's the exponent I use:
e**(-(groups[0]-mincost)/(memNos-placedMemNos))
groups[0]: it has the cost of new state
mincost: minimum cost of the states I have searched so far
memNos: total number of students in the input file
placedMemNos: number of students that have been added in the state space already
So as we go deeper into our search tree, T (which is memNos-placedMemNos) keep decreasing.
- I use multiprocessing to launch multiple searches with a different limit on the fringe size. I yield the output as soon as a search finishes.

### References:
1. Set Partitions: https://en.wikipedia.org/wiki/Partition_(number_theory)

***



## Part 1: Navigation
## Program 1
- This program is designed to find an optimum path between Pichu and the observer.
- Set of valid states: It contains all the coordinates where Pichu can travel. According to the problem it is the location of all the '.'
- Successor function: It returns all the states that Pichu can go to from it's current location. Here, it can go either one row up, or one row down, or one column right or one column left. Additionally it can only go to a location which is empty i.e '.'. There are walls in the map 'X', where Pichu cannot go.
- Cost function: It is uniform for all valid moves.
- Goal state definition: It is defined as the state where Pichu and observer meet. Here, the goal state is when 'p' reaches '@'
- Initial state: The initial state is given in the files map1.txt and map2.txt. In both these maps 'p' is placed at an arbitrary distance from '@'. There are '.' and 'X' surrounding them.
- The existing program uses Depth First Search to find the optimum path between the observer and Pichu. This is characterized by the Stack implementation of fringe. The last node to go to the fringe is the first one to come out.
- Why does the program often fail tofind a solution? The program goes inside an infinite loop and gets stuck there. It adds and then removes the same set of nodes from the fringe repeatedly.

## Solution 1
- The solution to the problem is A* search. By defining a consistent heuristic - Manhattan distance, and using Search Algorithm #3, I have overcome the problem of the program going into infinite loops. The solution to the problem is optimal.
- The fringe is implemented as a stack. We use append function to append new node to it and pop function to remove a node.
- The fringe has 4 parameters: 1. Current position of Pichu, 2. Distance travelled by Pichu, 3. Path covered by Pichu to reach current position, 4.Heuristic function of current position
- A dictionary 'visited' is used to store all the visited nodes and the distance travelled to reach it.

## Part 2: Hide-and-seek
## Program 2
- This program is designed to arrange the given number of pichus in a map so that they cannot see each other. Unlike the first program where pichus could only travel vertically and horizontally, in this program the pichus can see vertically, horizontally AND DIAGONALLY.
- The existing program uses the Depth First Search algorithm to place pichus in the desired locations. But it fails to do so, because it doesn't clearly define the goal state, or the successor function to include conditions where pichus can see each other.

## Solution 2
- To fix the program, I defined the goal state to have all the pichus placed such that no two pichus were in the same row, column or diagonal.
- To make the porgram faster, instead of defining the checks in the goal state, I added the checks in the Successor function itself.
- In the Successor function, I only return new states, where the new pichu cannot see another pichu in the same row, column or diagonal.
- I've used Depth First Search technique to find the goal state in this program.
- State Space: It contains all the maps containing 1 to k number of pichus in the given MXN grid.
- Initial State: It is a map containing just one Pichu at a given location in the grid.
- Goal state: The goal state is the map containing the given 'k' number of 'p' such that no two 'p' in the same row, column or diagonal have ONLY empty spaces ('.') between them.
- Successor function: It takes a map as an input and returns a list containing all the maps with a new pichu such that no two pichus in the same row, column or diagonal have ONLY empty spaces ('.') between them.
- Cost function: Cost function is irrelevant. It is uniform.
