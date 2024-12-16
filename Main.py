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

maze1 = Maze(win,(20,20),20,20)
visitedList = []
DepthFirst(maze1,(4,0),visitedList)

############################################################################################################################
while running:
    win.fill((20,20,110))
    maze1.DrawMazeThin((255,255,255),(100,200,250))


    








    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()