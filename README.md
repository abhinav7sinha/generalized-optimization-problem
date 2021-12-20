### [Choosing teams](https://github.iu.edu/cs-b551-fa2021/aganapa-jdevanir-sinhabhi-a1/tree/master/part3)
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
