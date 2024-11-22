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
    
    def OutputMaze(self):
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

    def DrawMazeThin(self,surface,cellColour,wallColour):
        for y in range(self.cols):
            for x in range(self.rows):
                currentCell = self.cellArray[x][y]
                pygame.draw.rect(surface,cellColour,currentCell.cellRect)

                if currentCell.wallsList[0] == True:
                    pygame.draw.line(surface,wallColour,((currentCell.size-1)+x*currentCell.size,y*currentCell.size),((currentCell.size-1)+x*currentCell.size,(currentCell.size-1)+y*currentCell.size))

                if currentCell.wallsList[1] == True:
                    pygame.draw.line(surface,wallColour,(x*currentCell.size,y*currentCell.size),(x*currentCell.size,(currentCell.size-1)+y*currentCell.size))

                if currentCell.wallsList[3] == True:
                    pygame.draw.line(surface,wallColour,(x*currentCell.size,y*currentCell.size),((currentCell.size-1)+x*currentCell.size,y*currentCell.size))
                
                if currentCell.wallsList[2] == True:
                    pygame.draw.line(surface,wallColour,(x*currentCell.size,(currentCell.size-1)+y*currentCell.size),((currentCell.size-1)+x*currentCell.size,(currentCell.size-1)+y*currentCell.size))

