import pygame

class ClickableElemets:
    def __init__(self,pos,box):
        self.pos = pos
        self.box = box
        self.clicked = False
    
    def RegisterClick(self):
        
        
