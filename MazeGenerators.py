import random 
def CheckVisits(grid,pos):
    count = 0
    if grid.mapArray[pos[0]+1][pos[1]] == 0:
        count += 1
    if grid.mapArray[pos[0]-1][pos[1]] == 0:
        count += 1
    if grid.mapArray[pos[0]][pos[1]+1] == 0:
        count += 1
    if grid.mapArray[pos[0]][pos[1]-1] == 0:
        count += 1
    if count <= 1:
        return True
    else:
        return False
    




def DepthFirst(grid,startPos):
    grid.OutputGrid()
    print()
    directionArray = [(1,0),(-1,0),(0,1),(0,-1)]
    grid.mapArray[startPos[0]][startPos[1]] = 0
    #Picks a direction to travel in
    while len(directionArray) != 0:
        directionIndex = random.randint(0,len(directionArray)-1)
        directon = directionArray[directionIndex]
        newPos = (startPos[0]+directon[0],startPos[1]+directon[1])
        #checks if its in the grid or if already been
        if newPos[0] < grid.rows and newPos[0] >= 0:
            if newPos[1] < grid.cols and newPos[1] >= 0:
                if grid.mapArray[newPos[0]][newPos[1]] == 1:
                    #checks for cycles
                    if CheckVisits(grid,newPos) == True:
                        DepthFirst(grid,newPos)

                else:
                    directionArray.pop(directionIndex)
            else:
                directionArray.pop(directionIndex)
        else:
            directionArray.pop(directionIndex)
                


    

    