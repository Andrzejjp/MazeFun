import pygame
class Grid:
    def __init__(self,rows,cols):
        self.rows = rows
        self.cols = cols
        #creates the 2d array for storing the maze
        self.mapArray =  [[1 for y in range(cols)] for x in range(rows)]
    
    def OutputGrid(self):
        for y in range(self.cols):
            for x in range(self.rows):
                print(self.mapArray[x][y], end = " , ")
            print("\n")

    def DrawGrid(self,surface,square):
        squareColour = (0,30,200)
        for y in range(self.cols):
            for x in range(self.rows):
                if self.mapArray[x][y] == 0:
                    pygame.draw.rect(surface,squareColour,pygame.Rect((x*square,y*square),(square,square)))
