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
pygame.display.set_caption("MazeFun")
pygame.font.init()

mazeList = []

Error = None

# Error stuff
errorB = Button(win,(0,0),(40,20),"Ok",15)

# Misc Elements
newMazeB = Button(win,(10,5),(80,20),"New Maze",15)
deleteB = Button(win,(10,670),(80,20),"Delete Maze",12,(200,200,200),(255,49,49))
sizeXS = Slider(win,(10,400),(80,5),"sizeX",32,1,15)
sizeYS = Slider(win,(10,435),(80,5),"sizeY",32,1,15)

# GenerateMaze() Elements
addStepB = Button(win,(55,110),(30,20),"+1",15)
subStepB = Button(win,(15,110),(30,20),"-1",15)

stepS = Slider(win,(10,90),(80,5),"Step",1,1,15)

gAlgorithmSelectorD = DropBox(win,(10,45),(80,20),"Algorithm",["DepthFirst"],11)

# SolveMaze() Elements
solveAlgoB = Button(win,(10,150),(80,20),"solveAlgo",10)

# sAlgorithmSelectorD = DropBox(win,())

selectedMaze = None

# functons
def ErrorMessage(message): #prepares an error message

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
        pygame.draw.line(surface,(160,160,160),(leftBarRect[0]+padding,140),(leftBarRect[0]+leftBarRect[2]-padding,140),3)
    
def GenerateMaze(selectedMaze): # everything to prepare generate mode

    if selectedMaze.clickObj.CheckSelect() == True:
        sizeXS.SetValue(selectedMaze.rows)
        sizeYS.SetValue(selectedMaze.cols)
        stepS.SetValue(selectedMaze.currentStep)

    sizeXS.Draw()
    if sizeXS.Clicked() == True: # when let go do below
        selectedMaze.stateString = "."
        selectedMaze.UpdateCurrentStep(1)
        stepS.max = 1
        stepS.SetValue(selectedMaze.currentStep)
    if sizeXS.clicking == True:
        selectedMaze.UpdateSize(sizeXS.ReturnValue(),selectedMaze.cols)


    sizeYS.Draw()
    if sizeYS.Clicked() == True: #when let go do below
        selectedMaze.stateString = "."
        selectedMaze.UpdateCurrentStep(1)
        stepS.max = 1
        stepS.SetValue(selectedMaze.currentStep)
    if sizeYS.clicking == True:
        selectedMaze.UpdateSize(selectedMaze.rows,sizeYS.ReturnValue())

        
    stepS.Draw()
    stepS.Clicked()
    if stepS.clicking == True:
        selectedMaze.UpdateCurrentStep(stepS.ReturnValue())

    if addStepB.Clicked() and selectedMaze.endStep > selectedMaze.currentStep:
        selectedMaze.UpdateCurrentStep(selectedMaze.currentStep + 1)
        stepS.SetValue(selectedMaze.currentStep)
    addStepB.Draw()

    if subStepB.Clicked() and 1 < selectedMaze.currentStep:
        selectedMaze.UpdateCurrentStep(selectedMaze.currentStep - 1)
        stepS.SetValue(selectedMaze.currentStep)
    subStepB.Draw()

    if gAlgorithmSelectorD.Clicked() == True and gAlgorithmSelectorD.open == False and gAlgorithmSelectorD.currentOption != None:
        AlgorithmManager(0,gAlgorithmSelectorD.currentOption,selectedMaze)
    if gAlgorithmSelectorD.open == True:
        stepS.active = False
        addStepB.active = False
        addStepB.clicking = True
        subStepB.active = False
        subStepB.clicking = True
    else:
        stepS.active = True
        addStepB.active = True
        subStepB.active = True
    gAlgorithmSelectorD.Draw()

    # selectedMaze.AlgorithmOverlay()

def SolveMaze(selectedMaze): # everything to prepare solve mode
    solveAlgoB.Draw()
    if solveAlgoB.Clicked() == True:
        if selectedMaze.currentStep > 1 and selectedMaze.currentStep == selectedMaze.endStep:
            AlgorithmManager(1,0,selectedMaze)
        
        else:
            ErrorMessage("maze must be fully generated")

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
            

            # ^^^^^^^^^^^^^^^^
            
            maze.AddtoStateString((cellPosX,maze.cols-1),(0,1)) # makes exit
            maze.UpdateEndStep()
            maze.UpdateCurrentStep(maze.endStep)
            stepS.max = maze.endStep
            stepS.SetValue(maze.endStep)

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
        stepS.max = 1
        stepS.SetValue(1)
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



    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()