import pygame
from queue import Queue
from MazeMethods import Maze
from ClickableElements import Button,Slider,DropBox
from MazeGenerators import *
from MazeSolvers import *

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
    "click on the New button to create your first maze",
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
sizeXS = Slider(win,(10,400),(80,5),"sizeX",32,1,15)
sizeYS = Slider(win,(10,435),(80,5),"sizeY",32,1,15)

# GenerateMaze() Elements


gAlgorithmSelectorD = DropBox(win,(10,45),(80,20),"Generate",["DepthFirst"],13)

# SolveMaze() Elements
solveAlgoB = Button(win,(10,155),(80,20),"solveAlgo",10)

sAlgorithmSelectorD = DropBox(win,(10,180),(80,20),"Solve",["BreadthFirst"],13)

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
        sizeXS.SetValue(selectedMaze.rows)
        sizeYS.SetValue(selectedMaze.cols)
        gAlgorithmSelectorD.currentOption = selectedMaze.gAlg
        sAlgorithmSelectorD.currentOption = selectedMaze.sAlg

    sizeXS.Draw()
    if sizeXS.Clicked() == True: # when let go do below
        selectedMaze.stateString = "."
        selectedMaze.UpdateCurrentStep(1)
        gAlgorithmSelectorD.currentOption = None
        selectedMaze.gAlg = None
        sAlgorithmSelectorD.currentOption = None
        selectedMaze.sAlg = None
    if sizeXS.clicking == True:
        selectedMaze.UpdateSize(sizeXS.ReturnValue(),selectedMaze.cols)
        selectedMaze.solveString = "."


    sizeYS.Draw()
    if sizeYS.Clicked() == True: #when let go do below
        selectedMaze.stateString = "."
        selectedMaze.UpdateCurrentStep(1)
        gAlgorithmSelectorD.currentOption = None
        selectedMaze.gAlg = None
        sAlgorithmSelectorD.currentOption = None
        selectedMaze.sAlg = None
    if sizeYS.clicking == True:
        selectedMaze.UpdateSize(selectedMaze.rows,sizeYS.ReturnValue())
        selectedMaze.solveString = "."

        



    if gAlgorithmSelectorD.Clicked() == True:
        if gAlgorithmSelectorD.open == False:
            selectedMaze.gAlg = gAlgorithmSelectorD.currentOption
            AlgorithmManager(0,gAlgorithmSelectorD.currentOption,selectedMaze)
    if gAlgorithmSelectorD.open == True: # disable buttons
        pass
    else: # reenable buttons
        pass
    gAlgorithmSelectorD.Draw()


def SolveMaze(selectedMaze): # everything to prepare solve mode

    if sAlgorithmSelectorD.Clicked() == True:
        if sAlgorithmSelectorD.open == False:
            if selectedMaze.currentStep > 4 and selectedMaze.currentStep == selectedMaze.endStep:
                selectedMaze.sAlg = sAlgorithmSelectorD.currentOption
                AlgorithmManager(1,sAlgorithmSelectorD.currentOption,selectedMaze)
            
            else:
                sAlgorithmSelectorD.currentOption = None
                ErrorMessage("maze must be fully generated to be solved")

    if gAlgorithmSelectorD.open == True: # disable buttons
        pass
    else: #reenable buttons
        pass
    sAlgorithmSelectorD.Draw()

def AlgorithmManager(mode,algorithm,maze): # prepares algorithm for maze 

    match mode:
        case 0: # generating mazes 

            maze.stateString = "."
            maze.ClearMaze()
            cellPosX = round(maze.rows/2)
        
            maze.AddtoStateString((cellPosX,0),(0,-1)) # makes entrance

            # algorithms contained within
            
            match algorithm:
                case 0: # depth first
                    vList= []
                    DepthFirst(maze,(round(maze.rows/2),0),vList)
                
                case _: # default case
                    
                    maze.gAlg = None
                    gAlgorithmSelectorD.currentOption = None

            

            # ^^^^^^^^^^^^^^^^
            
            maze.AddtoStateString((cellPosX,maze.cols-1),(0,1)) # makes exit
            maze.UpdateEndStep()
            maze.UpdateCurrentStep(maze.endStep)
            maze.solveString = "."
            maze.sAlg = None
            sAlgorithmSelectorD.currentOption = None

        case 1: # solving mazes

            selectedMaze.UpdateEndStep()
            selectedMaze.UpdateCurrentStep(selectedMaze.endStep)
            maze.solveString = "."

            # algorithms contained within

            match algorithm:
                case 0: # breadth first 

                    maze.GenerateAdjacencyMatrix()
                    nodes = maze.rows*maze.cols
                    q = Queue(nodes)
                    d = []
                    p = []
                    for i in range(nodes):
                        d.append(False)
                        p.append(False)
                    BreadthFirstSearch(round(maze.rows/2),round(nodes-maze.rows/2),q,d,p,False,maze)
                
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
        maze.DrawSolution()
        
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
    if newMazeB.Clicked():
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