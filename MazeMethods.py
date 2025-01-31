import pygame

class MazeCell:
    def __init__(self):
        self.wallsList = [True,True,True,True] #(Right,Left,Up,Down)





class Maze:
    def __init__(self,surface,pos,rows,cols,wColour=(20,20,100),bColour=(100,100,20)):
        self.surface = surface
        self.origin = pos
        self.rows = rows #how many cells long it will be 
        self.cols = cols # how many cells high it will be
        self.wColour = wColour
        self.bColour = bColour
        self.px = 20
        self.stateString = "." #stores the unique signiture of the algorithm, each step is 4bits + 16bits 
        self.cellArray = self.GenerateCellArray() #stores all cells in a 2d array

    def GenerateCellArray(self):
        #generates array
        array =  [[0 for y in range(self.cols)] for x in range(self.rows)]
        #fills it with cells
        for y in range(self.cols):
            for x in range(self.rows):
                newCell = MazeCell()
                array[x][y] = newCell
        return array

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

    def ApplySteps(self,step): #applies the relavent step to the maze step goes 1->
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

    def ClearMaze(self): #puts the walls back on the maze 
        for y in range(self.cols):
            for x in range(self.rows):
                currentCell = self.cellArray[x][y]
                for i in range (4):
                    currentCell.wallsList[i] = True

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
        #draws background
        bRect = pygame.Rect(self.origin,(self.rows*self.px,self.cols*self.px))
        pygame.draw.rect(self.surface,self.bColour,bRect)

        #draws walls
        for y in range(self.cols):
            for x in range(self.rows):
                currentCell = self.cellArray[x][y]

                if currentCell.wallsList[0] == True:
                    pygame.draw.line()

                if currentCell.wallsList[1] == True:
                    pygame.draw.line()

                if currentCell.wallsList[3] == True:
                    pygame.draw.line()
                
                if currentCell.wallsList[2] == True:
                    pygame.draw.line()

    def DrawMazeThick(self):
        pass

