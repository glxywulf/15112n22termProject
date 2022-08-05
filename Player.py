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
    # ! still working on it
    
    def checkCollision(self, lines):
        colLines = []
        
        for line in lines:
            if(self.isColliding(line)):
                colLines.append(line)
                
        landing = False
    
    def isColliding(self, line): # ? check code bullets IsCollidingWithLine function in Player class
        # if the line is horizontal
        if(line.isHorizontal):
            # check if the player is close to the line's x and y position
            isPlayerCloseX = ((line.x1 < self.cx and self.cx < line.x2) or 
                              (line.x1 < self.cx + self.width and self.cx + self.width < line.x2) or 
                              (self.cx < line.x1 and line.x1 < self.cx + self.width) or 
                              (self.cx < line.x2 and line.x2 < self.cx + self.width))
            isPlayerCloseY = self.cy < line.y1 and line.y1 < self.cy + self.height
            
            return (isPlayerCloseX and isPlayerCloseY)
        
        # if the line is vertical
        elif(line.isVertical):
            # check if the player is close to the line's x and y position
            isPlayerCloseY = ((line.y1 < self.cy and self.cy < line.y2) or 
                              (line.y1 < self.cy + self.height and self.cy + self.height < line.y2) or 
                              (self.cy < line.y1 and line.y1 < self.cy + self.height) or 
                              (self.cy < line.y2 and line.y2 < self.cy + self.height))
            isPlayerCloseX = self.cx < line.x1 and line.x1 < self.cx + self.width
            
            return (isPlayerCloseX and isPlayerCloseY)

        # if the line is diagonal
        else:
            # line coords
            x1 = line.x1
            y1 = line.y1
            x2 = line.x2
            y2 = line.y2
            
            # top left corner coords
            topLeftX = self.cx
            topLeftY = self.cy

            # top right corner coords
            topRightX = self.cx + self.width
            topRightY = self.cy

            # bottom left corner coords
            botLeftX = self.cx
            botLeftY = self.cy + self.height

            # bottom right corner coords
            botRightX = self.cx + self.width
            botRightY = self.cy + self.height
            
            # check line collisions of player bottom
            left = checkLineLine(topLeftX, topLeftY, botLeftX, botLeftY, x1, y1, x2, y2)

            # check line collisions of player bottom
            right = checkLineLine(topRightX, topRightY, botRightX, botRightY, x1, y1, x2, y2)

            # check line collisions of player bottom
            top = checkLineLine(topLeftX, topLeftY, topRightX, topRightY, x1, y1, x2, y2)

            # check line collisions of player bottom
            bottom = checkLineLine(bottomLeftX, bottomLeftY, bottomRightX, bottomRightY, x1, y1, x2, y2)
            
            
            if(left[0] or right[0] or top[0] or bottom[0]):
                # create a new set of collision information
                lineCollisInfo = Collision()
                
                # set the variables to true if whatever diagonal line has collided with the player
                lineCollisInfo.collidedLeft = left[0]
                lineCollisInfo.collidedRight = right[0]
                lineCollisInfo.collidedTop = top[0]
                lineCollisInfo.collidedBottom = bottom[0]
                
                # add a tuple of the coordinates that intersected with the line to
                # the list inside of the Collision object
                if(left[0]):
                    lineCollisInfo.collidedPoints.append((left[1], left[2]))
                if(right[0]):
                    lineCollisInfo.collidedPoints.append((right[1], right[2]))
                if(top[0]):
                    lineCollisInfo.collidedPoints.append((top[1], top[2]))
                if(bottom[0]):
                    lineCollisInfo.collidedPoints.append((bottom[1], bottom[2]))
                
                # set the inputted line's collision object to whatever we have just
                # newly made
                line.collisions = lineCollisInfo
                
                return True
            
            else:
                return False

    # in the case we collide with two lines, we have to check which one we
    # should prioritize when it comes to landing or bouncing off of it
    # TODO prolly cite stuff 
    def getPriority(self, lines):
        # if there are no lines we're colliding against we don't need to return
        # anything since there would be nothing to return
        if(len(lines) == 0): return None
        
        # we should only care if we come into contact with exactly two lines
        if(len(lines) == 2):
            # set variables to None and assign them later to get orientations
            # of the 2 lines that we collided with
            vertical = None
            horizontal = None
            diagonal = None
            
            # now we check if either line in lines is vert/hori/diag and set
            # the above variables to be that line
            if(lines[0].isVertical):
                vertical = lines[0]
            if(lines[0].isHorizontal):
                horizontal = lines[0]
            if(lines[0].isDiagonal):
                diagonal = lines[0]
            if(lines[1].isVertical):
                vertical = lines[1]
            if(lines[1].isHorizontal):
                horizontal = lines[1]
            if(lines[1].isDiagonal):
                diagonal = lines[1]
                
            # now we have to check each possible case that the pair of lines
            # could be; vert/hori, hori/diag, and diag/vert. although diag/vert
            # doesn't actually have any impact in the real game so we'll ignore
            # it for now
            if((vertical != None) and (horizontal != None)):
                # calculate the mid Ys of each line so we can compare them later
                # technically the horizontal midline calculation is unnecessary
                # but I want to be consistent
                vertYMid = (vertical.y1 + vertical.y2) / 2
                horiYMid = (horizontal.y1 + horizontal.y2) / 2
                
                # if the player is moving up
                if(self.dy < 0):
                    # if the midY of the vertical line is greater when the 
                    # player is moving up, then priority goes to the vertical line
                    # this would be a top right corner when imagined
                    if(vertYMid > horiYMid):
                        return vertical
                    
                    # otherwise, priority goes to the horizontal line
                    else:
                        return horizontal
                    
                # in the case that the player is moving down
                else:
                    # if the midY of the vertical line is below the y of the
                    # horizontal line, then the vertical line gets priority
                    # this is a top left corner when imagined
                    if(vertYMid < horiYMid):
                        return vertical
                    
                    # horizontal gets priority otherwise
                    else:
                        return horizontal
            
            # if the pair of lines are horizontal and diagonal
            if((horizontal != None) and (diagonal != None)):
                horiYMid = (horizontal.y1 + horizontal.y2) / 2
                diagYMid = (diagonal.y1 + diagonal.y2) / 2
                
                # if the diagonal line's midY is below the horizontal, we want
                # to prioritize the horizontal line. since we've techinically 
                # landed on the horizontal already
                if(horiYmid < diagYmid):
                    return horizontal
                
                # diagonal gets priority otherwise
                else:
                    return diagonal
                
        # now we have to correct
        # ? maybe come back to this.  
        for line in lines:
            directedCorrectX = 0
            directedCorrectY = 0
            correction = None
            
            if(line.isHorizontal):
                if(self.dy < 0):
                    directedCorrectY = line.y1 - (self.cy + self.height)
                    correction = abs(self.cy - (line.y1 - self.height))
                else:
                    directedCorrectY = line.y1 - self.cy
            
            # ! line 987 of player class

    # function to check if lines are colliding with each other based on points
    # of lines and points of player using some math formulas
    # TODO paste citation stuff
    def checkLineLine(self, x1, y1, x2, y2, x3, y3, x4, y4):  
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