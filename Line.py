from cmu_112_graphics import *
from Player import *
from Collision import *

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
        
        # store its collision information in each instance of this class
        self.collisions = Collision()
        
    def drawLine(self, app, canvas):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, width = 3)