#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: Abhinav Sinha, sinhabhi
# Anitha Ganapathy, aganapa
# Jyothsna Devaiah Devanira, jdevanir
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
#

import sys
import copy
import random as rm
import concurrent.futures
from math import e


def parseFile(input_file):
    '''
    This function takes a filename as an input and returns a dictionary
    of dictionaries as output.
    It contains memName, memTeamTrue, and memTeamFalse for all the students in
    the input_file
    '''
    requestedGroups = {}
    with open(input_file, "r") as f:
        f_contents = f.read().rstrip("\n").split("\n")
        for i in range(len(f_contents)):
            memName = f_contents[i].split(' ')[0]
            memGroupTrue = f_contents[i].split(' ')[1].split('-')
            memGroupFalse = f_contents[i].split(' ')[2].split(',')
            memGroupReq = {
                'memName': memName, 'memGroupTrue': sorted(memGroupTrue),
                'memGroupFalse': sorted(memGroupFalse)}
            requestedGroups[i] = memGroupReq
    return requestedGroups


def sortMemList(requestedGroups):
    '''
    This is a precomputation to sort the input student list such that the
    students who have requested the most people to work with
    are in the beginning of the list
    '''
    mems = []
    for key, value in requestedGroups.items():
        mem = str(len(value['memGroupTrue'])) + ' ' + value['memName']
        mems.insert(0, mem)
    mems.sort(reverse=True)
    for i in range(len(mems)):
        mems[i] = mems[i].split(' ')[1]
    return mems


def groupSizeCheck(groups, requestedGroups):
    '''
    Calculate number of students who were not assigned their requested group
    size
    '''
    noMatch = 0
    for h in range(len(requestedGroups)):
        for i in range(len(groups)):
            if requestedGroups[h]['memName'] in groups[i]:
                if len(requestedGroups[h]['memGroupTrue']) != len(groups[i]):
                    noMatch += 1
    return noMatch


def groupTrueMemCheck(groups, requestedGroups):
    '''
    Calculate number of students who were not assigned to someone they
    requested
    '''
    noMatch = 0
    for h in range(len(requestedGroups)):
        for i in range(len(groups)):
            if requestedGroups[h]['memName'] in groups[i]:
                noMatch += listCompareTrue(
                    requestedGroups[h]['memGroupTrue'], groups[i])
    return noMatch


def groupFalseMemCheck(groups, requestedGroups):
    '''
    Calculate number of students who were assigned to someone they requested
    not to work with
    '''
    noMatch = 0
    for h in range(len(requestedGroups)):
        for i in range(len(groups)):
            if requestedGroups[h]['memName'] in groups[i]:
                noMatch += listCompareFalse(
                    requestedGroups[h]['memGroupFalse'], groups[i])
    return noMatch


def listCompareTrue(list1, list2):
    count = 0
    for a in list1:
        if a not in list2 and a != 'xxx' and a != 'zzz':
            count += 1
    return count


def listCompareFalse(list1, list2):
    count = 0
    for a in list1:
        if a in list2:
            count += 1
    return count


def cost(groups, requestedGroups):
    '''
    I assign weights to the 4 components based on the time time it takes the
    instructors to manage them a. number of groups - 5 b. number of students
    who were not assigned their requested group size - 2 c. number of students
    who were not assigned to someone they requested - 0.05*60 d. Number of
    students who were assigned to someone they requested not to work with - 10
    '''
    time_1 = 5 * len(groups)
    time_2 = 2 * groupSizeCheck(groups, requestedGroups)
    time_3 = 0.05 * 60 * groupTrueMemCheck(groups, requestedGroups)
    time_4 = 10 * groupFalseMemCheck(groups, requestedGroups)
    total_time = time_1 + time_2 + time_3 + time_4
    return total_time


def getFutureStates(member, group, requestedGroups):
    '''
    To find all possible states, I calculate all the possible partitions of
    the set of students such that the maximum number of students in a subset
    is 3. I do this by starting with one student, say 'a'. I add a new student
    'b' and calculate all the possible sets for the 2 students. The key idea
    here is that the new student can either go inside an existing subset, or
    go into a new subset. So the new state space is: [[['a','b']], [['a'],
    ['b']]]. Now we aadd a third student 'c' as follows: 1. inside:
    ['a', 'b', 'c'] or ['a', 'c'] or ['b', 'c']. 2. outside: ['c'].
    So the new state space becomes: [[['a', 'b', 'c']], [['a', 'c'], [b]],
     [['b', 'c'], [a]], [['a'], ['b'], ['c']]] and so on. I do this till all
     the students have been added. Problem here is that the number of
     partitions increases very quickly as we add new elements.
     And this leads to an exponential increase in time and space complexity
     for computations. So, I decided use the Beam search technique and keep
     a fixed number of states in the fringe.
    '''
    outside = []
    group.pop(0)
    for i in range(len(group)):
        if(len(group[i])) < 3:
            inside = copy.deepcopy(group)
            inside[i].append(member)
            inside.insert(0, cost(inside, requestedGroups))
            yield(inside)
    outside = copy.deepcopy(group)
    outside.append([member])
    outside.insert(0, cost(outside, requestedGroups))
    yield(outside)


