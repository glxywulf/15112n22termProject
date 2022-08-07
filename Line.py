from cmu_112_graphics import *
from Player import *
from Collision import *

class Line:
    def __init__(self, x1, y1, x2, y2):
        # check if the line is horizontal or vertical and assigns the line
        self.isHorizontal = (y1 == y2)
        self.isVertical = (x1 == x2)
        
        # if it's neither horizontal or vertical then it's diagonal
        self.isDiagonal = not (self.isHorizontal or self.isVertical)
        
        # if it's horizontal or vertical we need to keep track of which x/y
        # is x1/y1 and x1/y2 so we set it like this
        if(self.isHorizontal or self.isVertical):
            self.x1 = min(x1, x2)
            self.y1 = min(y1, y2)
            self.x2 = max(x1, x2)
            self.y2 = max(y1, y2)
        
        # if it's horizontal we want to keep the order that it was inputted in
        else:
            self.x1 = x1
            self.y1 = y1
            self.x2 = x2
            self.y2 = y2
        
                
    def drawLine(self, app, canvas):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, width = 3)