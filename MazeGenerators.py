import random 


def RecursiveDepthFirst(startingVertex,visitedList,adjacencyMatrix,maze):
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
                maze.AddtoString("g",currentVertex,randomNeigbour) # updates genString
                RecursiveDepthFirst(randomNeigbour,visitedList,adjacencyMatrix,maze)
                break

            else:
                neigboursList.pop(randomIndexinNeigboursList)
                break

def StackDepthFirst(startingVertex,adjacencyMatrix,visitedList,stack,maze):

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
            maze.AddtoString("g",currentVertex,randomNeigbour) # updates genString
            visitedList.append(randomNeigbour)
            stack.put(randomNeigbour)

def WilsonsAlgorithm(adjacencyMatrix,mazeList,maze):

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
                        maze.AddtoString("g",walkList[i],walkList[i-1]) # updates genString

                    walkList.pop()
                    mazeList.extend(walkList)
            
            else:
                break

    