##Todo
#fix mazeGenerators 
import pygame
from GridMethods import Grid
from MazeGenerators import *
WinSize = (1400,700)
FPS = 60
running = True
clock = pygame.time.Clock()
pygame.display.init()
win = pygame.display.set_mode((WinSize[0], WinSize[1]))
grid1 = Grid(11,10)
grid1.OutputGrid()
DepthFirst(grid1,(6,0))

############################################################################################################################
while running:
    win.fill((200,0,0))
    grid1.DrawGrid(win,16)
    








    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()