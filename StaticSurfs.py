import pygame

leftBarRect = pygame.Rect(((0,0),(100,2000)))

def DrawStatics(surf):

    surfSize = surf.get_size()

    leftBarRect = pygame.Rect(((0,0),(100,surfSize[1])))
    topBarRect = pygame.Rect(((0,0),(surfSize[0],30))) 

    pygame.display.update(leftBarRect)
    pygame.display.update(topBarRect)

    surf.fill("#BCBEBC")
    pygame.draw.rect(surf,("#DEDEDE"),leftBarRect)
    pygame.draw.rect(surf,("#F5F5F5"),topBarRect)
    
    