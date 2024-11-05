##Todo
#fix mazeGenerators 
import pygame
from MazeMethods import Maze
from MazeGenerators import *
WinSize = (1400,700)
FPS = 60
running = True
clock = pygame.time.Clock()
pygame.display.init()
win = pygame.display.set_mode((WinSize[0], WinSize[1]))
Maze1 = Maze(20,10)
Maze1.OutputGrid()
DepthFirst(Maze1,(0,0))

############################################################################################################################
while running:
    win.fill((200,0,0))
    Maze1.DrawGrid(win,16)
    








    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()