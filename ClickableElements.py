import pygame


#parent class to everything that requires mouse click
class ClickableElements:
    def __init__(self,pos,box):
        self.pos = pos
        self.box = box
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
    def __init__(self,pos,box,surf,text,fsize= 20,colour= (200,200,200),hcolour= (230,230,230),fcolour= (0,0,0)):
        super().__init__(pos,box)
        pygame.font.init()
        self.surf = surf
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


class MazeClick(ClickableElements):
    def __init__(self,pos,box,surf):
        super().__init__(pos,box)
        self.surf = surf
        self.mouseDisp = (0,0)
        
    def RegisterClick(self):
        if pygame.mouse.get_pressed()[0] == False:
            self.valid = True

        if self.Hovering() == True and self.valid == True:
            if pygame.mouse.get_pressed()[0]:
                self.valid = False
                self.clicked = True
                mousePos = pygame.mouse.get_pos()
                self.mouseDisp = (mousePos[0]-self.pos[0],mousePos[1]-self.pos[1])


class Slider(Button):
    def __init__(self,pos,box,surf,text,max,min,fsize= 20,colour= (200,200,200),hcolour=(230,30,30),fcolour= (0,0,0)):
        super().__init__(pos,box,surf,text,fsize,colour,hcolour,fcolour)
        pygame.font.init()
        self.mouseDisp = (0,0)
        self.max = max
        self.min = min
        self.relativeDashPos = (0,0)
        self.dashBox = (box[1]*2,box[1]*4)

    def ReturnValue(self):
        pass

    def Hovering(self):
        dashRect = pygame.Rect((self.relativeDashPos[0]+self.bRect[0],self.relativeDashPos[1]+self.bRect[1]+self.bRect[3]/2-self.dashBox[1]/2),self.dashBox)
        mousePos = pygame.mouse.get_pos()
        if mousePos[0] >= self.pos[0] and mousePos[0] <= self.pos[0]+dashRect[2]:
            if mousePos[1] >= self.pos[1] and mousePos[1] <= self.pos[1]+dashRect[3]:
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
                mousePos = pygame.mouse.get_pos()
                self.mouseDisp = (mousePos[0]-self.pos[0],mousePos[1]-self.pos[1])
                


    def Draw(self):
        dashRect = pygame.Rect((self.relativeDashPos[0]+self.bRect[0],self.relativeDashPos[1]+self.bRect[1]+self.bRect[3]/2-self.dashBox[1]/2),self.dashBox)
        pygame.draw.rect(self.surf,self.colour,self.bRect)

        if self.Hovering() == True:
            pygame.draw.rect(self.surf,self.hcolour,dashRect)
        else:
            pygame.draw.rect(self.surf,self.colour,dashRect)
        
        # All the text
        textSurf = self.font.render(self.text,True,self.fcolour)
        minSurf = self.font.render(str(self.min),True,self.fcolour)
        maxSurf = self.font.render(str(self.max),True,self.fcolour)
        textSize = self.font.size(self.text)
        tPos = (self.pos[0]+self.box[0]/2-textSize[0]/2,self.pos[1]+self.box[1]/2-textSize[1])
        minPos = (self.pos[0],self.pos[1]+self.box[1]/2)
        maxPos = (self.pos[0]+self.box[0],self.pos[1]+self.box[1]/2)
        pygame.Surface.blit(self.surf,textSurf,tPos)
        pygame.Surface.blit(self.surf,minSurf,minPos)
        pygame.Surface.blit(self.surf,maxSurf,maxPos)

