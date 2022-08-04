from cmu_112_graphics import *
from Line import *

class Player:    
    def __init__(self):
        # app dimensions
        width = 1180
        height = 820
        
        # start position, player width and height
        self.cx = (width / 2)
        self.cy = (height - 300)
        self.width = 50
        self.height = 65
        
        # movement deltas
        self.dx = 0
        self.dy = 0
        self.ddy = 0
        self.gravity = 1
        self.onGround = False
        
    def drawPlayer(self, app, canvas):
        # draw the player
        # TODO eventually insert the actual player model from the game
        canvas.create_rectangle(self.cx, 
                                self.cy,
                                self.cx + self.width, 
                                self.cy + self.height,
                                fill = 'red')
        
    # just a helper to set the player's deltas via keyPressed
    def setDeltas(self, dx, dy):
        self.dx = dx
        self.dy = dy
    
    # apply the deltas to the players center point
    def movePlayer(self):
        self.cx += self.dx
        self.cy += self.dy
        
    # apply gravity on the player. finished initial velocity
    # TODO adjust self to incorporate acceleration as well after collision
    def applyGravity(self):
        # check if player is on a "ground" 
        if not(self.onGround):
            # if not, apply a gravity constant on the dy
            self.dy = self.gravity
        # otherwise, set dy to 0
        else:
            self.dy = 0

    # TODO paste citation stuff and continue work on collision
    def isColliding(self, line):        
        # line coords
        x1 = line.x1
        y1 = line.y1
        x2 = line.x2
        y2 = line.y2
        
        # player left coords
        lx1, ly1, lx2, ly2 = (self.cx, self.cy, self.cx, self.cy + self.height)
        
        # player right coords
        rx1, ry1, rx2, ry2 = (self.cx + self.width, self.cy, self.cx + self.width, self.cy + self.height)
        
        # player top coords
        tx1, ty1, tx2, ty2 = (self.cx, self.cy, self.cx + self.width, self.cy)
        
        # player bottom coords
        bx1, by1, bx2, by2 = (self.cx, self.cy + self.height, self.cx + self.width, self.cy + self.height)
        
        if(self.areLinesColliding(x1, y1, x2, y2, bx1, by1, bx2, by2)[0]):
            self.onGround = True
            self.cy = y1 - self.height
        
        
    # function to check if lines are colliding with each other based on points
    # of lines and points of player
    # TODO paste citation stuff
    def areLinesColliding(self, x1, y1, x2, y2, x3, y3, x4, y4):
        if(((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)) == 0):
            uA = 42
            uB = 42
        else:
            uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
            uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
        
        if((uA >= 0 and uA <= 1) and (uB >= 0 and uB <= 1)):
            intersectionX = x1 + (uA * (x2 - x1))
            intersectionY = y1 + (uA * (y2 - y1))
            return [True, intersectionX, intersectionY]
        
        return [False, 0, 0]