from cmu_112_graphics import *
from Player import *

class Line:
    def __init__(self, x1, y1, x2, y2):
        # start and end point of each line
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        
        # check if the line is horizontal or vertical and assigns the line
        self.isHorizontal = (y1 == y2)
        self.isVertical = (x1 == x2)

        # if it's neither horizontal or vertical then it's diagonal
        self.isDiagonal = not (self.isHorizontal or self.isVertical)
        
    def drawLine(self, app, canvas):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, width = 3)
        
    # TODO make collision logic
    def checkLineLine(self, x1, y1, x2, y2, x3, y3, x4, y4):
        # ! somehow dividing by 0. check it out when you can
        
        uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
        uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
        
        if((uA >= 0 and uA <= 1) and (uB >= 0 and uB <= 1)):
            return True
        else:
            return False