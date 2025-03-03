import pygame
from StaticSurfs import DrawStatics
from MazeMethods import Maze
from ClickableElements import Button,Slider
from MazeGenerators import *
winSize = (1400,700)
FPS = 0
running = True
clock = pygame.time.Clock()
pygame.display.init()
win = pygame.display.set_mode((winSize[0], winSize[1]))
pygame.display.set_caption("MazeFun")

mazeList = []

newMazeB = Button((10,5),(80,20),win,"New Maze",15)


algorithmB = Button((10,40),(80,20),win,"ApplyAlgorithm",10)
stepS = Slider((10,85),(80,5),win,"Step",1,1,15)
addStepB = Button((55,100),(30,20),win,"+1",15)
subStepB = Button((15,100),(30,20),win,"-1",15)


sizeXS = Slider((10,400),(80,5),win,"sizeX",32,1,15)
sizeYS = Slider((10,435),(80,5),win,"sizeY",32,1,15)

selectedMaze = None


############################################################################################################################
while running:
    DrawStatics(win)

    newMazeB.RegisterClick()
    if newMazeB.clicked == True:
        mazeList.append(Maze(win))
        newMazeB.clicked = False
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
        
        algorithmB.RegisterClick()
        if algorithmB.clicked == True:
            selectedMaze.stateString = "."
            selectedMaze.ClearMaze()
            vList= []
            DepthFirst(selectedMaze,(round(selectedMaze.rows/2),0),vList)
            selectedMaze.MakeEntrance()
            selectedMaze.UpdateEndStep()
            selectedMaze.UpdateCurrentStep(selectedMaze.endStep)
            stepS.max = selectedMaze.endStep
            stepS.SetValue(selectedMaze.endStep)
            algorithmB.clicked = False
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

        addStepB.RegisterClick()
        if addStepB.clicked == True and selectedMaze.endStep > selectedMaze.currentStep:
            selectedMaze.UpdateCurrentStep(selectedMaze.currentStep + 1)
            stepS.SetValue(selectedMaze.currentStep)
            addStepB.clicked = False
        addStepB.Draw()

        subStepB.RegisterClick()
        if subStepB.clicked == True and 1 < selectedMaze.currentStep:
            selectedMaze.UpdateCurrentStep(selectedMaze.currentStep - 1)
            stepS.SetValue(selectedMaze.currentStep)
            subStepB.clicked = False
        subStepB.Draw()
        
        # selectedMaze.AlgorithmOverlay()

            



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()