import pygame


#parent class to everything that requires mouse click
class ClickableElements:
    def __init__(self,pos,box):
        self.rect = pygame.Rect(pos,box)
        self.clicking = False # ensures only one click is registered even if lmb is held
        
    def Hovering(self):#checks that the mouse is over the element
        mousePos = pygame.mouse.get_pos()
        if mousePos[0] >= self.rect[0] and mousePos[0] <= self.rect[0]+self.rect[2]:
            if mousePos[1] >= self.rect[1] and mousePos[1] <= self.rect[1]+self.rect[3]:
                return True
            else:
                return False
        else :
            return False

    def Clicked(self):#returns true if the element was clicked 
        if pygame.mouse.get_pressed()[0] == False:
            self.clicking = False

        if self.Hovering() == True and self.clicking == False and pygame.mouse.get_pressed()[0] == True:
            self.clicking = True
            return True

        return False

class Button(ClickableElements):
    def __init__(self,surface,pos,box,text,fontSize= 20,colour= (200,200,200),hcolour= (230,230,230),fcolour= (0,0,0)):
        pygame.font.init()
        self.surf = surface
        super().__init__(pos,box)
        self.fsize = fontSize
        self.font = pygame.font.SysFont("Courier New", self.fsize)
        self.colour = colour
        self.hcolour = hcolour
        self.fcolour = fcolour
        self.text = text

    def Draw(self):
        if self.Hovering() == True:
            pygame.draw.rect(self.surf,self.hcolour,self.rect)
        else:
            pygame.draw.rect(self.surf,self.colour,self.rect)
        textSurf = self.font.render(self.text,True,self.fcolour)
        #centers the text on the button
        fontsize = self.font.size(self.text)
        tPos = (self.rect[0]+self.rect[2]/2-fontsize[0]/2,self.rect[1]+self.rect[3]/2-fontsize[1]/2)
        pygame.Surface.blit(self.surf,textSurf,tPos)

class MazeClick(ClickableElements):
    def __init__(self,surf,maze):
        self.pos = maze.origin
        self.box = (maze.rows*maze.px,maze.cols*maze.px)
        self.rect = pygame.Rect(self.pos,self.box)
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
    def __init__(self,surf,pos,box,text,max,min,fsize= 20,colour= (200,200,200),hcolour=(230,30,30),fcolour= (0,0,0)):
        super().__init__(surf,pos,box,text,fsize,colour,hcolour,fcolour)
        pygame.font.init()
        self.relativeDashPos = 0
        self.barRect = self.rect
        self.dashRect = pygame.Rect((self.barRect[0]+self.relativeDashPos,self.barRect[1]+self.barRect[3]/2-self.barRect[3]*2),(box[1]*2,box[1]*4))
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
            return True
            

        if self.Hovering() == True and pygame.mouse.get_pressed()[0] == True and self.valid == True:
            self.valid = False
            mousePos = pygame.mouse.get_pos()[0]
            self.mouseDisp = (mousePos-self.barRect[0]-self.relativeDashPos)

        if self.valid == False:
            mousePos = pygame.mouse.get_pos()[0]
            staticPos = self.barRect[0]+self.mouseDisp
            self.ChangeRelativeDashPos(mousePos-staticPos)
            if self.relativeDashPos < 0:
                self.ChangeRelativeDashPos(0)
            elif self.relativeDashPos > self.barRect[2]-self.dashRect[2]:
                self.ChangeRelativeDashPos(self.barRect[2]-self.dashRect[2])

    def Draw(self):
        dashRect = self.dashRect
        self.bRect = self.barRect
        pygame.draw.rect(self.surf,self.colour,self.bRect)

        if self.Hovering() == True:
            pygame.draw.rect(self.surf,self.hcolour,dashRect)
        else:
            pygame.draw.rect(self.surf,self.colour,dashRect)
        
        # All the text
        text = self.text+":"+str(self.ReturnValue())
        textSurf = self.font.render(text,True,self.fcolour)
        textSize = self.font.size(text)
        tPos = (self.rect[0]+self.rect[2]/2-textSize[0]/2,self.rect[1]-textSize[1]-self.bRect[3])
        pygame.Surface.blit(self.surf,textSurf,tPos)

class DropBox(Button):
    def __init__(self,surf,pos,box,text,optionsList,fontSize=20,colour=(200,200,200),hcolour=(230,230,230),fcolour=(0,0,0)):
        super().__init__(surf,pos,box,text,fontSize,colour,hcolour,fcolour)
        self.box = box
        self.options = optionsList
        self.open = False #toggles if the dropboxes options are visable
        self.currentOption = None

    def OptionFromY(self,y): # takes y value of mouse and returns the index of an option in options list
        ybox = self.box[1]
        ypos = self.rect[1]
        for i in range(2,len(self.options)+2):
            start = ypos + ybox*(i-1)
            end = ypos + ybox*(i)
            if start <= y and end >= y:
                return(i-2)

    def Clicked(self):
        if pygame.mouse.get_pressed()[0] == False:
            self.clicking = False

        if self.Hovering() == True and self.clicking == False and pygame.mouse.get_pressed()[0] == True:
            self.clicking = True
            if self.open:
                self.open = False
                self.rect = pygame.Rect(self.rect[0],self.rect[1],self.rect[2],self.box[1]) 
                print(self.OptionFromY(pygame.mouse.get_pos()[1]))
            else:
                self.open = True
                self.rect = pygame.Rect(self.rect[0],self.rect[1],self.rect[2],self.box[1] + self.box[1]*len(self.options))
        
    def Draw(self):
        if self.Hovering() == True:
            pygame.draw.rect(self.surf,self.hcolour,self.rect)
        else:
            pygame.draw.rect(self.surf,self.colour,self.rect)

        if self.open == True:
            textSurf = self.font.render((self.text+"-"),True,self.fcolour)
            # handles the options text 
            for i in range(1,len(self.options)+1):
                text = self.options[i-1]
                textSize = self.font.size(text)
                tPos = (self.rect[0]+self.rect[2]/2-textSize[0]/2,self.rect[1]+self.box[1]*i+self.box[1]/2-textSize[1]/2)
                otherTextSurf = self.font.render((text),True,self.fcolour)
                pygame.Surface.blit(self.surf,otherTextSurf,tPos)

        else:
            textSurf = self.font.render((self.text+"^"),True,self.fcolour)
        
        #centers the text on the button
        fontsize = self.font.size(self.text)
        tPos = (self.rect[0]+self.rect[2]/2-fontsize[0]/2,self.rect[1]+self.box[1]/2-fontsize[1]/2)
        pygame.Surface.blit(self.surf,textSurf,tPos)

