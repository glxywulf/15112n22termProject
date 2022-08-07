from cmu_112_graphics import *
from Line import *
from Player import *
from Level import *

# Model ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def appStarted(app):    
    # window dimensions
    app.width = 1200
    app.height = 850
    
    # make the player
    app.player = Player()
    
    # keep track of all the lines
    app.levelLines = Level()
    
    # test first level stuff
    # ? Also you prolly have to edit each one of the lines in order to make sure y1 < y2
    app.level = 0
    
    # * test diagonal lines
    # app.levelLines.gameLevelList[app.level - 1].append(Line(320,460,520,660))
    # app.levelLines.gameLevelList[app.level - 1].append(Line(400,625,600,425))
    
    # test image stuffs
    app.image1 = app.loadImage('lvlImages/1.png')
    app.avatar = app.loadImage('playerStuff/idle.png')
        
    # set default walk speed for player
    app.timerDelay = 10
    app.walkSpeed = 4
    
# Controller ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def keyPressed(app, event):
    if(app.player.onGround and not app.player.squatting):
        if(event.key == 'Left'):
            app.player.setDeltas(-app.walkSpeed, 0)
        elif(event.key == 'Right'):
            app.player.setDeltas(app.walkSpeed, 0)
    elif(app.player.onGround and app.player.squatting):
        if(event.key == 'Left'):
            app.player.jumpLeft = True
        elif(event.key == 'Right'):
            app.player.jumpRight = True
    if(event.key == 'Space'):
        if(app.player.onGround):
            app.player.setDeltas(0, 0)
            app.player.squatting = True
            if(app.player.vertJumpSpeed < app.player.maxVertJump):
                app.player.vertJumpSpeed += 1
        else:
            return 42
        
    # debug
    elif(event.key == 'r'):
        appStarted(app)
        
def keyReleased(app, event):
    if(event.key == 'Space' and app.player.onGround):
        app.player.jump()
        app.player.onGround = False
        app.player.vertJumpSpeed = app.player.minVertJump
    if(app.player.onGround):
        if(event.key == 'Right'):
            app.player.jumpRight = False
            app.player.setDeltas(0, 0)
        elif(event.key == 'Left'):
            app.player.jumpLeft = False
            app.player.setDeltas(0, 0)
    
def timerFired(app):
    if(app.player.changeLevel()[0]):
        app.level += app.player.changeLevel()[1]
        
        if(app.player.changeLevel()[1] == -1 and app.level > 0):
            app.player.cy = 0 - app.player.height
        elif(app.player.changeLevel()[1] == +1 and app.level < len(app.levelLines.gameLevelList) - 1):
            app.player.cy = 850
            
    app.player.checkCollisions(app.levelLines.gameLevelList[app.level])
    app.player.movePlayer()
    
# View ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def redrawAll(app, canvas):
    # canvas.create_image(0, 0, image = ImageTk.PhotoImage(app.image1), anchor = 'nw')
    for line in app.levelLines.gameLevelList[app.level]:
        line.drawLine(app, canvas)
    app.player.drawPlayer(app, canvas)
    
    
runApp(width = 1200, height = 850)