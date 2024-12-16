import pygame
from MazeMethods import Maze
from ClickableElements import ClickableElements,Button
from MazeGenerators import *
winSize = (1400,700)
FPS = 60
running = True
clock = pygame.time.Clock()
pygame.display.init()
win = pygame.display.set_mode((winSize[0], winSize[1]))

maze1 = Maze(win,(100,100),20,20)
clearbutton = Button((20,20),(130,30),win,"ClearMaze",20)
visitedlist = []
DepthFirst(maze1,(19,10),visitedlist)
############################################################################################################################
while running:
    win.fill((20,20,110))
    maze1.DrawMazeThin((20,20,20),(100,100,100))
    clearbutton.Run()


    








    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()