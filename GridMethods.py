class Grid:
    def __init__(self,length,width):
        self.length = length
        self.width = width

        #creates the 2d array for storing the maze
        mapArray =  [[0 for x in range(length)] for y in range(width)]
        
        #Generates a border around the maze
        for x in range(length-1):
            mapArray[x][0] = 1
            mapArray[x][width-1] = 1
        for y in range(width):
            mapArray[0][y] = 1
            mapArray[length-1][y] = 1 
        self.mapArray = mapArray
    
    def OutputGrid(self):
        for x in range(self.length):
            for y in range(self.width):
                print(self.mapArray[x][y], end = ",")
            print("\n")    