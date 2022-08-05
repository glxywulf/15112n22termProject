from cmu_112_graphics import *
from Line import *
from Player import *
from lvlImages import *

# Model ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def appStarted(app):    
    # window dimensions
    app.width = 1200
    app.height = 850
    
    # make the player
    app.player = Player()
    
    # keep track of all the lines
    app.lines = []
    
    # test first level stuff
    app.lines.append(Line(20, 0, 20, 460))
    app.lines.append(Line(20, 460, 320, 460))
    app.lines.append(Line(320, 460, 320, 820))
    app.lines.append(Line(320, 820, 880, 820))
    app.lines.append(Line(880, 460, 880, 820))
    app.lines.append(Line(880, 460, 1180, 460))
    app.lines.append(Line(1180, 0, 1180, 460))
    app.lines.append(Line(460, 100, 740, 100))
    app.lines.append(Line(460, 100, 460, 220))
    app.lines.append(Line(460, 220, 740, 220))
    app.lines.append(Line(740, 100, 740, 220))
    
    # test image stuffs
    app.image1 = app.loadImage('lvlImages/1.png')
    app.playImage = app.loadImage('idle.png')
    
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
        if(app.player.onGround):
            app.player.jump()
            app.player.onGround = False
        else:
            pass
        
    # debug
    elif(event.key == 'r'):
        appStarted(app)
        
def keyReleased(app, event):
    if(event):
        app.player.setDeltas(0, 0)
        
def timerFired(app):
    app.player.checkCollisions(app.lines)
    app.player.movePlayer()
    
# View ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def redrawAll(app, canvas):
    # canvas.create_image(0, 0, image = ImageTk.PhotoImage(app.image1), anchor = 'nw')
    for i in range(len(app.lines)):
        app.lines[i].drawLine(app, canvas)
    app.player.drawPlayer(app, canvas)
    
    
runApp(width = 1200, height = 850)