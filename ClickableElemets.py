import pygame

class ClickableElemets:
    def __init__(self,pos,box,colour=(200,200,200)):
        self.pos = pos
        self.box = box
        self.colour = colour
        self.clicked = False
        
    def Hover(self):
        mousePos = pygame.mouse.get_pos()
        if mousePos[0] >= self.pos[0] and mousePos[0] <= self.pos[0]+self.box[0]:
            if mousePos[1] >= self.pos[1] and mousePos[1] <= self.pos[1]+self.box[1]:
                self.colour = (255,255,255)
                return True
        return False

    def RegisterClick(self):
        if self.Hover() == True:
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True


class Button(ClickableElemets):
    
        
