from cmu_112_graphics import *
from Line import *

class Player:    
    def __init__(self):
        # app dimensions
        width = 1200
        height = 850
        
        # start position, player width and height
        self.cx = (width / 2)
        self.cy = (height - 250)
        self.width = 50
        self.height = 65
        
        # movement deltas
        self.dx = 0
        self.dy = 0
        self.ddy = 0
        self.gravity = .6
        self.onGround = False
        
        # player physics numbers and stuff
        self.minVertJump = 5
        self.maxVertJump = 22
        self.horiJumpSpeed = 8
        self.termVel = 20
        
    def drawPlayer(self, app, canvas):
        # draw the player
        # TODO eventually insert the actual player model from the game
        canvas.create_rectangle(self.cx, 
                                self.cy,
                                self.cx + self.width, 
                                self.cy + self.height,
                                fill = 'red')
        # canvas.create_image(self.cx + (self.width / 2), self.cy + self.height, image = ImageTk.PhotoImage(app.playImage), anchor = 's')
        
    # just a helper to set the player's deltas via keyPressed
    def setDeltas(self, dx, dy):
        self.dx = dx
        self.dy = dy
    
    # apply the deltas to the players center point
    def movePlayer(self):
        self.cx += self.dx
        self.cy += self.dy
        
        self.applyGravity()
        
    # apply gravity on the player. finished initial velocity
    # TODO adjust self to incorporate acceleration as well after collision
    def applyGravity(self):
        # check if player is on a "ground" 
        if not(self.onGround):
            self.dy = min(self.dy + self.gravity, self.termVel)
            
        # otherwise, set dy to 0
        else:
            self.dy = 0
            self.onGround = True

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
        
        # ! ok, so there's kind of an issue that we're running into right at the
        # ! beginning. We can't seem to quite understand which line to choose to collide with.
        # ! so this'll be the first issue to combat in a little bit.
        
        # so for every line that's on the screen
        for line in lines:
            # check if it's horizontal
            if(line.isHorizontal):
                # if so, check if the left and right side of the player is within the 
                # the horizontal length of the line in order to apply any effect to it
                if((leftX >= line.x1 and leftX <= line.x2) or (rightX >= line.x1 and rightX <= line.x2)):
                    # since we're within this particular line, check if the bottom of the
                    # player has come into contact with the line.
                    if(line.y1 < bottomY and (line.y1 > rightY or line.y1 > leftY)):
                        # set onGround to True if it has and snap the bottom to the line
                        self.onGround = True
                        self.dy = 0
                        self.cy = line.y1 - self.height
                    
                    # check if the top has collided with a horizontal line
                    elif(line.y1 > topY and (line.y1 < rightY or line.y1 < leftY)):
                        # in that case, snap the top to the line and reverse its upward velocity
                        self.cy = line.y1
                        self.dy = -self.dy
                
                # if the player isn't within the horizontal lines length
                else:
                    pass # ? maybe somthing here so just have it here
            
            # or if it's vertical
            elif(line.isVertical):
                # check if the player is within the vertical length of the line
                if((topY > line.y1 and topY < line.y2) or (bottomY > line.y1 and bottomY < line.y2)):
                    # check if the line is on the right of the player and we're hitting it
                    if(line.x1 < rightX and (line.x1 > topX or line.x1 > bottomX)):
                        # if we're on the ground
                        if(self.onGround):
                            # then simply snap the player's right to the line
                            self.cx = line.x1 - self.width
                        
                        # if we're falling
                        else:
                            # reverse the horizontal velocity after snapping the
                            # player's right to the line
                            self.cx = line.x1 - self.width
                            self.dx = -self.dx
                            
                    # same thing as above except for the left side of the player
                    elif(line.x1 > leftX and (line.x1 < topX or line.x1 < bottomX)):
                        # if we're on the ground, snap the left side to the line
                        if(self.onGround):
                            self.cx = line.x1
                            
                        # otherwise, reverse hori velocity and snap to the line
                        else:
                            self.cx = line.x1
                            self.dx = -self.dx
            
            # TODO figure out how to do diagonal sorting
            # ? take into consideration corner point to diagonal line point thing prof mentioned
            else:
                pass
            
    def jump(self):
        self.dy = -self.maxVertJump
        