import random 

def CheckVisits(grid,pos):
    #checks how many neighbours a cell has (checks the 8 sourunding cells)
    neighbours = 0
    for i in range(-1,2):
        for j in range(-1,2):
            if i != 0 and j != 0:

                if pos[0]+i < 0 or pos[0]+i > grid.rows-1 or pos[1]+j < 0 or pos[1]+j > grid.cols-1:
                    neighbours += 1
                
                elif grid.mapArray[pos[0]+i][pos[1]+j] == grid.pathChar:
                    neighbours += 1

    if neighbours <= 1:
        return True
    return False
    




def DepthFirst(grid,startPos):

    directionArray = [(1,0),(-1,0),(0,1),(0,-1)]
    grid.mapArray[startPos[0]][startPos[1]] = grid.pathChar

    #Picks a direction to travel in
    while len(directionArray) != 0:
        directionIndex = random.randint(0,len(directionArray)-1)
        directon = directionArray[directionIndex]
        newPos = (startPos[0]+directon[0],startPos[1]+directon[1])

        #checks if its in the grid or if already been
        if newPos[0] < grid.rows and newPos[0] >= 0:
            if newPos[1] < grid.cols and newPos[1] >= 0:
                if grid.mapArray[newPos[0]][newPos[1]] == grid.wallChar:
                    #checks for cycles
                    if CheckVisits(grid,newPos) == True:
                        DepthFirst(grid,newPos)
                    directionArray.pop(directionIndex)

                else:
                    directionArray.pop(directionIndex)
            else:
                directionArray.pop(directionIndex)
        else:
            directionArray.pop(directionIndex)
                


    

    