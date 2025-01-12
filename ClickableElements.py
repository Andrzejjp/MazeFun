import pygame


#parent class to everything that requires mouse click
class ClickableElements:
    def __init__(self,pos,box,surf):
        self.pos = pos
        self.box = box
        self.surf = surf
        self.valid = False
        self.clicked = False
        
    def Hovering(self):
        mousePos = pygame.mouse.get_pos()
        if mousePos[0] >= self.pos[0] and mousePos[0] <= self.pos[0]+self.box[0]:
            if mousePos[1] >= self.pos[1] and mousePos[1] <= self.pos[1]+self.box[1]:
                return True
            else:
                return False
        else :
            return False

    def RegisterClick(self):
        if pygame.mouse.get_pressed()[0] == False:
            self.valid = True

        if self.Hovering() == True and self.valid == True:
            if pygame.mouse.get_pressed()[0]:
                self.valid = False
                self.clicked = True


class Button(ClickableElements):
    def __init__(self,pos,box,surf,text,fsize= 20,colour= (200,200,200),hcolour= (250,250,250),fcolour= (0,0,0)):
        super().__init__(pos,box,surf)
        pygame.font.init()
        self.fsize = fsize
        self.font = pygame.font.SysFont("Courier New", self.fsize)
        self.colour = colour
        self.hcolour = hcolour
        self.fcolour = fcolour
        self.text = text
        self.bRect = pygame.Rect(self.pos,self.box)


    def Draw(self):
        if self.Hovering() == True:
            pygame.draw.rect(self.surf,self.hcolour,self.bRect)
        else:
            pygame.draw.rect(self.surf,self.colour,self.bRect)
        textSurf = self.font.render(self.text,True,self.fcolour)
        #centers the text on the button
        fontsize = self.font.size(self.text)
        tPos = (self.pos[0]+self.box[0]/2-fontsize[0]/2,self.pos[1]+self.box[1]/2-fontsize[1]/2)
        pygame.Surface.blit(self.surf,textSurf,tPos)



        
