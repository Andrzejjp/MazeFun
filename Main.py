import pygame
from StaticSurfs import DrawStatics
from MazeMethods import Maze
from ClickableElements import Button,Slider
from MazeGenerators import *
winSize = (1400,700)
FPS = 60
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
        checkOneTrue = False
        if maze.clickObj.selected == True and maze != selectedMaze:
            selectedMaze = maze
            for maze in mazeList:
                if maze != selectedMaze:
                    maze.clickObj.selected = False
                if maze.clickObj.selected == True:
                    checkOneTrue = True
        if checkOneTrue == False:
            selectedMaze = None

    #deals with the selectedMaze's relevant buttons etc
        

        
        


        if maze.clickObj.selected == True:
            if maze.clickObj.CheckSelect() == True:
                sizeXS.SetValue(maze.rows)
                sizeYS.SetValue(maze.cols)
            ##contains buttonrunstuff unique to each maze
            algorithmB.RegisterClick()
            if algorithmB.clicked == True:
                maze.stateString = "."
                maze.ClearMaze()
                vList= []
                DepthFirst(maze,(round(maze.rows/2),0),vList)
                maze.MakeEntrance()
                maze.UpdateEndStep()
                maze.UpdateCurrentStep(maze.endStep)
                stepS.max = maze.endStep
                stepS.SetValue(maze.endStep)
                algorithmB.clicked = False
            algorithmB.Draw()

            sizeXS.Draw()
            if sizeXS.RegisterClick() == True:
                maze.UpdateSize(sizeXS.ReturnValue(),maze.cols)

            sizeYS.Draw()
            if sizeYS.RegisterClick() == True:
                maze.UpdateSize(maze.rows,sizeYS.ReturnValue())
            
            stepS.Draw()
            if stepS.RegisterClick() == True:
                maze.UpdateCurrentStep(stepS.ReturnValue())

            addStepB.RegisterClick()
            if addStepB.clicked == True and maze.endStep > maze.currentStep:
                maze.UpdateCurrentStep(maze.currentStep + 1)
                stepS.SetValue(maze.currentStep)
                addStepB.clicked = False
            addStepB.Draw()

            subStepB.RegisterClick()
            if subStepB.clicked == True and 1 < maze.currentStep:
                maze.UpdateCurrentStep(maze.currentStep - 1)
                stepS.SetValue(maze.currentStep)
                subStepB.clicked = False
            subStepB.Draw()
                

            



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()