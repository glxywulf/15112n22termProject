from cmu_112_graphics import *

class Player:    
    def __init__(self):
        # app dimensions
        width = 1180
        height = 820
        
        # start position, player width and height
        self.cx = (width / 2)
        self.cy = (height - 200)
        self.width = 50
        self.height = 65
        
        # movement deltas
        self.dx = 0
        self.dy = 0
        self.ddy = 0
        self.onGround = False
        
    def drawPlayer(self, app, canvas):
        # draw the player
        # TODO eventually insert the actual player model from the game
        canvas.create_rectangle(self.cx - (self.width / 2), 
                                self.cy - (self.height / 2),
                                self.cx + (self.width / 2), 
                                self.cy + (self.height / 2),
                                fill = 'red')
        
    def setDeltas(self, dx, dy):
        self.dx = dx
        self.dy = dy
    
    def movePlayer(self):
        self.cx += self.dx
        self.cy += self.dy
        