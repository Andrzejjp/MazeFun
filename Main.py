import pygame
from MazeMethods import Maze
from ClickableElements import Button,Slider,DropBox
from MazeGenerators import *
winSize = (1400,700)
FPS = 0
running = True
clock = pygame.time.Clock()
pygame.display.init()
win = pygame.display.set_mode((winSize[0], winSize[1]),pygame.RESIZABLE)
pygame.display.set_caption("MazeFun")

mazeList = []

newMazeB = Button(win,(10,5),(80,20),"New Maze",15)
algorithmB = Button(win,(10,40),(80,20),"ApplyAlgorithm",10)
addStepB = Button(win,(55,100),(30,20),"+1",15)
subStepB = Button(win,(15,100),(30,20),"-1",15)
deleteB = Button(win,(10,670),(80,20),"Delete Maze",12,(200,200,200),(255,49,49))


stepS = Slider(win,(10,85),(80,5),"Step",1,1,15)
sizeXS = Slider(win,(10,400),(80,5),"sizeX",32,1,15)
sizeYS = Slider(win,(10,435),(80,5),"sizeY",32,1,15)

modeD = DropBox(win,(100,5),(80,20),"Mode",["Generate","Solve"],15)

selectedMaze = None

# functons
def DrawStaticSurfs(surface):

    surfSize = surface.get_size()

    leftBarRect = pygame.Rect(((0,0),(100,surfSize[1])))
    topBarRect = pygame.Rect(((0,0),(surfSize[0],30)))

    pygame.display.update(leftBarRect)
    pygame.display.update(topBarRect)

    surface.fill("#BCBEBC")
    pygame.draw.rect(surface,("#DEDEDE"),leftBarRect)
    pygame.draw.rect(surface,("#F5F5F5"),topBarRect)

def GenerateMaze(surface):
    pass

def SolveMaze(surface):
    pass

############################################################################################################################
while running:
    DrawStaticSurfs(win)

   
    if newMazeB.Clicked():
        mazeList.append(Maze(win))
    newMazeB.Draw()

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
        
    #rearranges the list so the selected maze is drawn last
    if selectedMaze != None:
        for i in range(len(mazeList)):
            if selectedMaze == mazeList[i]:
                mazeList.append(mazeList[i])
                mazeList.pop(i)

    #deals with the selectedMaze's relevant buttons etc
    if selectedMaze != None:
        if selectedMaze.clickObj.CheckSelect() == True:
            sizeXS.SetValue(selectedMaze.rows)
            sizeYS.SetValue(selectedMaze.cols)
            stepS.SetValue(selectedMaze.currentStep)
        
        if algorithmB.Clicked():
            selectedMaze.stateString = "."
            selectedMaze.ClearMaze()
            vList= []
            DepthFirst(selectedMaze,(round(selectedMaze.rows/2),0),vList)
            selectedMaze.MakeEntrance()
            selectedMaze.UpdateEndStep()
            selectedMaze.UpdateCurrentStep(selectedMaze.endStep)
            stepS.max = selectedMaze.endStep
            stepS.SetValue(selectedMaze.endStep)
        algorithmB.Draw()

        sizeXS.Draw()
        if sizeXS.RegisterClick() == True:
            selectedMaze.UpdateSize(sizeXS.ReturnValue(),selectedMaze.cols)
            selectedMaze.stateString = "."
            selectedMaze.UpdateCurrentStep(1)
            stepS.max = 1
            stepS.SetValue(selectedMaze.currentStep)

        sizeYS.Draw()
        if sizeYS.RegisterClick() == True:
            selectedMaze.UpdateSize(selectedMaze.rows,sizeYS.ReturnValue())
            selectedMaze.stateString = "."
            selectedMaze.UpdateCurrentStep(1)
            stepS.max = 1
            stepS.SetValue(selectedMaze.currentStep)
        
        stepS.Draw()
        if stepS.RegisterClick() == True:
            selectedMaze.UpdateCurrentStep(stepS.ReturnValue())

        if addStepB.Clicked() and selectedMaze.endStep > selectedMaze.currentStep:
            selectedMaze.UpdateCurrentStep(selectedMaze.currentStep + 1)
            stepS.SetValue(selectedMaze.currentStep)
        addStepB.Draw()

        if subStepB.Clicked() and 1 < selectedMaze.currentStep:
            selectedMaze.UpdateCurrentStep(selectedMaze.currentStep - 1)
            stepS.SetValue(selectedMaze.currentStep)
        subStepB.Draw()
        
        if deleteB.Clicked():
            mazeList.pop(len(mazeList)-1)
            selectedMaze = None
        deleteB.Draw()

        modeD.Clicked()
        modeD.Draw()


        # selectedMaze.AlgorithmOverlay()

            



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()