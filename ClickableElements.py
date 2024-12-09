import pygame


#parent class to everything that requires mouse click
class ClickableElements:
    def __init__(self,pos,box,surf):
        self.pos = pos
        self.box = box
        self.surf = surf
        self.hover = False
        self.clicked = False
        
    def Hovering(self):
        mousePos = pygame.mouse.get_pos()
        if mousePos[0] >= self.pos[0] and mousePos[0] <= self.pos[0]+self.box[0]:
            if mousePos[1] >= self.pos[1] and mousePos[1] <= self.pos[1]+self.box[1]:
                self.hover = True
            else:
                self.hover = False
        else :
            self.hover = False

    def RegisterClick(self):
        self.Hovering()
        if self.hover == True:
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True


class Button(ClickableElements):
    def __init__(self,pos,box,surf,text,fsize= 36,colour= (200,200,200),hcolour= (250,250,250),fcolour= (0,0,0)):
        super().__init__(pos,box,surf)
        pygame.font.init()
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 36)
        self.colour = colour
        self.hcolour = hcolour
        self.fcolour = fcolour
        self.fsize = fsize
        self.text = text
        self.bRect = pygame.Rect(self.pos,self.box)

    def Draw(self):
        self.Hovering()
        if self.hover == True:
            pygame.draw.rect(self.surf,self.hcolour,self.bRect)
        else:
            pygame.draw.rect(self.surf,self.colour,self.bRect)
        textSurf = self.font.render(self.text,True,self.fcolour)
        #centers the text on the button
        fontsize = self.font.size(self.text)
        tPos = (self.pos[0]+self.box[0]/2-fontsize[0]/2,self.pos[1]+self.box[1]/2-fontsize[1]/2)
        pygame.Surface.blit(self.surf,textSurf,tPos)

    def DoClicked(self):
        self.RegisterClick()
        if self.clicked == True:
            #what the button should do
            print("clicked")
            #make specific button sub classes
            self.clicked = False
    
    def Run(self):
        self.Draw()
        self.DoClicked()


        
