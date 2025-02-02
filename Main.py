import pygame
from StaticSurfs import DrawStatics
from MazeMethods import Maze
from ClickableElements import ClickableElements,Button
from MazeGenerators import *
winSize = (1400,700)
FPS = 60
running = True
clock = pygame.time.Clock()
pygame.display.init()
win = pygame.display.set_mode((winSize[0], winSize[1]))
pygame.display.set_caption("MazeFun")

maze1 = Maze(win,(120,50),10,10)



############################################################################################################################
while running:
    DrawStatics(win)
    maze1.DrawMazeThin()
    



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()