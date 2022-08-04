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
    
    # keep track of all the lines
    app.lines = []
    app.lines.append(Line(0, app.height - 100, app.width, app.height - 100)) #horiz
    # app.lines.append(Line(200, 0, 200, app.height))
    # app.lines.append(Line(app.width - 200, 0, app.width - 200, app.height))
        
    # set default walk speed for player
    app.timerDelay = 10
    app.walkSpeed = 4
    
# Controller ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def keyPressed(app, event):
    if(event.key == 'Left'):
        app.player.setDeltas(-app.walkSpeed, 0)
    elif(event.key == 'Right'):
        app.player.setDeltas(app.walkSpeed, 0)
    elif(event.key == 'Space'):
        app.player.setDeltas(0, app.walkSpeed)
        
    # debug
    elif(event.key == 'r'):
        appStarted(app)
        
def keyReleased(app, event):
    if(event):
        app.player.setDeltas(0, 0)
        
def timerFired(app):
    for line in app.lines:
        app.player.isColliding(line)
    app.player.movePlayer()
    app.player.applyGravity()
    
# View ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def redrawAll(app, canvas):
    for i in range(len(app.lines)):
        app.lines[i].drawLine(app, canvas)
    app.player.drawPlayer(app, canvas)
    
    
runApp(width = 1180, height = 820)