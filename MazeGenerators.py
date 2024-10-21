import random 
def DepthFirst(grid,startPos,visitedList):
    visitedList.append(startPos)
    # has bias for directions
    for i in range(-1,2,2):
        for visited in visitedList:
            if visited == (startPos[0]+i,startPos[1]):
                DepthFirst(grid,(startPos[0]+i,startPos[1]),visitedList)

    