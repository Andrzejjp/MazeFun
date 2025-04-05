import pygame
from ClickableElements import MazeClick

class Maze:
    def __init__(self,surface,pos=(110,10),rows=10,cols=10,wColour=(100,200,255),bColour=(255,255,255)):
        self.surface = surface
        self.origin = pos
        self.rows = rows #how many cells long it will be 
        self.cols = cols # how many cells high it will be
        self.wColour = wColour
        self.bColour = bColour
        self.px = 20
        self.genString = "." #stores the generated maze  
        self.solveString = "." #stores the solution to the maze
        self.adjacencyMatrix = None # data structure that stores a the maze (0,0)=top left (m,n)=bottom right 
        self.solutionAdjacencyMatrix = None
        self.GenerateAdjacencyMatrix()
        self.gStep = 1
        self.sStep = 1
        self.mRect = pygame.Rect(self.origin,(self.cols*20,self.rows*20))
        self.clickObj = MazeClick(self.surface,self)
        self.gAlg = None
        self.sAlg = None

    def UpdateSize(self,rows,cols):

        self.rows = rows
        self.cols = cols

        self.GenerateAdjacencyMatrix(2)
        self.clickObj.box = (self.cols*self.px,self.rows*self.px)
        self.clickObj.rect = pygame.Rect(self.origin,self.clickObj.box)
        
    def UpdatePx(self,newpx):
        self.mRect = pygame.Rect(self.origin,(self.rows*newpx,self.cols*newpx))
        self.clickObj = MazeClick(self.origin,(self.rows*newpx,self.cols*newpx),self.surface)
        self.px = newpx

    def UpdateOrigin(self,newOrigin):
        self.mRect = pygame.Rect(newOrigin,(self.rows*self.px,self.cols*self.px))
        self.clickObj.rect = pygame.Rect((newOrigin[0],newOrigin[1]),(self.clickObj.rect[2],self.clickObj.rect[3]))
        self.origin = newOrigin

    def AddtoString(self,type,vertex1,vertex2): # adds instrucion to genString or solveString
        if type == "g":
            self.genString += str(vertex1)+","+str(vertex2)+"."
        elif type == "s":
            self.solveString += str(vertex1)+","+str(vertex2)+"."
        
    def GetEndStep(self,type): # finds the total steps
        dots = 0
        if type == "g":

            for dot in self.genString:
                if dot == ".":
                    dots += 1
        
        elif type == "s":

            for dot in self.solveString:
                if dot == ".":
                    dots += 1

        return (dots)
    
    def GenerateAdjacencyMatrix(self,type=2,whose="g"):#  1 = path,2 = wall,0 = no connection type = 1 or = 2
        rows = self.rows
        cols = self.cols
        vertices  = rows*cols

        if type > 2 or type < 1:
            raise TypeError("adjacency matrix can only use 1 or 2")


        
        #generates an un-connected graph
        adjacencyMatrix = [[0 for output in range(vertices)] for input in range(vertices)]

        for i in range(0,vertices):
            #finds 4 neigbours around
            if (i-cols) > -1: # up
                adjacencyMatrix[i][i-cols] = type
            if (i%cols) != cols-1:# right
                adjacencyMatrix[i][i+1] = type
            if (i%cols) != 0: # left
                adjacencyMatrix[i][i-1] = type
            if i < vertices-cols: # down
                adjacencyMatrix[i][i+cols] = type
        if whose == "g":
            self.adjacencyMatrix = adjacencyMatrix
        elif whose == "s":
            self.solutionAdjacencyMatrix = adjacencyMatrix

    def ApplyString(self,type,steps,filler=False): #applies from step 1 to "steps"

        if type == "g":
            self.GenerateAdjacencyMatrix()
        elif type == "s":
            self.GenerateAdjacencyMatrix(2,"s")

        if steps > self.GetEndStep(type):
            steps = self.GetEndStep(type)

        if type == "g":
           codeString = self.genString
        elif type == "s":
            codeString = self.solveString
        
        # extracts desired instruction
        for step in range(1,steps+1): 

            dots = 0
            index1 = None
            index2 = None
            for i in range(len(codeString)):
                if codeString[i] == ".":
                    dots+=1
                
                if dots == step and index1 == None:
                    index1 = i
                if dots == step+1 and index2 == None:
                    index2 = i

                if dots > step:
                    break
                
            instruction = codeString[(index1+1):index2]

            for i in range(len(instruction)):

                if instruction[i] == ",":
                    vertex1 = int(instruction[0:i])
                    vertex2 = int(instruction[i+1:len(instruction)])
                    if type == "g":
                        self.adjacencyMatrix[vertex1][vertex2] = 1
                        self.adjacencyMatrix[vertex2][vertex1] = 1
                    
                    if type == "s"and filler == False:
                        self.solutionAdjacencyMatrix[vertex1][vertex2] = 1
                        self.solutionAdjacencyMatrix[vertex2][vertex1] = 1
                    elif type == "s" and filler == True:
                        self.solutionAdjacencyMatrix[vertex1][vertex2] = 3
                        self.solutionAdjacencyMatrix[vertex2][vertex1] = 3

    def OutputMaze(self): #displays the maze in the terminal
        #cycles through the list form top right to bottom left
        for y in range(self.rows):
            for x in range(self.cols):
                walls = 0
                currentVertex = self.adjacencyMatrix[x+y*self.cols]
                for neighbours in  currentVertex:
                    if neighbours == 2:
                        walls += 1
                print(walls, end = "    ")
            print("\n")

    def OutputAM(self): # displays the Adjacency Matrix in the terminal
        for y in range(self.cols*self.rows):
            for x in range(self.rows*self.cols):
                print(self.adjacencyMatrix[x][y],end= "    ")
            print("\n")

    def DrawMazeThin(self):

        
        #draws background
        surf = self.surface
        px = self.px
        height = self.rows
        length = self.cols

        bRect = pygame.Rect(self.origin,(length*px,height*px))
        pygame.draw.rect(surf,self.bColour,bRect)

        #draws walls
        
        vertices = height*length
        wColour = self.wColour
        originX = self.origin[0]
        originY = self.origin[1]

        pygame.draw.line(surf,wColour,(originX,originY),(originX+px*length,originY),2)
        pygame.draw.line(surf,wColour,(originX+px*length,originY),(originX+px*length,originY+px*height),2)
        pygame.draw.line(surf,wColour,(originX+px*length,originY+px*height),(originX,originY+px*height),2)
        pygame.draw.line(surf,wColour,(originX,originY+px*height),(originX,originY),2)
        
        for i in range(0,vertices):
            x = i%length
            y = i//length
            
            # makes a wall for up and right
            if (i-length) > -1: # up
                if self.adjacencyMatrix[i][i-length] == 2:
                    pygame.draw.line(surf,wColour,(originX+px*x,originY+px*y),(originX+px*(x+1),originY+px*y),2)
                    
            if (i%length) != length-1:# right
                if self.adjacencyMatrix[i][i+1] == 2:
                    pygame.draw.line(surf,wColour,(originX+px*(x+1),originY+px*y),(originX+px*(x+1),originY+px*(y+1)),2)

    def DrawMazeThick(self):
        pass

    def DrawSolution(self):
        surf = self.surface
        px = self.px
        height = self.rows
        length = self.cols

        vertices = height*length
        wColour = (0,255,0)
        originX = self.origin[0]
        originY = self.origin[1]

        for i in range(0,vertices):
            x = i%length
            y = i//length
            
            # makes a wall for up and right
            if (i-length) > -1: # up
                if self.solutionAdjacencyMatrix[i][i-length] == 1:
                    vertexPos = (originX+px*x+px//2,originY+px*y+px//2)
                    neigbourPos = (originX+px*x+px//2,originY+px*(y-1)+px//2)

                    pygame.draw.line(surf,wColour,vertexPos,neigbourPos,2)
                    
            if (i%length) != length-1:# right
                if self.solutionAdjacencyMatrix[i][i+1] == 1:
                    vertexPos = (originX+px*x+px//2,originY+px*y+px//2)
                    neigbourPos = (originX+px*(x+1)+px//2,originY+px*y+px//2)
                    
                    pygame.draw.line(surf,wColour,vertexPos,neigbourPos,2)
            
            # makes a wall for up and right
            if (i-length) > -1: # up
                if self.solutionAdjacencyMatrix[i][i-length] == 3:
                    pygame.draw.line(surf,wColour,(originX+px*x,originY+px*y),(originX+px*(x+1),originY+px*y),2)
                    
            if (i%length) != length-1:# right
                if self.solutionAdjacencyMatrix[i][i+1] == 3:
                    pygame.draw.line(surf,wColour,(originX+px*(x+1),originY+px*y),(originX+px*(x+1),originY+px*(y+1)),2)
                    
    def MoveMaze(self):
        disp = self.clickObj.mouseDisp
        mousepos = pygame.mouse.get_pos()
        self.UpdateOrigin((mousepos[0]-disp[0],mousepos[1]-disp[1]))
        self.clickObj.mouseDisp = disp


