

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
        c = destination
        print(destination)
        while c != start:
            c = parent[c]
            print(c)
        c = parent[c]
        print(c)

