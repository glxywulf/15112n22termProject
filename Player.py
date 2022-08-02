from cmu_112_graphics import *

class Player:    
    def __init__(self):
        width = 1180
        height = 820
        
        self.pos = (width / 2, height - 200)
        self.width = 50
        self.height = 65
        
    def drawPlayer(self, app, canvas):
        (cx, cy) = self.pos
        canvas.create_rectangle(cx - (self.width / 2), cy - self.height / 2,
                                cx + (self.width / 2), cy + self.height / 2,
                                fill = 'red')
        