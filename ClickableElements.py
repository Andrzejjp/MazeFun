import pygame


# abstract class for registering clicked inputs
class ClickableElements:
    def __init__(self,pos,box):
        self.rect = pygame.Rect(pos,box)
        self.clicking = False # ensures only one click is registered even if lmb is held
        self.active = True # used to deactivate the functionality of the element
        
    def Hovering(self,rect):#checks if the mouse is hovering over a rect
        if self.active == True:
            mousePos = pygame.mouse.get_pos()
            if mousePos[0] >= rect[0] and mousePos[0] <= rect[0]+rect[2]:
                if mousePos[1] >= rect[1] and mousePos[1] <= rect[1]+rect[3]:
                    return True

    def Clicked(self):#returns true if the element was clicked 
        if pygame.mouse.get_pressed()[0] == False:
            self.clicking = False

        if self.Hovering(self.rect) == True and self.clicking == False and pygame.mouse.get_pressed()[0] == True:
            self.clicking = True
            return True

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
        if self.Hovering(self.rect) == True:
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
        self.active = True
        self.pos = maze.origin
        self.box = (maze.rows*maze.px,maze.cols*maze.px)
        self.rect = pygame.Rect(self.pos,self.box)
        self.surf = surf
        self.maze = maze
        self.mouseDisp = (0,0)
        self.clicking = False
        self.validR = True
        self.selected = False
        self.selectedIndicator = False
        
    def RegisterClick(self):
        if pygame.mouse.get_pressed()[0] == False:
            self.clicking = False
        
        if pygame.mouse.get_pressed()[2] == False:
            self.validR = True

        if self.Hovering(self.rect) == True and self.clicking == False and pygame.mouse.get_pressed()[0] == True and self.selected:
            self.clicking = True
            mousePos = pygame.mouse.get_pos()
            self.mouseDisp = (mousePos[0]-self.maze.origin[0],mousePos[1]-self.maze.origin[1])
        
        if self.Hovering(self.rect) == True and pygame.mouse.get_pressed()[2] == True and self.validR == True:
            if self.selected:
                self.selected = False
            else:
                self.selected = True
                self.selectedIndicator = True
            self.validR = False
        
        if self.clicking == True:
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
        self.clicking = False

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

    def Clicked(self):

        leftRect = pygame.Rect((self.barRect[0],self.barRect[1]),(self.dashRect[0]-self.barRect[0],self.barRect[3]))
        rightRect = pygame.Rect((self.dashRect[0]+self.dashRect[2],self.barRect[1]),(self.barRect[0]+self.barRect[2]-self.dashRect[0]-self.dashRect[2],self.barRect[3]))

        #checks for letting go
        if pygame.mouse.get_pressed()[0] == False and self.clicking == True:
            self.clicking = False
            return True
            

        if self.Hovering(self.dashRect) == True and pygame.mouse.get_pressed()[0] == True and self.clicking == False:
            self.clicking = True
            mousePos = pygame.mouse.get_pos()[0]
            self.mouseDisp = (mousePos-self.barRect[0]-self.relativeDashPos)

        if self.Hovering(leftRect) == True and pygame.mouse.get_pressed()[0] == True and self.clicking == False:
            self.clicking = True
        
        if self.Hovering(rightRect) == True and pygame.mouse.get_pressed()[0] == True and self.clicking == False:
            self.clicking = True

        if self.clicking == True:
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

        if self.Hovering(dashRect) == True:
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
        self.options = optionsList
        self.open = False #toggles if the dropboxes options are visable
        self.currentOption = None
        self.optionsRects = self.GenerateOptionsRects()

    def GenerateOptionsRects(self):
        rectList = []
        for i in range(1,len(self.options)+1):
            rect = pygame.Rect((self.rect[0],self.rect[1]+(self.rect[3]*i),self.rect[2],self.rect[3]))
            rectList.append(rect)
        return rectList

    def Clicked(self):
        if pygame.mouse.get_pressed()[0] == False:
            self.clicking = False

        if self.Hovering(self.rect) == True and self.clicking == False and pygame.mouse.get_pressed()[0] == True:
            self.clicking = True
            if self.open:
                self.currentOption = None
                self.open = False
            else:
                self.open = True
            return True
        
        if self.open:
            for i in range(len(self.optionsRects)):
                if self.Hovering(self.optionsRects[i]) and self.clicking == False and pygame.mouse.get_pressed()[0] == True:
                    self.clicking = True
                    self.currentOption = i
                    self.open = False
                    return True


    
    def Draw(self):
        selectedOption = ""

        if self.currentOption != None:
            selectedOption = self.options[self.currentOption][0]
        else:
            selectedOption = ""

        if self.Hovering(self.rect):
            pygame.draw.rect(self.surf,self.hcolour,self.rect)
        else:
            pygame.draw.rect(self.surf,self.colour,self.rect)
    
        if self.open:

            # sets text for cover button
            text = self.text+":"+selectedOption+"-"

            for  i in range(len(self.options)):
                # centers options text on rect
                rect = self.optionsRects[i]
                otext = self.options[i]
                otextSurf = self.font.render(otext,True,self.fcolour)
                otextSize = self.font.size(otext)
                otPos = (rect[0]+rect[2]/2-otextSize[0]/2,rect[1]+rect[3]/2-otextSize[1]/2)

                if self.Hovering(rect):
                    pygame.draw.rect(self.surf,self.hcolour,rect)
                else:
                    pygame.draw.rect(self.surf,self.colour,rect)
                
                pygame.Surface.blit(self.surf,otextSurf,otPos)
        else:

            #sets text for cover button
            text = self.text+":"+selectedOption+"^"

        #centers cover text
        textSurf = self.font.render(text,True,self.fcolour)
        textSize = self.font.size(text)
        tPos = (self.rect[0]+self.rect[2]/2-textSize[0]/2,self.rect[1]+self.rect[3]/2-textSize[1]/2)
        pygame.Surface.blit(self.surf,textSurf,tPos)


        
    # def Draw(self):
    #     option = ""
    #     if self.currentOption != None:
    #         option = (self.options[self.currentOption])[0]
    #     if self.Hovering(self.rect) == True:
    #         pygame.draw.rect(self.surf,self.hcolour,self.rect)
    #     else:
    #         pygame.draw.rect(self.surf,self.colour,self.rect)

    #     if self.open == True:
    #         combinedText = self.text+":"+option+"-"
    #         textSurf = self.font.render(combinedText,True,self.fcolour)
    #         # handles the options text 
    #         for i in range(1,len(self.options)+1):
    #             text = self.options[i-1]
    #             textSize = self.font.size(text)
    #             tPos = (self.rect[0]+self.rect[2]/2-textSize[0]/2,self.rect[1]+self.box[1]*i+self.box[1]/2-textSize[1]/2)
    #             otherTextSurf = self.font.render((text),True,self.fcolour)
    #             pygame.Surface.blit(self.surf,otherTextSurf,tPos)

    #     else:
    #         combinedText = self.text+":"+option+"^"
    #         textSurf = self.font.render(combinedText,True,self.fcolour)
        
    #     #centers the text on the button
    #     fontsize = self.font.size(combinedText)
    #     tPos = (self.rect[0]+self.rect[2]/2-fontsize[0]/2,self.rect[1]+self.box[1]/2-fontsize[1]/2)
    #     pygame.Surface.blit(self.surf,textSurf,tPos)

