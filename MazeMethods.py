import pygame

class MazeCell:
    def __init__(self,size,pos,colour):
        self.size = size #length of square
        self.pos = pos #top left of the square 
        self.colour = colour
        self.wallsList = [True,True,True,True] #(Right,Left,Up,Down)
        self.cellRect = pygame.Rect((pos[0],pos[1]),(size,size))





class Maze:
    def __init__(self,rows,cols):
        self.rows = rows #how many cells long it will be 
        self.cols = cols # how many cells high it will be
        self.cellArray = self.GenerateCellArray(16,(255,255,255)) #stores all cells in a 2d array

    def GenerateCellArray(self,cellSize,colour):
        #generates array
        array =  [[0 for y in range(self.cols)] for x in range(self.rows)]
        #fills it with cells
        for y in range(self.cols):
            for x in range(self.rows):
                newCell = MazeCell(cellSize,(x*cellSize,y*cellSize),colour)
                array[x][y] = newCell
        return array
    
    def RemoveAdjacentCellWalls()
    

    def OutputMaze(self):
        #cycles through the list form top right to bottom left
        for y in range(self.cols):
            for x in range(self.cols):
                walls = 0
                currentCell = self.cellArray[x][y]
                for wall in  currentCell.wallsList:
                    if wall == True:
                        walls += 1
                print(walls, end = "    ")
            print("\n")








    #def OutputGrid(self):
    #    for y in range(self.cols):
    #        for x in range(self.rows):
    #            print(self.mapArray[x][y], end = "    ")
    #        print("\n")

    #def DrawGrid(self,surface,square):
    #    squareColour = (100,150,200)
    #    for y in range(self.cols):
    #        for x in range(self.rows):
    #            if self.mapArray[x][y] == self.pathChar:
    #                pygame.draw.rect(surface,squareColour,pygame.Rect((x*square,y*square),(square,square)))
