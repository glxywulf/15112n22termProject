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
            
            # TODO add this back in when you finish getting the collision working
            # ? keep tinkering with the specific values
            # if(self.dy < 20):
            #     self.gravity = self.gravity + (self.gravity * self.ddy)
            # else:
            #     self.dy = 20
            
        # otherwise, set dy to 0
        else:
            self.dy = 0

    # TODO paste citation stuff and continue work on collision
    # TODO write up the collision stuff 
    # ! work on it
    
    # ok so, we have a different plan now. still relatively working along the 
    # same concept maybe but we'll just tinker around with it. I know this has 
    # made you waste like 2 days but shhhhhhhh i think this will work
    
    def checkCollisions(self, lines):
        
        # player sides midpoints
        leftX = self.cx
        leftY = self.cy + (self.height / 2)

        rightX = self.cx + self.width
        rightY = self.cy + (self.height / 2)

        topX = self.cx + (self.width / 2)
        topY = self.cy

        bottomX = self.cx + (self.width / 2)
        bottomY = self.cy + self.height
        
        # player corners
        tLx = self.cx
        tLy = self.cy
        
        tRx = self.cx + self.width
        tRy = self.cy
        
        bLx = self.cx
        bLy = self.cy + self.height
        
        bRx = self.cx + self.width
        bRy = self.cy + self.height
        
        # * actual collision stuff below
        
        # we need to check if the lines are horizontal or vertical first things
        # first. worry about diagonal logic after you get this stuff done
        # let's also sort lines into if they're below, above, on the right/left
                
        for line in lines:
            if(line.isHorizontal):
                if(line.y1 < bottomY and (line.y1 > rightY or line.y1 > leftY)):
                    self.onGround = True
                    self.cy = line.y1 - self.height
                elif(line.y1 > topY and (line.y1 < rightY or line.y1 < leftY)):
                    self.cy = line.y1
                    self.dy = -self.dy
            elif(line.isVertical):
                if(line.x1 < rightX and (line.x1 > topX or line.x1 > bottomX)):
                    if(self.onGround):
                        self.cx = line.x1 - self.width
                    else:
                        self.cx = line.x1 - self.width
                        self.dx = -self.dx
                elif(line.x1 > leftX and (line.x1 < topX or line.x1 < bottomX)):
                    if(self.onGround):
                        self.cx = line.x1
                    else:
                        self.cx = line.x1
                        self.dx = -self.dx
            
            # TODO figure out how to do diagonal sorting
            # ? take into consideration corner point to diagonal line point thing prof mentioned
            else:
                pass
            