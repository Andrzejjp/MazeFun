import random 



def DepthFirst(maze,pos,visitedList):
    visitedList.append(pos)
    directionArray = [(1,0),(-1,0),(0,1),(0,-1)]
    #picks a direction to travel in 
    while len(directionArray) != 0:
            directionIndex = random.randint(0,len(directionArray)-1)
            direction = directionArray[directionIndex]
            newPos = (pos[0]+direction[0],pos[1]+direction[1])
            #checks if direction is valid 
            if newPos[0] < maze.rows and newPos[0] >= 0:
                if newPos[1] < maze.cols and newPos[1] >= 0:
                    #checks if the cell has been visited
                    visited = False
                    for item in visitedList:
                         if item == newPos:
                              visited = True
                    if visited == False:
                         
                         maze.RemoveCellWalls(pos,direction)
                         DepthFirst(maze,newPos,visitedList)
                
            directionArray.pop(directionIndex)

    

    