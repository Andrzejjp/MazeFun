class Grid:
    def __init__(self,rows,cols):
        self.rows = rows
        self.cols = cols

        #creates the 2d array for storing the maze
        mapArray =  [[0 for y in range(cols)] for x in range(rows)]
        
        #Generates a border around the maze with a hole in the bottom middle
        for x in range(rows):
            mapArray[x][0] = 1
            mapArray[x][cols-1] = 1
        for y in range(cols):
            mapArray[0][y] = 1
            mapArray[rows-1][y] = 1
        mapArray[int((rows/2))][cols-1] = 0

        self.mapArray = mapArray
    
    def OutputGrid(self):
        for y in range(self.cols):
            for x in range(self.rows):
                print(self.mapArray[x][y], end = " , ")
            print("\n")    