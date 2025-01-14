import pygame

class MazeCell:
    def __init__(self,size,pos,colour):
        self.size = size #length of square
        self.pos = pos #top left of the square 
        self.colour = colour
        self.wallsList = [True,True,True,True] #(Right,Left,Up,Down)
        self.cellRect = pygame.Rect((pos[0],pos[1]),(size,size))





class Maze:
    def __init__(self,surface,pos,rows,cols):
        self.surface = surface
        self.origin = pos
        self.rows = rows #how many cells long it will be 
        self.cols = cols # how many cells high it will be
        self.stateString = "." #stores the unique signiture of the algorithm
        self.step = 1
        self.end = 0 
        self.cellArray = self.GenerateCellArray(20,(255,255,255)) #stores all cells in a 2d array

    def GenerateCellArray(self,cellSize,colour):
        #generates array
        array =  [[0 for y in range(self.cols)] for x in range(self.rows)]
        #fills it with cells
        for y in range(self.cols):
            for x in range(self.rows):
                newCell = MazeCell(cellSize,(x*cellSize+self.origin[0],y*cellSize+self.origin[1]),colour)
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

    def CountSteps(self):#counts the steps of the state string
        dots = 0
        for dot in self.stateString:
            if dot == ".":
                dots += 1
        self.end = dots

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

    def DrawMazeThin(self,cellColour,wallColour):
        for y in range(self.cols):
            for x in range(self.rows):
                currentCell = self.cellArray[x][y]
                pygame.draw.rect(self.surface,cellColour,currentCell.cellRect)

                if currentCell.wallsList[0] == True:
                    pygame.draw.line(self.surface,wallColour,((currentCell.size-1)+x*currentCell.size+self.origin[0],y*currentCell.size+self.origin[1]),((currentCell.size-1)+x*currentCell.size+self.origin[0],(currentCell.size-1)+y*currentCell.size+self.origin[1]))

                if currentCell.wallsList[1] == True:
                    pygame.draw.line(self.surface,wallColour,(x*currentCell.size+self.origin[0],y*currentCell.size+self.origin[1]),(x*currentCell.size+self.origin[0],(currentCell.size-1)+y*currentCell.size+self.origin[1]))

                if currentCell.wallsList[3] == True:
                    pygame.draw.line(self.surface,wallColour,(x*currentCell.size+self.origin[0],y*currentCell.size+self.origin[1]),((currentCell.size-1)+x*currentCell.size+self.origin[0],y*currentCell.size+self.origin[1]))
                
                if currentCell.wallsList[2] == True:
                    pygame.draw.line(self.surface,wallColour,(x*currentCell.size+self.origin[0],(currentCell.size-1)+y*currentCell.size+self.origin[1]),((currentCell.size-1)+x*currentCell.size+self.origin[0],(currentCell.size-1)+y*currentCell.size+self.origin[1]))

    def DrawMazeThick(self,cellColour,WallColour):
        pass

