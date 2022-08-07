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
        self.vertJumpSpeed = self.minVertJump
        self.horiJumpSpeed = 8
        self.termVel = 20
        self.squatting = False
        self.jumpRight = False
        self.jumpLeft = False
        
    def drawPlayer(self, app, canvas):
        # draw the player
        # TODO eventually insert the actual player model from the game
        if not(self.squatting):
            canvas.create_rectangle(self.cx, 
                                    self.cy,
                                    self.cx + self.width, 
                                    self.cy + self.height,
                                    fill = 'red')
            # canvas.create_image(self.cx + self.width / 2, self.cy + self.height, 
            #                     image = ImageTk.PhotoImage(app.avatar), anchor = 's')
        else:
            canvas.create_rectangle(self.cx,
                                    self.cy + (self.height / 2),
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

    # TODO paste citation stuff and continue work on collision
    # TODO write up the collision stuff 
    # ! work on it
    
    def checkLevelStatus(self, level):
        return 42
        
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
            
            # TODO Here's probably a good place to check what kind of level we're on
            # TODO so we can just set different conditional gates to allow certain kinds of collision
            
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
                        self.cy = line.y1 - self.height
                        
                        if(self.jumpLeft):
                            self.jumpLeft = False
                            self.cy = line.y1 - self.height
                        elif(self.jumpRight):
                            self.jumpRight = False
                            self.cy = line.y1 - self.height
                            
                        self.dx = 0
                        self.dy = 0
                    
                    # check if the top has collided with a horizontal line
                    if(line.y1 > topY and (line.y1 < rightY or line.y1 < leftY)):
                        # in that case, snap the top to the line and reverse its upward velocity
                        self.cy = line.y1
                        self.dy = -self.dy
                        
                        if(self.jumpLeft):
                            self.jumpLeft = False
                        elif(self.jumpRight):
                            self.jumpRight = False
                                            
                # if the player isn't within the horizontal lines length
                else:
                    self.checkMoveOffLine(lines)
            
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
                        
                        # if we're falling or jumping
                        else:
                            # reverse the horizontal velocity after snapping the
                            # player's right to the line
                            self.cx = line.x1 - self.width
                            self.dx = -(self.dx / 2)
                            
                    # same thing as above except for the left side of the player
                    elif(line.x1 > leftX and (line.x1 < topX or line.x1 < bottomX)):
                        # if we're on the ground, snap the left side to the line
                        if(self.onGround):
                            self.cx = line.x1
                            
                        # otherwise, reverse hori velocity and snap to the line
                        else:
                            self.cx = line.x1
                            self.dx = -(self.dx / 2)
            
            # TODO figure out how to do diagonal sorting
            # ? take into consideration corner point to diagonal line point thing prof mentioned
            else:
                left = self.checkDiagLine(tLx, tLy, bLx, bLy, line.x1, line.y1, line.x2, line.y2)
                right = self.checkDiagLine(tRx, tRy, bRx, bRy, line.x1, line.y1, line.x2, line.y2)
                top = self.checkDiagLine(tLx, tLy, tRx, tRy, line.x1, line.y1, line.x2, line.y2)
                bottom = self.checkDiagLine(bLx, bLy, bRx, bRy, line.x1, line.y1, line.x2, line.y2)
                
                # top left
                if(top[0] and left[0]):
                    self.dy = -self.dy
                                    
                # top right
                if(top[0] and right[0]):
                    self.dy = -self.dy
                                    
                # bottom left
                if(bottom[0] and left[0]):
                    self.dx = self.dy
                    
                    self.cx = bottom[1]
                    self.cy = bottom[2] - self.height
                
                # bottom right
                if(bottom[0] and right[0]):
                    self.dx = -self.dy

                    self.cx = bottom[1] - self.width
                    self.cy = bottom[2] - self.height
    
    # checks if the player has moves off of the current horizontal line that it is resting on
    def checkMoveOffLine(self, lines):
        # first check if player is on the ground, if so run the check
        if(self.onGround):
            # set a temp variable which will hold what line the player is currently on
            onLine = None
            
            # loop through all of the lines
            for line in lines:
                # if the line is horizontal and it's y is == the y of the bottom of the player
                if(line.isHorizontal and line.y1 == (self.cy + self.height)):
                    # set onLine to be that line
                    onLine = line
                    
                    # initialize varibles that know the x position of the left and right of the player
                    left = self.cx        
                    right = self.cx + self.width
                    
                    # check that onLine isn't None
                    if(onLine != None):
                        # if the player is off of the line, set onGround to False
                        if((left > onLine.x2 and right > onLine.x2) or (left < onLine.x1 and right < onLine.x1)):
                            self.onGround = False
                        
                        # otherwise, onGround should be True and snap the player to the line
                        else:
                            self.cy = onLine.y1 - self.height
                            self.onGround = True
                            
                            # break the for loop here so if doesn't accidentally
                            # set onLine to a different line
                            break
                    
                    # if online is None, make sure onGround is False since we're not on a line
                    else:
                        self.onGround = False

    # function to check if lines are colliding with each other based on points
    # of lines and points of player using some math formulas
    # TODO paste citation stuff
    def checkDiagLine(self, x1, y1, x2, y2, x3, y3, x4, y4):  
        uA = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))      
        uB = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
        
        # if uA and uB are within 0-1 inclusive, then the pair of lines are colliding
        if((uA >= 0 and uA <= 1) and (uB >= 0 and uB <= 1)):
            interX = x1 + (uA * (x2 - x1))
            interY = y1 + (uA * (y2 - y1))
            
            # return True and the point at which there is an intersection
            return [True, interX, interY]
        
        # return false otherwise
        return [False, 0, 0]

    # function that allows player to jump.
    def jump(self):
        # set's the dy to - vertJumpSpeed which increments whenever space is pressed
        # when getting ready to jump you are squatting, so when you jump you shouldnt be anymore
        self.dy = -self.vertJumpSpeed
        self.squatting = False
        
        # if jumpRight is True we should jump right at the fixed horizontal jumpSpeed
        if(self.jumpRight):
            self.dx = self.horiJumpSpeed
        
        # if jumpLeft is True, same as right just in the left direction
        elif(self.jumpLeft):
            self.dx = -self.horiJumpSpeed
            
        # if neither are true just jump with no horizontal velocity
        else:
            self.dx = 0
            
    def changeLevel(self):
        if(self.cy + self.height < 0):
            return [True, +1]
        elif(self.cy > 850 and self.dy > 0):
            return [True, -1]
        else:
            return [False, 0]