from collections import deque



def createMazeDict(nXCells, nYCells, cellDim):

    aDict = {}

    for i in range(nXCells):

        for j in range(nYCells):

            aDict[(i,j)] = {'position': (cellDim * i, cellDim * j), 'neighbors': [], 'visited': False, 'cost': 0}

    return aDict



    pass



nXCells, nYCells, cellDim = 2, 2, 10

mazeDict = createMazeDict(nXCells, nYCells, cellDim)

print(mazeDict)







def addAllNeighbors(mazeDict, nXCells, nYCells):

    for (coord, data) in mazeDict.items():

        if (coord[0] - 1, coord[1]) in mazeDict:

            data["neighbors"].append((int(coord[0]) - 1, coord[1]))

        if (coord[0], coord[1] + 1) in mazeDict:

            data["neighbors"].append((coord[0], coord[1] + 1))

        if (coord[0] + 1, coord[1]) in mazeDict:

            data["neighbors"].append((coord[0] + 1, coord[1]))

        if (coord[0], coord[1] - 1) in mazeDict:

            data["neighbors"].append((coord[0], coord[1] - 1))

    return mazeDict







mazeDict = createMazeDict(nXCells, nYCells, cellDim)

mazeDict = addAllNeighbors(mazeDict, nXCells, nYCells)

print(mazeDict)



def getRobotOrientation(heading):

    while heading > 360:

        heading = heading - 360

    if heading > 315 or heading < 45:

        return "E"

    elif heading > 45 and heading < 135:

        return "N"

    elif heading > 135 and heading < 225:

        return "W"

    elif heading > 225 and heading < 315:

        return "S"

    pass

"""

print(getRobotOrientation(361))

print(getRobotOrientation(88.5))

"""



def getPotentialNeighbors(currentCell, orientation):

    if orientation == "N":

        return [(currentCell[0]-1, currentCell[1]), (currentCell[0], currentCell[1]+1), (currentCell[0] + 1, currentCell[1]), (currentCell[0], currentCell[1]-1)]

    if orientation == "W":

        return [(currentCell[0], currentCell[1]-1), (currentCell[0]-1, currentCell[1]), (currentCell[0], currentCell[1]+1), (currentCell[0] + 1, currentCell[1])]

    if orientation == "S":

        return [(currentCell[0] + 1, currentCell[1]), (currentCell[0], currentCell[1]-1), (currentCell[0]-1, currentCell[1]), (currentCell[0], currentCell[1]+1)]

    if orientation == "E":

        return [(currentCell[0], currentCell[1]+1), (currentCell[0] + 1, currentCell[1]), (currentCell[0], currentCell[1]-1), (currentCell[0]-1, currentCell[1])]

    pass



"""

print(getPotentialNeighbors((0,1),"E"))

print(getPotentialNeighbors((2,3),"S"))

"""





def isValidCell(cellIndices, nXCells, nYCells):

    (a,b) = cellIndices

    return 0 < a < nXCells and 0 < b < nYCells

    pass

"""

print(isValidCell((3,3), 4, 5))

print(isValidCell((1,2), 2, 2))

"""





def getWallConfiguration(IR0,IR3,IR6,threshold):

    if 4095/(IR0 + 1) <= threshold:

        l = True

    else:

        l = False

    if 4095/(IR3 + 1) <= threshold:

        f = True

    else:

        f = False

    if 4095/(IR6 + 1) <= threshold:

        r = True

    else:

        r = False

    return [l, f, r]



    pass

"""

print(getWallConfiguration(300, 200, 39, 100))

print(getWallConfiguration(23, 800, 10, 100))

"""





def getNavigableNeighbors(wallsAroundCell, potentialNeighbors, prevCell, nXCells, nYCells):

    list1 = []

    if prevCell!=None:

        list1.append(prevCell)

    if wallsAroundCell[0] == False:

        if 0 <= potentialNeighbors[0][0] < nXCells and 0 <= potentialNeighbors[0][1] < nYCells:

            list1.append((potentialNeighbors[0][0], potentialNeighbors[0][1]))

    if wallsAroundCell[1] == False:

        if 0 <= potentialNeighbors[1][0] < nXCells and 0 <= potentialNeighbors[1][1] < nYCells:

            list1.append((potentialNeighbors[1][0], potentialNeighbors[1][1]))

    if wallsAroundCell[2] == False:

        if 0 <= potentialNeighbors[2][0] < nXCells and 0 <= potentialNeighbors[2][1] < nYCells:

            list1.append((potentialNeighbors[2][0], potentialNeighbors[2][1]))

    return list1



    pass

print(getNavigableNeighbors([True, True, False], [(1,2),(2,1),(1,0),(0,1)], (0,1), 2, 2))

