import pygame
from MazeMethods import Maze
from MazeGenerators import *
winSize = (1400,700)
FPS = 60
running = True
clock = pygame.time.Clock()
pygame.display.init()
win = pygame.display.set_mode((winSize[0], winSize[1]))
maze1 = Maze(50,3)
visitedList =[]
DepthFirst(maze1,(5,0),visitedList)

############################################################################################################################
while running:
    win.fill((200,0,0))
    maze1.DrawMazeThin(win,(255,255,255),(200,20,20))








    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()