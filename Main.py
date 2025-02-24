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
algorithmB = Button((10,40),(80,20),win,"Apply",15)
sizeXSlider = Slider((10,85),(80,5),win,"sizeX",32,1,15)


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
        maze.ClickHandler()
        if maze.selected == True:
            ##contains buttonrunstuff unique to each maze
            algorithmB.RegisterClick()
            if algorithmB.clicked == True:
                maze.ClearMaze()
                vList= []
                DepthFirst(maze,(0,0),vList)
                maze.CountSteps()
                maze.currentStep = maze.endStep
                maze.UpdateMazeState()
                maze.stateString = "."
                algorithmB.clicked = False
            algorithmB.Draw()
            sizeXSlider.RegisterClick()
            sizeXSlider.Draw()
                

            



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()