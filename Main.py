import pygame
from MazeMethods import Maze
from ClickableElemets import*
from MazeGenerators import *
winSize = (1400,700)
FPS = 60
running = True
clock = pygame.time.Clock()
pygame.display.init()
win = pygame.display.set_mode((winSize[0], winSize[1]))
clickBox = ClickableElemets((0,0),(500,500))

############################################################################################################################
while running:
    win.fill((20,20,110))
    








    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()