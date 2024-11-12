import pygame

class MazeCells:
    def __init__(self,size,pos,colour):
        self.size = size #length of square
        self.pos = pos #top left of the square 
        self.colour = colour
        self.wallslist = (True,True,True,True) #(Right,Left,Up,Down)





class Maze:
    def __init__(self,rows,cols):
        self.rows = rows #how many cells long it will be 
        self.cols = cols # how many cells high it will be
        self.cellArray =             #stores all cells in a 2d array

    def GenerateCellArray(self):
        pass






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
