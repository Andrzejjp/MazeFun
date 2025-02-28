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
    def __init__(self,surf,maze):
        self.pos = maze.origin
        self.box = (maze.rows*maze.px,maze.cols*maze.px)
        self.surf = surf
        self.maze = maze
        self.mouseDisp = (0,0)
        self.valid = True
        self.validR = True
        self.selected = False
        self.selectedIndicator = False
        
    def RegisterClick(self):
        if pygame.mouse.get_pressed()[0] == False:
            self.valid = True
        
        if pygame.mouse.get_pressed()[2] == False:
            self.validR = True

        if self.Hovering() == True and self.valid == True and pygame.mouse.get_pressed()[0] == True and self.selected:
            self.valid = False
            mousePos = pygame.mouse.get_pos()
            self.mouseDisp = (mousePos[0]-self.maze.origin[0],mousePos[1]-self.maze.origin[1])
        
        if self.Hovering() == True and pygame.mouse.get_pressed()[2] == True and self.validR == True:
            if self.selected:
                self.selected = False
            else:
                self.selected = True
                self.selectedIndicator = True
            self.validR = False
        
        if self.valid == False:
            mousePos = pygame.mouse.get_pos()
            self.maze.UpdateOrigin((mousePos[0]-self.mouseDisp[0],mousePos[1]-self.mouseDisp[1]))
        
        if self.selected == True:
            surf = self.surf
            colour = (255,0,0)
            px = self.maze.px
            mazePos = (self.maze.origin[0]-1,self.maze.origin[1]-1)
            mazeBox = (self.maze.rows*px,self.maze.cols*px)
            pygame.draw.line(surf,colour,mazePos,(mazePos[0]+mazeBox[0]+1,mazePos[1]))
            pygame.draw.line(surf,colour,(mazePos[0]+mazeBox[0]+1,mazePos[1]),(mazePos[0]+mazeBox[0]+1,mazePos[1]+mazeBox[1]+1))
            pygame.draw.line(surf,colour,(mazePos[0]+mazeBox[0]+1,mazePos[1]+mazeBox[1]+1),(mazePos[0],mazePos[1]+mazeBox[1]+1))
            pygame.draw.line(surf,colour,(mazePos[0],mazePos[1]+mazeBox[1]+1),mazePos)

    def CheckSelect(self): #returns true if a maze has been selected only once per selection
        if self.selectedIndicator == True:
            self.selectedIndicator = False
            return True

class Slider(Button):
    def __init__(self,pos,box,surf,text,max,min,fsize= 20,colour= (200,200,200),hcolour=(230,30,30),fcolour= (0,0,0)):
        super().__init__(pos,box,surf,text,fsize,colour,hcolour,fcolour)
        pygame.font.init()
        self.relativeDashPos = 0
        self.barRect = self.bRect
        self.dashRect = pygame.Rect((self.barRect[0]+self.relativeDashPos,self.barRect[1]+self.barRect[3]/2-self.box[1]*2),(box[1]*2,box[1]*4))
        self.mouseDisp = 0
        self.max = max
        self.min = min
        self.valid = True

    def ChangeRelativeDashPos(self,newPos):#new pos is the Relative pos
        self.relativeDashPos = newPos
        self.dashRect = pygame.Rect((self.barRect[0]+self.relativeDashPos,self.dashRect[1]),(self.dashRect[2],self.dashRect[3]))

    def SetValue(self,value):#sets the dash on the slider to a value in the range
        range = self.max - self.min
        temp = value - self.min
        if range == 0:
            percent = 0
        else:
            percent = temp/range
        total = self.barRect[2]-self.dashRect[2]
        self.ChangeRelativeDashPos(percent*total)

    def ReturnValue(self):#returns the value of the position the slider is sat on 
        total = self.max - self.min
        range = self.barRect[2]-self.dashRect[2]
        sliderPercent = (self.relativeDashPos)/range
        value = self.min+(total*sliderPercent)
        return(round(value))

    def Hovering(self):
        dashRect = self.dashRect
        mousePos = pygame.mouse.get_pos()
        if mousePos[0] >= self.dashRect[0] and mousePos[0] <= self.dashRect[0]+self.dashRect[2]:
            if mousePos[1] >= self.dashRect[1] and mousePos[1] <= self.dashRect[1]+self.dashRect[3]:
                return True
            else:
                return False
        else :
            return False
    
    def RegisterClick(self):
        #checks for letting go
        if pygame.mouse.get_pressed()[0] == False and self.valid == False:
            self.valid = True
            self.clicked = False
            return True
            

        if self.Hovering() == True and pygame.mouse.get_pressed()[0] == True and self.valid == True:
            self.valid = False
            mousePos = pygame.mouse.get_pos()[0]
            self.mouseDisp = (mousePos-self.barRect[0]-self.relativeDashPos)
            self.clicked = True

        if self.clicked == True:
            mousePos = pygame.mouse.get_pos()[0]
            staticPos = self.barRect[0]+self.mouseDisp
            self.ChangeRelativeDashPos(mousePos-staticPos)
            if self.relativeDashPos < 0:
                self.ChangeRelativeDashPos(0)
            elif self.relativeDashPos > self.barRect[2]-self.dashRect[2]:
                self.ChangeRelativeDashPos(self.barRect[2]-self.dashRect[2])

    def Draw(self):
        dashRect = self.dashRect
        pygame.draw.rect(self.surf,self.colour,self.bRect)

        if self.Hovering() == True:
            pygame.draw.rect(self.surf,self.hcolour,dashRect)
        else:
            pygame.draw.rect(self.surf,self.colour,dashRect)
        
        # All the text
        text = self.text+":"+str(self.ReturnValue())
        textSurf = self.font.render(text,True,self.fcolour)
        minSurf = self.font.render(str(self.min),True,self.fcolour)
        maxSurf = self.font.render(str(self.max),True,self.fcolour)
        textSize = self.font.size(text)
        tPos = (self.pos[0]+self.box[0]/2-textSize[0]/2,self.pos[1]-textSize[1]-self.bRect[3])
        pygame.Surface.blit(self.surf,textSurf,tPos)
