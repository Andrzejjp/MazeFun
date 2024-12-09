import pygame
from Main import win

#parent class to everything that requires mouse click
class ClickableElements:
    def __init__(self,pos,box,surf):
        self.pos = pos
        self.box = box
        self.surf = win
        self.hover = False
        self.clicked = False
        
    def Hover(self):
        mousePos = pygame.mouse.get_pos()
        if mousePos[0] >= self.pos[0] and mousePos[0] <= self.pos[0]+self.box[0]:
            if mousePos[1] >= self.pos[1] and mousePos[1] <= self.pos[1]+self.box[1]:
                self.hover = True
        self.hover = False

    def RegisterClick(self):
        self.Hover()
        if self.hover == True:
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True


class Button(ClickableElements):
    def __init__(self,pos,box,surf,text,colour=(200,200,200),hcolour=(250,250,250)):
        super().__init__(pos,box,surf)
        pygame.font.init()
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 36)
        self.colour = colour
        self.hcolour = hcolour
        self.text = text
        self.bRect = pygame.Rect(self.pos,self.box)

    def Draw(self):
        self.RegisterClick()
        if self.hover == True:
            pygame.draw.rect(self.surf,self.bRect,self.hcolour)
        else:
            pygame.draw.rect(self.surf,self.bRect,self.hcolour)
        textSurf = self.font.render(self.text,True,(0,0,0))
        pygame.Surface.blit(textSurf,self.surf)


        
