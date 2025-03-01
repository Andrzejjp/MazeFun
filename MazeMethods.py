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
        self.clickObj.box = (self.rows*self.px,self.cols*self.px)

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

    def UpdateEndStep(self):#Calculates and assingnes the value of self.endStep
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

    def MakeEntrance(self): #once an algorithim has been applied this remove to walls along the edges
        cellPosX = round(self.rows/2)
        
        self.AddtoStateString((cellPosX,0),(0,-1))
        self.AddtoStateString((cellPosX,self.cols-1),(0,1))

    def ClearMaze(self): #puts the walls back on the maze
        for y in range(self.cols):
            for x in range(self.rows):
                currentCell = self.cellArray[x][y]
                for i in range (4):
                    currentCell.wallsList[i] = True
    def ConvertFromStateString(self,step):
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
        return pos,dir
        
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

    def UpdateCurrentStep(self,step): #applies all steps from 1 to current step
        self.UpdateEndStep()
        if 1 <= step and self.endStep >= step:
            self.currentStep = step
        else:
            raise TypeError("step Value is outside the range")
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

    def AlgorithmOverlay(self,pColour=(255,0,0),cColour=(0,0,255),fColour=(0,255,0)):#creates nice colours to show the algorithm better
        overlaySurf = pygame.Surface((self.rows*self.px,self.cols*self.px),)
        #adds to the overlay
        for i in range(1,self.currentStep):
            pos = self.ConvertFromStateString(i)[0]
            cellRect = pygame.Rect((pos[0]*self.px,pos[1]*self.px),(self.px,self.px))
            pygame.draw.rect(overlaySurf,pColour,cellRect)
        if self.endStep-self.currentStep > 0:
            pos = self.ConvertFromStateString(self.currentStep)[0]
            cellRect = pygame.Rect((pos[0]*self.px,pos[1]*self.px),(self.px,self.px))
            pygame.draw.rect(overlaySurf,cColour,cellRect)

            pos = self.ConvertFromStateString(self.currentStep+1)[0]
            cellRect = pygame.Rect((pos[0]*self.px,pos[1]*self.px),(self.px,self.px))
            pygame.draw.rect(overlaySurf,fColour,cellRect)

        #sets up the overlay
        pygame.Surface.set_colorkey(overlaySurf,(0,0,0))
        pygame.Surface.set_alpha(overlaySurf,100)
        pygame.Surface.blit(self.surface,overlaySurf,self.origin)

