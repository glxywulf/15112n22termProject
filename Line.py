# Images and level line coordinates copied from: https://github.com/Code-Bullet/Jump-King/tree/321506e725ef448654936837672d9fe8fba123bb 
# Image loading code from: https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
# Specific player acceleration values and movement speeds copied from link above and tweaked to fit the timing of CMU graphics
# Idea on how to implement collision priority: https://www.youtube.com/watch?v=DmQ4Dqxs0HI
# Diagonal line collision formula taken from: https://www.jeffreythompson.org/collision-detection/line-line.php 

from cmu_112_graphics import *
from Player import *

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
        
        # if it's diagonal we want to keep the order that it was inputted in
        else:
            self.x1 = x1
            self.y1 = y1
            self.x2 = x2
            self.y2 = y2
        
    # Line class function which helps to just draw the line
    def drawLine(self, app, canvas):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, width = 3)