import pygame
import random
from queue import Queue
from MazeMethods import Maze
from ClickableElements import Button,Slider,DropBox
from MazeGenerators import *
from MazeSolvers import *
from queue import LifoQueue

winSize = (1400,700)
FPS = 0
running = True
clock = pygame.time.Clock()
pygame.display.init()
win = pygame.display.set_mode((winSize[0], winSize[1]))
pygame.display.set_caption("MazeMaker")
pygame.font.init()

mazeList = []

Error = None
# User Help stuff
helpB = Button(win,(10,670),(80,20),"Help",15)
helpText = [
    "Help Menu",
    "",
    "1.click on the New button to create your first maze",
    "2.click SelectG to select an algorithm and click on generate to make a maze ",
    "3.click SelectS to select an algoirthm and click solve to solve the maze",
    "",
    "CONTROLS",
    "",
    "LeftMouseButton - interact with buttons and almost everything on screen",
    "RightMouseButton - Selects a maze when hovering over one"
]

# Error stuff
errorB = Button(win,(0,0),(40,20),"Ok",15)

# Misc Elements
newMazeB = Button(win,(10,5),(80,20),"New Maze",15)
deleteB = Button(win,(10,640),(80,20),"Delete Maze",12,(200,200,200),(255,49,49))
sizeYS = Slider(win,(10,400),(80,5),"sizeX",100,2,15)
sizeXS = Slider(win,(10,435),(80,5),"sizeY",100,2,15)

# GenerateMaze() Elements
generateB = Button(win,(10,70),(80,20),"Generate",15)

gAlgorithmSelectorD = DropBox(win,(10,45),(80,20),"SelectG",["RecursiveDF","StackDF","Wilson's"],13)

# SolveMaze() Elements
solveB = Button(win,(10,205),(80,20),"Solve",15)

sAlgorithmSelectorD = DropBox(win,(10,180),(80,20),"SelectS",["BreadthFirst",],13)

selectedMaze = None

