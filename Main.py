from cmu_112_graphics import *
from Line import *
from Player import *

# Model ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def appStarted(app):    
    app.width = 1180
    app.height = 820
    
# Controller ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    
# View ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def redrawAll(app, canvas):
    testLine = Line(0, app.height - 100, app.width, app.height - 100)
    king = Player()
    
    testLine.drawLine(app, canvas)
    king.drawPlayer(app, canvas)
    
    
runApp(width = 1180, height = 820)