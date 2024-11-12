##Todo
#fix mazeGenerators 
import pygame
from MazeMethods import Maze
from MazeGenerators import *
winSize = (1400,700)
FPS = 60
running = True
clock = pygame.time.Clock()
pygame.display.init()
win = pygame.display.set_mode((winSize[0], winSize[1]))
Maze1 = Maze(40,40)

############################################################################################################################
while running:
    win.fill((200,0,0))








    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()