# functons
def DrawHelpScreen(): # Draws the help screen
    
    fontsize = 15
    padding = 20
    font = pygame.font.SysFont("Courier New",fontsize)
    fontColour = (0,0,0)
    winSize = win.get_size()
    textList = helpText

    longestLine = 0 
    for line in textList:
        textLength = font.size(line)[0]
        if longestLine < textLength:
            longestLine = textLength
    
    textHeight = font.size(textList[0])[1]
    bgLength = longestLine+padding*2
    bgHeight = (textHeight*len(textList))+padding*2
    backgroundRect = pygame.Rect((winSize[0]//2-(bgLength//2),winSize[1]//2-(bgHeight//2)),(bgLength,bgHeight))
    
    textSurfList = []
    for i in range(len(textList)):
        textSurfList.append(font.render(textList[i],True,fontColour))
    
    underlaySurf = pygame.Surface((winSize[0],winSize[1]))
    underlaySurf.fill((1,1,1))
    pygame.Surface.set_colorkey(underlaySurf,(0,0,0))
    pygame.Surface.set_alpha(underlaySurf,230)
    pygame.Surface.blit(win,underlaySurf,(0,0))

    pygame.draw.rect(win,(255,255,255),backgroundRect)

    for i in range(len(textSurfList)):
        pygame.Surface.blit(win,textSurfList[i],(backgroundRect[0]+padding,backgroundRect[1]+padding+textHeight*i))
    
def ErrorMessage(message): # creates error messages

    fontsize = 15
    padding = 30
    font = pygame.font.SysFont("Courier New",fontsize)
    fcolour = (255,0,0)
    winSize = win.get_size()
    text = "ERROR: "+message

    textSize = font.size(text)
    backroundRect = pygame.Rect((winSize[0]//2-(textSize[0]+padding)//2,winSize[1]//2-(textSize[1]+padding)//2),(textSize[0]+padding,textSize[1]+padding+errorB.rect[3]))
    textSurf = font.render(text,True,fcolour)
    pos = (winSize[0]//2-textSize[0]//2,winSize[1]//2-textSize[1]//2)
    errorB.rect = pygame.Rect((winSize[0]//2-errorB.rect[2]//2,winSize[1]//2+textSize[1]//2+padding//4),(errorB.rect[2],errorB.rect[3]))
    global Error
    Error = (backroundRect,textSurf,pos)

def DrawStaticSurfs(surface,selectedMaze):

    surfSize = surface.get_size()

    leftBarRect = pygame.Rect(((0,0),(100,surfSize[1])))
    topBarRect = pygame.Rect(((0,0),(surfSize[0],30)))

    surface.fill((220,220,220))
    pygame.draw.rect(surface,("#FFFFFF"),leftBarRect)
    # pygame.draw.rect(surface,("#F5F5F5"),topBarRect)

    #bars for ui
    padding = 10
    if selectedMaze != None:
        pygame.draw.line(surface,(160,160,160),(leftBarRect[0]+padding,35),(leftBarRect[0]+leftBarRect[2]-padding,35),3)
        pygame.draw.line(surface,(160,160,160),(leftBarRect[0]+padding,170),(leftBarRect[0]+leftBarRect[2]-padding,170),3)
    
def GenerateMaze(selectedMaze): # everything to prepare generate mode
    if selectedMaze.clickObj.CheckSelect() == True:
        sizeYS.SetValue(selectedMaze.rows)
        sizeXS.SetValue(selectedMaze.cols)
        gAlgorithmSelectorD.currentOption = selectedMaze.gAlg
        sAlgorithmSelectorD.currentOption = selectedMaze.sAlg

    if generateB.Clicked() == True:
        if gAlgorithmSelectorD.currentOption == None:
            ErrorMessage("Try selecting an algorithm from the DropBox above the Generate Button")
        selectedMaze.gAlg = gAlgorithmSelectorD.currentOption
        AlgorithmManager(0,gAlgorithmSelectorD.currentOption,selectedMaze)
    generateB.Draw()

    gAlgorithmSelectorD.Clicked()
    if gAlgorithmSelectorD.open == True: # disable buttons
        generateB.active = False
        generateB.clicking = True
        
    else: # reenable buttons
        generateB.active = True
    gAlgorithmSelectorD.Draw()

    # animate the maze drawing
    if selectedMaze.gStep < selectedMaze.GetEndStep("g"):
        selectedMaze.ApplyString("g",selectedMaze.gStep)
        selectedMaze.gStep += 1

def SolveMaze(selectedMaze): # everything to prepare solve mode
    if solveB.Clicked():
        if sAlgorithmSelectorD.currentOption == None:
            ErrorMessage("Try selecting an algorithm from the DropBox above the Solve Button")

        elif 2 < selectedMaze.GetEndStep("g"):
            selectedMaze.sAlg = sAlgorithmSelectorD.currentOption
            AlgorithmManager(1,sAlgorithmSelectorD.currentOption,selectedMaze)
            
        else:
            sAlgorithmSelectorD.currentOption = None
            ErrorMessage("maze must be fully generated to be solved")
        
    solveB.Draw()

    sAlgorithmSelectorD.Clicked()

    if sAlgorithmSelectorD.open == True: # disable buttons
        solveB.active = False
        solveB.clicking = True
    
    else: #re-enable buttons
        solveB.active = True
    sAlgorithmSelectorD.Draw()

    #animates solution to maze
    if selectedMaze.sStep < selectedMaze.GetEndStep("s"):
        selectedMaze.ApplyString("s",selectedMaze.sStep)
        selectedMaze.sStep += 1
    if selectedMaze.sAlg != None:
        selectedMaze.DrawSolution()

def AlgorithmManager(mode,algorithm,maze): # prepares algorithm for maze 

    match mode:
        case 0: # generating mazes 

            maze.genString = "."
            maze.gStep = 1

            # algorithms contained within
            
            match algorithm:
                case 0: # recursive depth first
                    if maze.rows > 32 or maze.cols > 32:
                        ErrorMessage("Cannot use the RecursiveDepthFirst algorithm when maze is larger than 32*32")
                    else:

                        randomVertex = random.randint(0,maze.rows*maze.cols-1)
                        visitedList = []
                        adjacencyMatrix = maze.adjacencyMatrix

                        RecursiveDepthFirst(randomVertex,visitedList,adjacencyMatrix,maze)
                
                case 1: # stack depth first
                    randomVertex = random.randint(0,maze.rows*maze.cols-1)
                    adjacencyMatrix = maze.adjacencyMatrix
                    visitedList = []
                    stack = LifoQueue()

                    StackDepthFirst(randomVertex,adjacencyMatrix,visitedList,stack,maze)
                
                case 2: # Wilson's Algorithm
                    randomVertex = random.randint(0,maze.rows*maze.cols-1)
                    adjacencyMatrix = maze.adjacencyMatrix
                    randomVertex2 = None
                    while True:
                        randomVertex2 = random.randint(0,maze.rows*maze.cols-1)
                        if randomVertex != randomVertex2:
                            break

                    WilsonsAlgorithm(adjacencyMatrix,[randomVertex],maze)
                
                case _: # default case
                    
                    maze.gAlg = None
                    gAlgorithmSelectorD.currentOption = None

            # ^^^^^^^^^^^^^^^^
            maze.solveString = "."
            maze.ApplyString("s",maze.GetEndStep("s"))

        case 1: # solving mazes

            maze.solveString = "."
            maze.sStep = 1

            # algorithms contained within

            match algorithm:
                case 0: # breadth first 

                    nodes = maze.rows*maze.cols
                    q = Queue(nodes)
                    d = []
                    p = []
                    for i in range(nodes):
                        d.append(False)
                        p.append(False)
                    BreadthFirstSearch(0,nodes-1,q,d,p,False,maze)
                
                case 1: # dead end filler
                    nodes = maze.rows*maze.cols
                    adjacencyMatrix = maze.adjacencyMatrix

                    DeadEndFilling(0,nodes-1,adjacencyMatrix,maze)
                
                case _: # default Case
                    maze.sAlg = None
                    sAlgorithmSelectorD.currentOption = None
    
            # ^^^^^^^^^^^^^^^^^
            


############################################################################################################################
while running:

    DrawStaticSurfs(win,selectedMaze)

    for maze in mazeList:
        maze.DrawMazeThin()
        maze.clickObj.RegisterClick()
        
        #enforces 1 maze to be selected at a time
        selectedCount = 0
        if maze.clickObj.selected == True and maze != selectedMaze:
            selectedMaze = maze
            for maze in mazeList:
                if maze != selectedMaze:
                    maze.clickObj.selected = False
                if maze.clickObj.selected == True:
                    selectedCount += 1
        if selectedCount > 1:
            selectedMaze = None
        if selectedMaze != None and selectedMaze.clickObj.selected == False:
            selectedMaze = None
        
    #rearranges mazeList so the selected maze is drawn last
    if selectedMaze != None:
        for i in range(len(mazeList)):
            if selectedMaze == mazeList[i]:
                mazeList.append(mazeList[i])
                mazeList.pop(i)
    # generates a new maze
    if newMazeB.Clicked(): # Newmaze button click event
        mazeList.append(Maze(win))
        if len(mazeList) > 1 :
            mazeList[-2].clickObj.selected = False
        selectedMaze = mazeList[-1]

        mazeList[-1].clickObj.selected = True
        sizeXS.SetValue(selectedMaze.rows)
        sizeYS.SetValue(selectedMaze.cols)
        gAlgorithmSelectorD.currentOption = None
        sAlgorithmSelectorD.currentOption = None
    newMazeB.Draw()


    if selectedMaze != None: # does something when a maze is selected
    
        GenerateMaze(selectedMaze)

        SolveMaze(selectedMaze)

        sizeYS.Draw()
        if sizeYS.Clicked() == True: # when let go do below
            selectedMaze.stateString = "."
            gAlgorithmSelectorD.currentOption = None
            selectedMaze.gAlg = None
            sAlgorithmSelectorD.currentOption = None
            selectedMaze.sAlg = None
        if sizeYS.clicking == True:
            selectedMaze.UpdateSize(sizeYS.ReturnValue(),selectedMaze.cols)
            selectedMaze.solveString = "."
            selectedMaze.ApplyString("g",selectedMaze.gStep)
            selectedMaze.ApplyString("s",selectedMaze.sStep)

        sizeXS.Draw()
        if sizeXS.Clicked() == True: #when let go do below
            selectedMaze.stateString = "."
            gAlgorithmSelectorD.currentOption = None
            selectedMaze.gAlg = None
            sAlgorithmSelectorD.currentOption = None
            selectedMaze.sAlg = None
        if sizeXS.clicking == True:
            selectedMaze.UpdateSize(selectedMaze.rows,sizeXS.ReturnValue())
            selectedMaze.solveString = "."
            selectedMaze.ApplyString("g",selectedMaze.gStep)
            selectedMaze.ApplyString("s",selectedMaze.sStep)

        # deletes a maze if button is clicked
        if selectedMaze != None:
            if deleteB.Clicked():
                    mazeList.pop(len(mazeList)-1)
                    selectedMaze = None
            deleteB.Draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # error message handler
    if Error != None:
        
        #sets up the decreased opacity background
        underlaySurf = pygame.Surface((winSize[0],winSize[1]))
        underlaySurf.fill((1,1,1))
        pygame.Surface.set_colorkey(underlaySurf,(0,0,0))
        pygame.Surface.set_alpha(underlaySurf,230)
        pygame.Surface.blit(win,underlaySurf,(0,0))
        
        pygame.draw.rect(win,(255,255,255),Error[0])
        pygame.Surface.blit(win,Error[1],Error[2])

        if errorB.Clicked() == True:
            Error = None
        errorB.Draw()

    # help screen
    if helpB.Clicked() == True:
        if helpB.text == "Close":
            helpB.text = "Help"
        else:
            helpB.text = "Close"

    if helpB.text == "Close":
        DrawHelpScreen()
    helpB.Draw()



    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()