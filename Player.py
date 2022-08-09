from cmu_112_graphics import *
from Line import *

class Player:    
    def __init__(self):
        # app dimensions
        width = 1200
        height = 900
        
        # start position, player width and height
        self.cx = (width / 2)
        self.cy = (height - 200)
        self.width = 50
        self.height = 65
        
        # movement deltas and player status
        self.dx = 0
        self.dy = 0
        self.ddy = 0
        self.onGround = False
        self.squatting = False
        self.jumpRight = False
        self.jumpLeft = False
        self.isMoving = False
        self.moveLeft = False
        self.moveRight = False
        
        # player physics numbers and stuff
        # vertical physics (i.e. gravity)
        self.minVertJump = 5
        self.maxVertJump = 22
        self.vertJumpSpeed = self.minVertJump
        self.gravity = .6 # tweak this
        self.horiJumpSpeed = 8
        self.termVel = 20
        
        # horizontal physics (i.e. ice and wind stuff)
        self.maxWind = .3
        self.windAccel = .003
        self.iceAccel = .5
        self.isSlidding = False
        self.walkSpeed = 4
        
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
    def movePlayer(self, level, lines):
        if(level.isIce):
            self.applyIce(lines)
        
        self.cx += self.dx
        self.cy += self.dy
        
        self.applyGravity()
        
    # apply gravity on the player. finished initial velocity
    def applyGravity(self):
        # check if player is on a "ground" 
        if not(self.onGround):
            self.dy = min(self.dy + self.gravity, self.termVel)
            
        # otherwise, set dy to 0
        else:
            self.dy = 0
            
    # ! Still working on this
    def applyIce(self, lines):
        if(self.onGround and not self.isMoving):
            self.isSlidding = True
            
            if(self.dx < 0):
                self.dx += self.iceAccel
            elif(self.dx > 0):
                self.dx -= self.iceAccel
            
            if(self.dx < .1 and self.dx > -.1):
                self.dx = 0
                
        elif(self.onGround and self.isMoving):
            if(self.dx < 4 and self.dx > -4):
                if(self.moveRight):
                    self.dx += self.iceAccel
                elif(self.moveLeft):
                    self.dx -= self.iceAccel  
                    
        self.checkMoveOffLine(lines)                  
            
    # TODO paste citation stuff and continue work on collision
    # ! work on it
        
    # ok so, we have a different plan now. still relatively working along the 
    # same concept maybe but we'll just tinker around with it. I know this has 
    # made you waste like 2 days but shhhhhhhh i think this will work
    
    def checkCollisions(self, lines, level):
        
        # get the lines we've collided with
        collidedLines = self.getCollidedLines(lines)
                
        # * actual collision stuff below                        
        # so for every line we collide with, react accordingly
        if(len(collidedLines) == 1):
            self.reactCollide(collidedLines, level)
        
        # clarify reactions to the prioritized line
        elif(len(collidedLines) >= 2):
            priority = [self.getPriority(collidedLines)]
            if(priority != []):
                self.reactCollide(priority, level)
                
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
        
    def getCollidedLines(self, lines):
        
        collidedWith = []
        
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
        
        for line in lines:
            if(line.isHorizontal):
                if((leftX >= line.x1 and leftX <= line.x2) or (rightX >= line.x1 and rightX <= line.x2) or (line.x1 >= leftX and line.x2 <= rightX)):
                    if(line.y1 < bottomY and (line.y1 > rightY or line.y1 > leftY)):
                        collidedWith.append(line)
                    if(line.y1 > topY and (line.y1 < rightY or line.y1 < leftY)):
                        collidedWith.append(line)
                else:
                    self.checkMoveOffLine(lines)
            elif(line.isVertical):
                if((topY > line.y1 and topY < line.y2) or (bottomY > line.y1 and bottomY < line.y2) or (line.y1 >= topY and line.y2 <= bottomY)):
                    if(line.x1 < rightX and (line.x1 > topX or line.x1 > bottomX)):
                        collidedWith.append(line)
                    elif(line.x1 > leftX and (line.x1 < topX or line.x1 < bottomX)):
                        collidedWith.append(line)
            else:
                left = self.checkDiagLine(tLx, tLy, bLx, bLy, line.x1, line.y1, line.x2, line.y2)
                right = self.checkDiagLine(tRx, tRy, bRx, bRy, line.x1, line.y1, line.x2, line.y2)
                top = self.checkDiagLine(tLx, tLy, tRx, tRy, line.x1, line.y1, line.x2, line.y2)
                bottom = self.checkDiagLine(bLx, bLy, bRx, bRy, line.x1, line.y1, line.x2, line.y2)
                
                if(left[0] or right[0] or top[0] or bottom[0]):
                    collidedWith.append(line)
                            
        return collidedWith
    
    # ! So priority works most of the time. If I ever come back to work on this 
    # ! project again, this'll be a thing I need to fine tune. But for the sake
    # ! of now, it's fine.
    def getPriority(self, lines):
        
        # find out what kind of lines you've bumped into
        hori = None
        vert = None
        diag = None
        
        for line in lines:
            if(line.isHorizontal):
                hori = line
            elif(line.isVertical):
                vert = line
            else:
                diag = line
        
        # player corners
        # player mid height
        midY = self.cy + (self.height / 2)
        
        # top left
        tLx = self.cx
        tLy = self.cy
        
        # top right
        tRx = self.cx + self.width
        tRy = self.cy
        
        # bottom left
        bLx = self.cx
        bLy = self.cy + self.height
        
        # bottom right
        bRx = self.cx + self.width
        bRy = self.cy + self.height
        
        # compare how much we have to correct the player by
        correctX = None
        correctY = None
        
        # if we collided with a horizontal and vertical line
        if(hori != None and vert != None):
            # prioritize top collision info
            if((tLx < vert.x1 and tLy < hori.y1) or (tRx > vert.x1 and tRy < hori.y1)):
                if(self.dx > 0):
                    correctX = abs(tRx - vert.x1)
                    correctY = abs(tRy - hori.y1)
                elif(self.dx < 0):
                    correctX = abs(vert.x1 - tLx)
                    correctY = abs(tLy - hori.y1)
                elif(self.dx == 0):
                    # there's a slight issue when player is on the ground where it isn't
                    # alligning correctly. So we have to make sure that it does
                    
                    # if we're running into a wall left of player that's within proximity of the player
                    if((self.cx <= vert.x1) and (abs(self.cx - vert.x1) < 5)):
                        # snap the left of the player to the line
                        self.cx = vert.x1
                        
                    # if we're running into a wall right of the player that's within proximity of the player
                    elif((self.cx + self.width >= vert.x1) and (abs(self.cx + self.width - vert.x1) < 5)):
                        # snap the right of the player to the line
                        self.cx = vert.x1 - self.width
                    
                    return hori
            
            # if correction variables are still None because the top corners haven't collided
            if(correctX != None and correctY != None):
                # check if we're colliding into the pair o`f lines with the bottom corners of the player
                if((bLx < vert.x1 and bLy > hori.y1) or (bRx > vert.x1 and bRy > hori.y1)):
                    # if we're moving right
                    if(self.dx > 0):
                        # set the correction variables to the difference of the relevant lines' x/y coord
                        correctX = abs(bRx - vert.x1)
                        correctY = abs(bRy - hori.y1)
                        
                    # if we're moving left
                    elif(self.dx < 0):
                        # set the correction variables to the difference of the relevant lines' x/y coord
                        correctX = abs(vert.x1 - bLx)
                        correctY = abs(bLy - hori.y1)
                        
                    # if we're jumping straight up/down
                    elif(self.dx == 0):
                        # there's a slight issue when player is on the ground where it isn't
                        # alligning correctly. So we have to make sure that it does
                        
                        # if we're running into a wall left of player that's within proximity of the player
                        if((self.cx <= vert.x1) and (abs(self.cx - vert.x1) < 5)):
                            # snap the left of the player to the line
                            self.cx = vert.x1

                        # if we're running into a wall right of the player that's within proximity of the player
                        elif((self.cx + self.width >= vert.x1) and (abs(self.cx + self.width - vert.x1) < 5)):
                            # snap the right of the player to the line
                            self.cx = vert.x1 - self.width
                        
                        # regardless of hitting left/right if we're not moving left or right hori line has priority
                        return hori
            
            # make sure that both the correction variables aren't still None
            if(correctX != None and correctY != None):
                # check whether the x/y correction is greater than the other
                # whichever one is lesser we should return the line that causes
                # that correction
                if(correctX > correctY and not correctY < 1):
                    return hori
                elif(correctX < correctY and not correctX < 1):
                    return vert
        
        # if there's ever a diagonal line then return whatever other line that's present
        elif(hori != None and diag != None):
            diagMid = (diag.y1 + diag.y2) / 2
            if(diagMid > hori.y1):
                return hori
        elif(vert != None and diag != None):
            return vert
    
    def reactCollide(self, lines, level):        
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
        
        # * Reactions are below here
        for line in lines:
            # check if it's horizontal
            if(line.isHorizontal):
                # if so, check if the left and right side of the player is within the 
                # the horizontal length of the line in order to apply any effect to it
                if((leftX >= line.x1 and leftX <= line.x2) or (rightX >= line.x1 and rightX <= line.x2) or (line.x1 >= leftX and line.x2 <= rightX)):
                    # since we're within this particular line, check if the bottom of the
                    # player has come into contact with the line.
                    if(line.y1 < bottomY and (line.y1 > rightY or line.y1 > leftY)):
                        # set onGround to True if it has and snap the bottom to the line
                        self.onGround = True
                        self.cy = line.y1 - self.height
                        
                        # TODO Implement the level status effects here. Since this is 
                        # TODO after we've snapped the player to the line and before we
                        # TODO begin changing the player's deltas
                        
                        if(self.jumpLeft):
                            self.jumpLeft = False
                            self.cy = line.y1 - self.height
                        elif(self.jumpRight):
                            self.jumpRight = False
                            self.cy = line.y1 - self.height
                            
                        if(level.isIce):
                            self.applyIce(lines)
                            self.checkMoveOffLine(lines)
                        else:
                            self.dx = 0
                            self.dy = 0
                                                    
                    # check if the top has collided with a horizontal line
                    if(line.y1 > topY and (line.y1 < rightY or line.y1 < leftY) and self.dy < 0):
                        # in that case, snap the top to the line and reverse its upward velocity
                        self.cy = line.y1
                        self.dy = -self.dy
                        
                        if(self.jumpLeft):
                            self.jumpLeft = False
                        elif(self.jumpRight):
                            self.jumpRight = False
                                                    
                        # if the player isn't within the horizontal lines length
                        else:
                            self.checkMoveOffLine(line)
                    
            # or if it's vertical
            elif(line.isVertical):
                if((topY > line.y1 and topY < line.y2) or (bottomY > line.y1 and bottomY < line.y2) or (line.y1 >= topY and line.y2 <= bottomY)):
                    # check if the line is on the right of the player and we're hitting it
                    if(line.x2 < rightX and (line.x2 > topX or line.x2 > bottomX)):
                        # if we're on the ground
                        if(self.onGround):
                            # then simply snap the player's right to the line
                            self.cx = line.x2 - self.width
                        
                        # if we're falling or jumping
                        else:
                            # reverse the horizontal velocity after snapping the
                            # player's right to the line
                            self.cx = line.x2 - self.width
                            self.dx = -(self.dx / 2)
                            
                    # same thing as above except for the left side of the player
                    elif(line.x2 > leftX and (line.x2 < topX or line.x2 < bottomX)):
                        # if we're on the ground, snap the left side to the line
                        if(self.onGround):
                            self.cx = line.x2

                        # otherwise, reverse hori velocity and snap to the line
                        else:
                            self.cx = line.x2
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
                    self.onGround = False
                    
                    self.cx = bottom[1] - 1
                    self.cy = bottom[2] - self.height - 1
                    
                # bottom right
                if(bottom[0] and right[0]):
                    self.dx = -self.dy
                    self.onGround = False

                    self.cx = bottom[1] - self.width - 1
                    self.cy = bottom[2] - self.height - 1