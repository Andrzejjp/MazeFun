

def BreadthFirstSearch(start,destination,queue,discoveredList,parent,found,maze):
    solveList =[]
    queue.put(start)
    discoveredList[start] = True
    found = False
    while queue.empty() != True and found == False:
        node = queue.get()
        for i in range(maze.rows*maze.cols):
            if maze.adjacencyMatrix[node][i] == 1:
                if discoveredList[i] == False and found == False:
                    queue.put(i)
                    discoveredList[i] = True
                    parent[i] = node
                    if i == destination:
                        found = True
    
    if found == True:
        temp = destination
        solveList.append(destination)
        while temp != start:
            temp = parent[temp]
            solveList.append(temp)
    
    #transforms the solve list to be read in by maze class
    for i in range(1,len(solveList)):
        maze.AddtoString("s",solveList[i-1],solveList[i])

def DeadEndFilling(start,destination,adjacencyMatrix,maze):
    finish = False
    while finish == False:
        #find a dead end 
        for i in range(0,len(adjacencyMatrix)-1):
            ends = 0
            deadEndIndex = None
            for j in range(0,len(adjacencyMatrix)-1):
                
                if i != start or i!= destination or j!= start or j!= destination:

                    if adjacencyMatrix[i][j] == 1:
                        ends += 1
                        deadEndIndex = i
            
            if ends == 1:
                maze.AddtoString("s",deadEndIndex,j)
                break

        finish = True
    
