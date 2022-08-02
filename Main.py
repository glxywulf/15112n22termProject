from cmu_112_graphics import *
from Line import *
from Player import *

# Model ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def appStarted(app):    
    # window dimensions
    app.width = 1180
    app.height = 820
    
    # make the plaer
    app.player = Player()
    
    # set default walk speed for player
    app.timerDelay = 10
    app.walkSpeed = 5
    
# Controller ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def keyPressed(app, event):
    if(event.key == 'Left'):
        app.player.setDeltas(-app.walkSpeed, 0)
    elif(event.key == 'Right'):
        app.player.setDeltas(app.walkSpeed, 0)
        
def keyReleased(app, event):
    if(event):
        app.player.setDeltas(0, 0)
        
def timerFired(app):
    app.player.movePlayer()
    
# View ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def redrawAll(app, canvas):
    testLine = Line(0, app.height - 100, app.width, app.height - 100)
    
    testLine.drawLine(app, canvas)
    app.player.drawPlayer(app, canvas)
    
    
runApp(width = 1180, height = 820)