import random 


def RecursiveDepthFirst(startingVertex,visitedList,adjacencyMatrix):
    currentVertex = startingVertex
    visitedList.append(currentVertex)

    neigboursList = []
    for i in range(0,len(adjacencyMatrix)):

        if adjacencyMatrix[currentVertex][i] != 0: #searches only the neighbours
            neigboursList.append(i)

    while len(neigboursList) != 0:
        
        while True:
            randomIndexinNeigboursList = random.randint(0,len(neigboursList)-1)
            randomNeigbour = neigboursList[randomIndexinNeigboursList]
            if (randomNeigbour in visitedList) == False:
                adjacencyMatrix[currentVertex][randomNeigbour] = 1 # updates the array
                adjacencyMatrix[randomNeigbour][currentVertex] = 1
                RecursiveDepthFirst(randomNeigbour,visitedList,adjacencyMatrix)
                break
            else:
                neigboursList.pop(randomIndexinNeigboursList)
                break

def StackDepthFirst(startingVertex,adjacencyMatrix,visitedList,stack):

    visitedList.append(startingVertex)
    stack.put(startingVertex)

    while stack.empty() == False:
        currentVertex = stack.get()

        unvisitedNeigboursList = []
        for i in range(0,len(adjacencyMatrix)):
            
            if adjacencyMatrix[currentVertex][i] != 0: #searches only the neighbours

                if (i in visitedList) == False: # checks if visited
                    unvisitedNeigboursList.append(i)
                
        if len(unvisitedNeigboursList) != 0:
            randomNeigbour = unvisitedNeigboursList[random.randint(0,len(unvisitedNeigboursList)-1)]
            stack.put(currentVertex)
            adjacencyMatrix[currentVertex][randomNeigbour] = 1 # updates the array
            adjacencyMatrix[randomNeigbour][currentVertex] = 1
            visitedList.append(randomNeigbour)
            stack.put(randomNeigbour)

def WilsonsAlgorithm(adjacencyMatrix,mazeList):

    while len(mazeList) < len(adjacencyMatrix):

        while True:
            currentVertex = random.randint(0,len(adjacencyMatrix)-1)

            if (currentVertex in mazeList) == False:
                break
        
        walkList = []
        while (currentVertex in mazeList) == False:
            walkList.append(currentVertex)

            #finds the neigbours of the current cell
            neigboursList = []
            for i in range(0,len(adjacencyMatrix)):

                if adjacencyMatrix[currentVertex][i] != 0 and (i in walkList) == False:
                    neigboursList.append(i)
            
            if len(neigboursList) != 0:
                randomNeigbour = neigboursList[random.randint(0,len(neigboursList)-1)]
                currentVertex = randomNeigbour

                if (randomNeigbour in mazeList) == True:

                    indexOfConnection = mazeList.index(randomNeigbour)
                    walkList.append(mazeList[indexOfConnection])

                    for i in range(1,len(walkList)):
                        adjacencyMatrix[walkList[i]][walkList[i-1]] = 1
                        adjacencyMatrix[walkList[i-1]][walkList[i]] = 1

                    walkList.pop()
                    mazeList.extend(walkList)
            
            else:
                break

    