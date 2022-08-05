from cmu_112_graphics import *
from Line import *
from Player import *
from lvlImages import *

# Model ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def appStarted(app):    
    # window dimensions
    app.width = 1200
    app.height = 850
    
    # make the plaer
    app.player = Player()
    
    # keep track of all the lines
    app.lines = []
    
    app.lines.append(Line(20, 0, 20, 460))
    app.lines.append(Line(20, 460, 320, 460))
    app.lines.append(Line(320, 460, 320, 820))
    app.lines.append(Line(320, 820, 880, 820))
    app.lines.append(Line(880, 820, 880, 460))
    app.lines.append(Line(880, 460, 1180, 460))
    app.lines.append(Line(1180, 460, 1180, 0))
    app.lines.append(Line(460, 100, 740, 100))
    app.lines.append(Line(460, 100, 460, 220))
    app.lines.append(Line(460, 220, 740, 220))
    app.lines.append(Line(740, 220, 740, 100))
    
    app.image1 = app.loadImage('1.png')
    
    # * testing lines-------------------------------
    # horizontal pair
    # app.lines.append(Line(0, 100, app.width, 100))
    # app.lines.append(Line(0, app.height - 100, app.width, app.height - 100)) #horiz
    
    # vertical pair
    # app.lines.append(Line(200, 0, 200, app.height))
    # app.lines.append(Line(app.width - 200, 0, app.width - 200, app.height))
    
    # diagonal line
    # app.lines.append(Line(0,0,app.width,app.height)) #diag
    # * testing lines-------------------------------
        
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
        app.player.onGround = False
        app.player.setDeltas(0, -app.walkSpeed)
        
    # debug
    elif(event.key == 'r'):
        appStarted(app)
        
def keyReleased(app, event):
    if(event):
        app.player.setDeltas(0, 0)
        
def timerFired(app):
    app.player.checkCollisions(app.lines)
    app.player.movePlayer()
    app.player.applyGravity()
    
# View ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def redrawAll(app, canvas):
    canvas.create_image(0, 0, image = ImageTK.PhotoImage(app.image1))
    for i in range(len(app.lines)):
        app.lines[i].drawLine(app, canvas)
    app.player.drawPlayer(app, canvas)
    
    
runApp(width = 1200, height = 850)