print(getNavigableNeighbors([False, True, False], [(0,2),(1,3),(2,2),(1,1)], (1,1), 4, 4))





def updateMazeNeighbors(mazeDict, currentCell, navNeighbors):



    for location, data in mazeDict.items():

        if currentCell in data['neighbors']:

            if location not in navNeighbors:

                mazeDict[location]['neighbors'].remove(currentCell)

        



    mazeDict[currentCell]['neighbors'] = navNeighbors

    return mazeDict



    pass





def getNextCell(mazeDict, currentCell):

    listOne = []

    listTwo = []

    for currentNeighbors in mazeDict[currentCell]['neighbors']:

        if mazeDict[currentNeighbors]['visited'] == False:

            listOne.append((currentNeighbors, mazeDict[currentNeighbors]["cost"]))

        elif mazeDict[currentNeighbors]['visited'] == True:

            listTwo.append((currentNeighbors, mazeDict[currentNeighbors]["cost"]))

    print(listTwo)

    print(listOne)

    if len(listOne) == 0:

        minCost1 = 10000000

        minIndex1 = -1

        for i, j in enumerate(listTwo):

            if j[1] < minCost1:

                minCost1 = j[1]

                minIndex1 = i

        return listTwo[minIndex1][0]

    
    minCost2 = 1000000000

    minIndex2 = -1

    for i, j in enumerate(listOne):

        if j[1] < minCost2:

            minCost2 = j[1]

            minIndex2 = i



    return listOne[minIndex2][0]



    pass



"""

mazeDict = {(0, 0): {'position': (0, 0),'neighbors': [(0, 1)], 'visited': True, 'cost': 0},

            (0, 1): {'position': (0, 1),'neighbors': [(0, 0), (1, 1)], 'visited': True, 'cost': 1},

            (1, 0): {'position': (1, 0), 'neighbors': [(1, 1)], 'visited': False, 'cost': 3},

            (0, 2): {'position': (0, 2), 'neighbors': [(0, 1), (0, 3), (1, 2)], 'visited': False, 'cost': 0},

            (1, 1): {'position': (1, 1), 'neighbors': [(1, 0), (0, 1)], 'visited': False, 'cost': 2}}

currentCell = (0,1)

print(getNextCell(mazeDict, currentCell))



mazeDict = {(0, 0): {'position': (0, 0),'neighbors': [(0, 1)], 'visited': True, 'cost': 0},

            (0, 1): {'position': (0, 1),'neighbors': [(0, 0), (1, 1)], 'visited': False, 'cost': 1},

            (1, 0): {'position': (1, 0), 'neighbors': [(1, 1)], 'visited': False, 'cost': 3},

            (1, 1): {'position': (1, 1), 'neighbors': [(1, 0), (0, 1)], 'visited': True, 'cost': 2}}

currentCell = (1,1)

print(getNextCell(mazeDict, currentCell))

"""





def checkCellArrived(currentCell, destination):

    return currentCell == destination



"""

print(checkCellArrived((4,3), (4,3)))

print(checkCellArrived((6,7), (7,6)))

"""





"""

The following implementation of the Flood Fill algorithm is

tailored for maze navigation. It updates the movement cost for

each maze cell as the robot learns about its environment. As

the robot moves and discovers navigable adjacent cells, it

gains new information, leading to frequent updates in the

maze's data structure. This structure tracks the layout and

traversal costs. With each step and discovery, the algorithm

recalculates the cost to reach the destination, adapting to

newly uncovered paths. This iterative process of moving,

observing, and recalculating continues until the robot reaches

its destination, ensuring an optimal path based on the robot's

current knowledge of the maze.

"""



from collections import deque



def updateMazeCost(mazeDict, start, goal):

    for (i,j) in mazeDict.keys():

        mazeDict[(i,j)]["flooded"] = False

    queue = deque([goal])

    mazeDict[goal]['cost'] = 0

    mazeDict[goal]['flooded'] = True

    while queue:

        current = queue.popleft()

        current_cost = mazeDict[current]['cost']

        for neighbor in mazeDict[current]['neighbors']:

            if not mazeDict[neighbor]['flooded']:

                mazeDict[neighbor]['flooded'] = True

                mazeDict[neighbor]['cost'] = current_cost + 1

                queue.append(neighbor)

    return mazeDict



"""

This function prints the information from the dictionary as

a grid and can help you troubleshoot your implementation.

"""

def printMazeGrid(mazeDict, nXCells, nYCells, attribute):

    for y in range(nYCells - 1, -1, -1):

        row = '| '

        for x in range(nXCells):

            cell_value = mazeDict[(x, y)][attribute]

            row += '{} | '.format(cell_value)

        print(row[:-1])

