

def BreadthFirstSearch(start,destination,queue,discoveredList,parent,found,maze):
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
        maze.AddtoSolveString(destination)
        while temp != start:
            temp = parent[temp]
            maze.AddtoSolveString(temp)
