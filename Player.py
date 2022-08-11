# Images and level line coordinates copied from: https://github.com/Code-Bullet/Jump-King/tree/321506e725ef448654936837672d9fe8fba123bb 
# Image loading code from: https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
# Specific player acceleration values and movement speeds copied from link above and tweaked to fit the timing of CMU graphics
# Idea on how to implement collision priority: https://www.youtube.com/watch?v=DmQ4Dqxs0HI
# Diagonal line collision formula taken from: https://www.jeffreythompson.org/collision-detection/line-line.php 

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
        self.faceRight = True
        
        # player physics numbers and stuff
        # vertical physics (i.e. gravity)
        self.minVertJump = 5
        self.maxVertJump = 23
        self.vertJumpSpeed = self.minVertJump
        self.gravity = .6 
        self.horiJumpSpeed = 8
        self.termVel = 20
        
        # horizontal physics (i.e. ice and wind stuff)
        self.maxWind = 8
        self.windAccel = .4
        self.windMoveRight = False
        self.iceAccel = .5
        self.isSlidding = False
        self.walkSpeed = 4
        
    # draw the player
    def drawPlayer(self, app, canvas):
        # TODO work on sprite animation
        if(self.isMoving and self.onGround):
            if(self.faceRight):
                sprite = app.sprites[app.currSprite]
                canvas.create_image(self.cx + self.width / 2, self.cy + self.height + 1, 
                                    image = ImageTk.PhotoImage(sprite), anchor = 's')
            else:
                sprite = app.invSprites[app.currSprite]
                canvas.create_image(self.cx + self.width / 2, self.cy + self.height + 1, 
                                    image = ImageTk.PhotoImage(sprite), anchor = 's')
        elif(self.onGround and not self.isMoving):
            if not(self.squatting):
                if(self.faceRight):
                    canvas.create_image(self.cx + self.width / 2, self.cy + self.height + 1, 
                                        image = ImageTk.PhotoImage(app.avatar), anchor = 's')
                else:
                    canvas.create_image(self.cx + self.width / 2, self.cy + self.height + 1, 
                                        image = ImageTk.PhotoImage(app.invAva), anchor = 's')
            else:
                canvas.create_image(self.cx + self.width / 2, self.cy + self.height + 1, 
                                    image = ImageTk.PhotoImage(app.squatAva), anchor = 's')
        
        elif not(self.onGround):
            if(self.faceRight and self.dx < 0):
                canvas.create_image(self.cx + self.width / 2, self.cy + self.height + 1, 
                                    image = ImageTk.PhotoImage(app.avaBump), anchor = 's')
            elif(not self.faceRight and self.dx > 0):
                canvas.create_image(self.cx + self.width / 2, self.cy + self.height + 1, 
                                    image = ImageTk.PhotoImage(app.invBump), anchor = 's')
            else:
                if(self.faceRight):
                    if(self.dy < 0):
                        canvas.create_image(self.cx + self.width / 2, self.cy + self.height + 1, 
                                            image = ImageTk.PhotoImage(app.avaJump), anchor = 's')
                    else:
                        canvas.create_image(self.cx + self.width / 2, self.cy + self.height + 1, 
                                            image = ImageTk.PhotoImage(app.avaFall), anchor = 's')
                else:
                    if(self.dy < 0):
                        canvas.create_image(self.cx + self.width / 2, self.cy + self.height + 1, 
                                            image = ImageTk.PhotoImage(app.invJump), anchor = 's')
                    else:
                        canvas.create_image(self.cx + self.width / 2, self.cy + self.height + 1, 
                                            image = ImageTk.PhotoImage(app.invFall), anchor = 's')
                    


        
    # just a helper to set the player's deltas via keyPressed
    def setDeltas(self, dx, dy):
        self.dx = dx
        self.dy = dy
    
    # apply the deltas to the players center point
    def movePlayer(self, level, lines):
        # move the positional coords according to the deltas
        self.cx += self.dx
        self.cy += self.dy
        
        # no matter what apply gravity as the player moves
        self.applyGravity()
        
    # apply gravity on the player. finished initial velocity
    def applyGravity(self):
        # check if player is on a "ground" 
        if not(self.onGround):
            self.dy = min(self.dy + self.gravity, self.termVel)
            
        # otherwise, set dy to 0
        else:
            self.dy = 0
    
    # apply ice physics to ice levels
    def applyIce(self, lines):
        # if player is on the ground and not moving
        if(self.onGround and not self.isMoving):
            # set slidding to True
            self.isSlidding = True
            
            # depending on moving left or right add the deceleration in the opposite direction
            if(self.dx < 0):
                self.dx += self.iceAccel
            elif(self.dx > 0):
                self.dx -= self.iceAccel
            
            # if the dx gets small enough just set it back to 0
            if(self.dx < .1 and self.dx > -.1):
                self.dx = 0
        
        # tries to accelerate player when on the ice. 
        elif(self.onGround and self.isMoving):
            if(self.dx < 4 and self.dx > -4):
                if(self.moveRight):
                    self.dx += self.iceAccel
                elif(self.moveLeft):
                    self.dx -= self.iceAccel  
        
        # check if we've moved off the line and act accordingly
        self.checkMoveOffLine(lines)
    
    # apply wind physics to player
    def applyWind(self):
        # if player isn't on the ground
        if not(self.onGround):
            # check what direction the wind is pushing at the moment and add to 
            # the dx in a accelerating fashion
            if(self.windMoveRight):
                self.dx = min(self.dx + self.windAccel, self.maxWind)
            else:
                self.dx = max(self.dx - self.windAccel, -self.maxWind)
                    
    # checks the collisions and causes reactions 
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
    
    # helper function to help check whether or not we should change the level
    # returns a boolean and int in a list which holds whether or not there should
    # be a level change and whether it's to the next/previous level
    def changeLevel(self):
        # if the bottom of the player is above the top of the window, go to the next level
        if(self.cy + self.height < 0):
            return [True, +1]
        
        # or if the top of the player reaches the bottom of the screen, go to the previous level
        elif(self.cy > 900 and self.dy > 0):
            return [True, -1]
        
        # otherwise just do nothing
        else:
            return [False, 0]
    
    # get the lines that the player has collided with
    def getCollidedLines(self, lines):
        # list of collided lines
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
        
        # check every line in the level
        for line in lines:
            # if the line is horizontal
            if(line.isHorizontal):
                # check if the player is within the X and Y of the line
                if((leftX >= line.x1 and leftX <= line.x2) or (rightX >= line.x1 and rightX <= line.x2) or (line.x1 >= leftX and line.x2 <= rightX)):
                    # check if the bottom collided with the line that's within range
                    if(line.y1 < bottomY and (line.y1 > rightY or line.y1 > leftY)):
                        collidedWith.append(line)
                    
                    # check if the top collided with the line that's within range
                    if(line.y1 > topY and (line.y1 < rightY or line.y1 < leftY)):
                        collidedWith.append(line)
                
                # if we aren't in range, call checkMoveOffLine
                else:
                    self.checkMoveOffLine(lines)
                    
            # if the line is vertical
            elif(line.isVertical):
                # check if we're within X and Y range of the line
                if((topY > line.y1 and topY < line.y2) or (bottomY > line.y1 and bottomY < line.y2) or (line.y1 >= topY and line.y2 <= bottomY)):
                    # check if the right or left of the player has come into contact with the line
                    # if so, add them to the list of collided lines
                    if(line.x1 < rightX and (line.x1 > topX or line.x1 > bottomX)):
                        collidedWith.append(line)
                    elif(line.x1 > leftX and (line.x1 < topX or line.x1 < bottomX)):
                        collidedWith.append(line)
            
            # if the line is diagonal
            else:
                # check if any side of the player comes into contact with the diagonal line
                left = self.checkDiagLine(tLx, tLy, bLx, bLy, line.x1, line.y1, line.x2, line.y2)
                right = self.checkDiagLine(tRx, tRy, bRx, bRy, line.x1, line.y1, line.x2, line.y2)
                top = self.checkDiagLine(tLx, tLy, tRx, tRy, line.x1, line.y1, line.x2, line.y2)
                bottom = self.checkDiagLine(bLx, bLy, bRx, bRy, line.x1, line.y1, line.x2, line.y2)
                
                # if any are True then add it to collided lines
                if(left[0] or right[0] or top[0] or bottom[0]):
                    collidedWith.append(line)
                            
        return collidedWith
    
    # ! So priority works most of the time. If I ever come back to work on this 
    # ! project again, this'll be a thing I need to fine tune. 
    # get the line we should collide with if we come into contact with >= 2 lines
    def getPriority(self, lines):
        
        # find out what kind of lines you've bumped into
        hori = None
        vert = None
        diag = None
        
        # check what kind of lines they are
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
                    
                    if(hori != None):
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
                        if(hori != None):
                            return hori
            
            # make sure that both the correction variables aren't still None
            if(correctX != None and correctY != None):
                # check whether the x/y correction is greater than the other
                # whichever one is lesser we should return the line that causes
                # that correction
                if(correctX > correctY and not correctY < 1 and hori != None):
                    return hori
                elif(correctX < correctY and not correctX < 1 and vert != None):
                    return vert
        
        # if there's ever a diagonal line then return whatever other line that's present
        elif(hori != None and diag != None):
            diagMid = (diag.y1 + diag.y2) / 2
            if(diagMid > hori.y1):
                return hori
            else:
                return diag
            
        # vertical lines have priority over diagonal lines
        elif(vert != None and diag != None):
            return vert
        
        # if there are only diagonal lines just return the diagonal line
        elif(vert == None and hori == None):
            return diag
    
    # defines how the player should react to all three types of lines
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
            if(line == None):
                continue
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
                        
                        # if we're jumping left or right and we've landed, set
                        # jumpRight/Left to False and snap the player to the line
                        if(self.jumpLeft):
                            self.jumpLeft = False
                            self.cy = line.y1 - self.height
                        elif(self.jumpRight):
                            self.jumpRight = False
                            self.cy = line.y1 - self.height
                        
                        # if the level is an ice level apply ice physics to the line
                        if(level.isIce):
                            self.applyIce(lines)
                            self.checkMoveOffLine(lines)
                        
                        # if it's not an ice level than just set deltas to 0
                        else:
                            self.dx = 0
                            self.dy = 0
                                                    
                    # check if the top has collided with a horizontal line
                    if(line.y1 > topY and (line.y1 < rightY or line.y1 < leftY) and self.dy < 0):
                        # in that case, snap the top to the line and reverse its upward velocity
                        self.cy = line.y1
                        self.dy = -self.dy
                        
                        # set jump directions to false
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
            
            # diagonal line collision
            else:
                # check what sides are in contact with the diagonal
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