##Todo
import pygame
from GridMethods import Grid
WinSize = (1400,700)
FPS = 60
running = True
clock = pygame.time.Clock()
pygame.display.init()
win = pygame.display.set_mode((WinSize[0], WinSize[1]))
grid1 = Grid(11,10)
grid1.OutputGrid()

############################################################################################################################
while running:
    win.fill((200,0,0))
    
    








    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()