def updateFringeSmall(member, groupsList, requestedGroups, maxFringe):
    fringe = []
    mincost = -1
    while groupsList:
        for groups in getFutureStates(
                member, groupsList.pop(0), requestedGroups):
            if len(fringe) < maxFringe:
                if fringe == []:
                    fringe.append(groups)
                    mincost = groups[0]
                elif groups[0] <= mincost:
                    mincost = groups[0]
                    fringe.append(groups)
                else:
                    fringe.append(groups)
            else:
                break
        fringe.sort()
    print(len(fringe))
    return fringe

# Simulated-Annealing


def updateFringe_SA(member, groupsList, requestedGroups, maxFringe, memNos,
                    placedMemNos):
    fringe = []
    mincost = -1
    while groupsList:
        for groups in getFutureStates(
                member, groupsList.pop(0), requestedGroups):
            if fringe == []:
                fringe.append(groups)
                mincost = groups[0]
            elif placedMemNos < 10:
                if len(fringe) < maxFringe:
                    fringe.append(groups)
                else:
                    break
            else:
                if len(fringe) < maxFringe:
                    if groups[0] <= mincost:
                        mincost = min(mincost, groups[0])
                        fringe.append(groups)
                    elif rm.random() < e**(
                            -(groups[0]-mincost)/(memNos-placedMemNos)):
                        fringe.append(groups)
                    else:
                        fringe.append(groups)
                else:
                    break
        fringe.sort()
    return fringe


def search(input_file, maxFringe):
    # Read input file
    requestedGroups = parseFile(input_file)

    # Create list of members in class
    memList = sortMemList(requestedGroups)
    memNos = len(memList)

    # Set initial fringe
    firstGroup = [memList.pop()]
    fringe = [[cost(firstGroup, requestedGroups), firstGroup]]
    if(memNos < 11):
        while(memList):
            fringe = updateFringeSmall(
                memList.pop(), fringe, requestedGroups, maxFringe)
    else:
        while(memList):
            placedMemNos = memNos-len(memList)
            fringe = updateFringe_SA(
                memList.pop(), fringe, requestedGroups, maxFringe, memNos,
                placedMemNos)
    return fringe


def buildOutputDict(groups):
    cost = groups.pop(0)
    groupList = [None]*len(groups)
    result = {}
    for i in range(len(groups)):
        groupList[i] = ''
        for j in range(len(groups[i])):
            if(groupList[i] == ''):
                groupList[i] += groups[i][j]
            else:
                groupList[i] += '-'+groups[i][j]
            groupList[i].strip('-')
    result.update({"assigned-groups": groupList, "total-cost": cost})
    return result


def solver(input_file):
    """
    1. This function should take the name of a .txt input file in the format
     indicated in the assignment.
    2. It should return a dictionary with the following keys:
        - "assigned-groups" : a list of groups assigned by the program, each
         consisting of usernames separated by hyphens
        - "total-cost" : total cost (time spent by instructors in minutes) in
         the group assignment
    3. Do not add any extra parameters to the solver() function, or it will
     break our grading and testing code.
    4. Please do not use any global variables, as it may cause the testing code
     to fail.
    5. To handle the fact that some problems may take longer than others,
     and you don't know ahead of time how much time it will take to find the
      best solution, you can compute a series of solutions and then
       call "yield" to return that preliminary solution. Your program can
        continue yielding multiple times; our test program will take the last
         answer you 'yielded' once time expired.
    """
    # Setup:
    finalCost = []
    # Read input file
    requestedGroups = parseFile(input_file)

    # Create list of members in class
    memList = sortMemList(requestedGroups)
    memNos = len(memList)

    # Set list of maxFringeLengths
    maxFringeList = [25, 50, 100, 500, 1000, 2000, 3000, 10000]

    # Set initial fringe
    firstGroup = [memList.pop()]
    fringe = [[cost(firstGroup, requestedGroups), firstGroup]]

    # Start search:

    if memNos < 11:
        fringe = search(input_file, 10000)
        yield(buildOutputDict(fringe.pop(0)))
    else:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = [
                executor.submit(search, input_file, maxFringe)
                for maxFringe in maxFringeList]
            for f in concurrent.futures.as_completed(results):
                fringe = f.result()
                finalCost.append(fringe[0][0])
                finalCost.sort()
                if(fringe[0][0] <= finalCost[0]):
                    yield(buildOutputDict(fringe.pop(0)))


if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):
        print(
            "----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])
