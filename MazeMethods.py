import pygame
from ClickableElements import MazeClick,ClickableElements
from StaticSurfs import leftBarRect



class MazeCell:
    def __init__(self):
        self.wallsList = [True,True,True,True] #(Right,Left,Up,Down)





class Maze:
    def __init__(self,surface,pos=(100,30),rows=10,cols=10,wColour=(100,200,255),bColour=(255,255,255)):
        self.surface = surface
        self.origin = pos
        self.rows = rows #how many cells long it will be 
        self.cols = cols # how many cells high it will be
        self.wColour = wColour
        self.bColour = bColour
        self.px = 20
        self.stateString = "." #stores the unique signiture of the algorithm, each step is 4bits + 16bits 
        self.cellArray = self.GenerateCellArray() #stores all cells in a 2d array
        self.currentStep = 1
        self.endStep = 1
        self.mRect = pygame.Rect(self.origin,(self.rows*20,self.cols*20))
        self.clickObj = MazeClick(self.surface,self)

    def GenerateCellArray(self):
        #generates array
        array =  [[0 for y in range(self.cols)] for x in range(self.rows)]
        #fills it with cells
        for y in range(self.cols):
            for x in range(self.rows):
                newCell = MazeCell()
                array[x][y] = newCell
        return array

    def UpdateSize(self,rows,cols):
        self.rows = rows
        self.cols = cols
        self.cellArray = self.GenerateCellArray()

    def UpdatePx(self,newpx):
        self.mRect = pygame.Rect(self.origin,(self.rows*newpx,self.cols*newpx))
        self.clickObj = MazeClick(self.origin,(self.rows*newpx,self.cols*newpx),self.surface)
        self.px = newpx

    def UpdateOrigin(self,newOrigin):
        self.mRect = pygame.Rect(newOrigin,(self.rows*self.px,self.cols*self.px))
        self.clickObj.pos = (newOrigin)
        self.origin = newOrigin

    def AddtoStateString(self,cellPos,direction): # direction followed by x and y in hex
        block = ""
        if direction == (1,0):
            block += "0"
        elif direction == (-1,0):
            block += "1"
        elif direction == (0,1):
            block += "2"
        elif direction == (0,-1):
            block += "3"
        block += hex(cellPos[0])
        block += hex(cellPos[1])
        block += "."
        self.stateString += block       

    def CountSteps(self):#counts the steps of the state string
        dots = 0
        for dot in self.stateString:
            if dot == ".":
                dots += 1
        self.endStep = dots

    def RemoveCellWalls(self,cellPos,direction): #direction is a coordinate in (x,y)
        
        currentCell = self.cellArray[cellPos[0]][cellPos[1]]
        adjacentCellCoords = (cellPos[0]+direction[0],cellPos[1]+direction[1])
        #checks if adjacentCellCoords exist
        if adjacentCellCoords[0] < self.rows and adjacentCellCoords[0] >= 0:
            if adjacentCellCoords[1] < self.cols and adjacentCellCoords[1] >= 0:
                adjacentCell = self.cellArray[adjacentCellCoords[0]][adjacentCellCoords[1]]
                match direction:
                    case (1,0):
                        adjacentCell.wallsList[1] = False
                    case(-1,0):
                        adjacentCell.wallsList[0] = False
                    case(0,1):
                        adjacentCell.wallsList[3] = False
                    case(0,-1):
                        adjacentCell.wallsList[2] = False
        match direction:
                    case (1,0):
                        currentCell.wallsList[0] = False
                    case(-1,0):
                        currentCell.wallsList[1] = False
                    case(0,1):
                        currentCell.wallsList[2] = False
                    case(0,-1):
                        currentCell.wallsList[3] = False

    def ClearMaze(self): #puts the walls back on the maze
        for y in range(self.cols):
            for x in range(self.rows):
                currentCell = self.cellArray[x][y]
                for i in range (4):
                    currentCell.wallsList[i] = True

    def ApplyStep(self,step): #applies the relevant step to the maze step goes 1->
        #extracts the relevant step#
        instruction = ""
        dotcount = 0
        for i in self.stateString:
            if i == ".":
                dotcount += 1
            if dotcount == step:
                instruction += i
        #finds the direction
        dir = ""
        match instruction[1] :
            case "0":
                dir = (1,0)
            case "1":
                dir = (-1,0)
            case "2":
                dir = (0,1)
            case "3":
                dir = (0,-1)
        #finds the position
        pos = ""
        instruction = instruction[2:]
        for i in range(len(instruction[2:])):
            if instruction[2+i] == "x":
                index = i+1
        pos = (int(instruction[:index],0),int(instruction[index:],0))
        self.RemoveCellWalls(pos,dir)

    def UpdateMazeState(self): #applies all steps from 1 to current step
        self.ClearMaze()
        for i in range(1,self.currentStep):
            self.ApplyStep(i)

    def OutputMaze(self): #displays the maze in the terminal
        #cycles through the list form top right to bottom left
        for y in range(self.cols):
            for x in range(self.rows):
                walls = 0
                currentCell = self.cellArray[x][y]
                for wall in  currentCell.wallsList:
                    if wall == True:
                        walls += 1
                print(walls, end = "    ")
            print("\n")

    def DrawMazeThin(self):

        surf = self.surface
        px = self.px
        oriX = self.origin[0]
        oriY = self.origin[1]
        wColour = self.wColour
        

        #draws background
        bRect = pygame.Rect(self.origin,(self.rows*px,self.cols*px))
        pygame.draw.rect(surf,self.bColour,bRect)

        #draws walls
        for y in range(self.cols):
            for x in range(self.rows):
                currentCell = self.cellArray[x][y]

                if currentCell.wallsList[0] == True:
                    pygame.draw.line(surf,wColour,(x*px+px+oriX-1,y*px+oriY),(x*px+px+oriX-1,y*px+px+oriY))

                if currentCell.wallsList[1] == True:
                    pygame.draw.line(surf,wColour,(x*px+oriX,y*px+oriY),(x*px+oriX,y*px+px+oriY))

                if currentCell.wallsList[3] == True:
                    pygame.draw.line(surf,wColour,(x*px+px+oriX,y*px+oriY),(x*px+oriX,y*px+oriY))
                
                if currentCell.wallsList[2] == True:
                    pygame.draw.line(surf,wColour,(x*px+px+oriX,y*px+px+oriY-1),(x*px+oriX,y*px+px+oriY-1))

    def DrawMazeThick(self):
        pass

    def MoveMaze(self):
        disp = self.clickObj.mouseDisp
        mousepos = pygame.mouse.get_pos()
        self.UpdateOrigin((mousepos[0]-disp[0],mousepos[1]-disp[1]))
        self.clickObj.mouseDisp = disp
    ###somehow get all of this into clickable elements file
    def ClickHandler(self):
        noNoBox = ClickableElements((leftBarRect[0],leftBarRect[1]+30),(leftBarRect[2],leftBarRect[3]))
        self.clickObj.RegisterClick()
        if self.clickObj.clicked == True:
            self.selected = True
            self.clickObj.clicked = False
        if self.clickObj.Hovering() == False and pygame.mouse.get_pressed()[0] == True and noNoBox.Hovering() == False:
            self.selected = False
        if self.selected == True and pygame.mouse.get_pressed()[0] == True and noNoBox.Hovering() == False:
            self.MoveMaze()
        
        
        if self.selected == True:

            originX = self.origin[0]
            originY = self.origin[1]

            pygame.draw.line(self.surface,(255,0,0),(originX+self.rows*self.px-1,originY),(originX+self.rows*self.px-1,originY+self.cols*self.px-1)) # fix
            pygame.draw.line(self.surface,(255,0,0),(originX,originY),(originX,originY+self.cols*self.px-1))
            pygame.draw.line(self.surface,(255,0,0),(originX,originY),(originX+self.rows*self.px-1,originY,))
            pygame.draw.line(self.surface,(255,0,0),(originX,originY+self.cols*self.px-1),(originX+self.rows*self.px-1,originY+self.cols*self.px-1))
        
        
