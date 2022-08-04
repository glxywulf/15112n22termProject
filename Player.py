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
        # if the line is horizontal
        # TODO keep tweaking horizontal collision because it only kinda works
        # ! Any collision with horizontal lines causes the bottom of the player to snap to the collided line 
        if(line.isHorizontal):
            isPlayerCloseX = ((line.x1 < self.cx and self.cx < line.x2) or 
                              (line.x1 < self.cx + self.width and self.cx + self.width < line.x2) or 
                              (self.cx < line.x1 and line.x1 < self.cx + self.width) or 
                              (self.cx < line.x2 and line.x2 < self.cx + self.width))
            isPlayerCloseY = self.cy < line.y1 and line.y1 < self.cy + self.height
            
            if (isPlayerCloseX and isPlayerCloseY):
                self.onGround = True
                self.cy = line.y1 - self.height
        
        # if the line is vertical
        # TODO after you're done with horizontal, apply similar logic to vertical lines
        # ! same issue as horizontal lines
        elif(line.isVertical):
            isPlayerCloseY = ((line.y1 < self.cy and self.cy < line.y2) or 
                              (line.y1 < self.cy + self.height and self.cy + self.height < line.y2) or 
                              (self.cy < line.y1 and line.y1 < self.cy + self.height) or 
                              (self.cy < line.y2 and line.y2 < self.cy + self.height))
            isPlayerCloseX = self.cx < line.x1 and line.x1 < self.cx + self.width
            
            if(isPlayerCloseY and (self.cx > line.x1)):
                # print(self.cx, line.x1, line.x2)
                # print(isPlayerCloseX, isPlayerCloseY)
                
                self.cx = line.x1
            
            elif(isPlayerCloseY and (line.x1 > self.cx + self.width)):
                # print(self.cx, line.x1, line.x2)
                # print(isPlayerCloseX, isPlayerCloseY)
                
                self.cx = line.x1 - self.width
        
        # if the line is diagonal
        # TODO finish diagonal logic
        else:
            # line coords
            x1 = line.x1
            y1 = line.y1
            x2 = line.x2
            y2 = line.y2
            
            # top left corner
            topLeftX = self.cx
            topLeftY = self.cy

            # top right corner
            topRightX = self.cx + self.width
            topRightY = self.cy

            # bottom left corner
            botLeftX = self.cx
            botLeftY = self.cy + self.height

            # bottom right corner
            botRightX = self.cx + self.width
            botRightY = self.cy + self.height
            
            # TODO keep working on collision shit
            if(self.areLinesColliding(botLeftX, botLeftY, botRightX, botRightY, x1, y1, x2, y2)[0]):
                self.onGround = True
                self.cy = y1 - self.height
        
    # function to check if lines are colliding with each other based on points
    # of lines and points of player
    # TODO paste citation stuff
    # TODO keep fucking around with the collision logic
    def areLinesColliding(self, x1, y1, x2, y2, x3, y3, x4, y4):  
        uA = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))      
        uB = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
        
        if((uA >= 0 and uA <= 1) and (uB >= 0 and uB <= 1)):
            interX = x1 + (uA * (x2 - x1))
            interY = y1 + (uA * (y2 - y1))
            return [True, interX, interY]
        
        return [False, 0, 0]