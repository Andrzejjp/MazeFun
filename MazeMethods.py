import pygame
class Maze:
    def __init__(self,rows,cols):
        self.rows = rows
        self.cols = cols
        self.pathChar = "."
        self.wallChar = "W"
        #creates the 2d array for storing the maze
        self.mapArray =  [[self.wallChar for y in range(cols)] for x in range(rows)]
    
    def OutputGrid(self):
        for y in range(self.cols):
            for x in range(self.rows):
                print(self.mapArray[x][y], end = "    ")
            print("\n")

    def DrawGrid(self,surface,square):
        squareColour = (100,150,200)
        for y in range(self.cols):
            for x in range(self.rows):
                if self.mapArray[x][y] == self.pathChar:
                    pygame.draw.rect(surface,squareColour,pygame.Rect((x*square,y*square),(square,square)))
