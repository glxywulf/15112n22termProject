from cmu_112_graphics import *
from Line import *
from Player import *
from Level import *
from LevelSetup import *

# Model ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def appStarted(app):    
    # window dimensions
    app.width = 1200
    app.height = 850
    
    # make the player
    app.player = Player()
    
    # keep track of all the lines
    app.levelLines = LevelSetup()
    
    # test first level stuff
    # ? Also you prolly have to edit each one of the lines in order to make sure y1 < y2
    app.level = 0
    
    # * test diagonal lines
    # app.levelLines.gameLevelList[app.level - 1].append(Line(320,460,520,660))
    # app.levelLines.gameLevelList[app.level - 1].append(Line(400,625,600,425))
    
    # * test image stuffs
    app.bgrdImage = app.loadImage('lvlImages/1.png')
    app.avatar = app.loadImage('playerStuff/idle.png')
        
    # set default walk speed for player
    app.timerDelay = 3
    app.walkSpeed = 4
    
# Controller ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def keyPressed(app, event):
    if(app.player.onGround and not app.player.squatting and not app.levelLines.gameLevelList[app.level].cantMove):
        if(event.key == 'Left'):
            app.player.isMoving = True
            app.player.moveLeft = True
            app.player.setDeltas(-app.walkSpeed, 0)
        elif(event.key == 'Right'):
            app.player.isMoving = True
            app.player.moveRight = True
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
                
    if(app.levelLines.gameLevelList[app.level].isIce):
        app.player.applyIce(app.levelLines.gameLevelList[app.level].lines)
        
    # debug
    if(event.key == 'r'):
        appStarted(app)
    if(event.key == 'n' and app.level < len(app.levelLines.gameLevelList) - 1):
        app.level += 1
        app.player.onGround = False
        
def keyReleased(app, event):
    if(event.key == 'Space' and app.player.onGround):
        app.player.jump()
        app.player.onGround = False
        app.player.vertJumpSpeed = app.player.minVertJump
    if(app.player.onGround):
        if(event.key == 'Right'):
            app.player.jumpRight = False
            app.player.setDeltas(0, 0)
            
            if(app.levelLines.gameLevelList[app.level].isIce):
                app.player.isMoving = False
                app.player.moveRight = False

                app.player.applyIce(app.levelLines.gameLevelList[app.level].lines)
                
        elif(event.key == 'Left'):
            app.player.jumpLeft = False
            app.player.setDeltas(0, 0)
            
            if(app.levelLines.gameLevelList[app.level].isIce):
                app.player.isMoving = False
                app.player.moveLeft = False

                app.player.applyIce(app.levelLines.gameLevelList[app.level].lines)
    

def timerFired(app):
    # * test image stuff
    app.bgrdImage = app.loadImage(f'lvlImages/{app.level + 1}.png')
    
    if(app.level >= 0 and app.level < len(app.levelLines.gameLevelList)):
        if(app.player.changeLevel()[0]):
            if(app.player.changeLevel()[1] == -1):
                app.level += app.player.changeLevel()[1]
                app.player.cy = 0 - app.player.height
            elif(app.player.changeLevel()[1] == +1):
                app.level += app.player.changeLevel()[1]
                app.player.cy = 900
                
        if(app.levelLines.gameLevelList[app.level].isIce):
            app.player.applyIce(app.levelLines.gameLevelList[app.level].lines)
            
        app.player.checkCollisions(app.levelLines.gameLevelList[app.level].lines, app.levelLines.gameLevelList[app.level])
        
        app.player.movePlayer(app.levelLines.gameLevelList[app.level], app.levelLines.gameLevelList[app.level].lines)
    
# View ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def redrawAll(app, canvas):
    # * test image stuff
    # canvas.create_image(0, 0, image = ImageTk.PhotoImage(app.bgrdImage), anchor = 'nw')
    
    if(app.level >= 0 and app.level < len(app.levelLines.gameLevelList)):
        for line in app.levelLines.gameLevelList[app.level].lines:
            line.drawLine(app, canvas)
    app.player.drawPlayer(app, canvas)
    
    
runApp(width = 1200, height = 900)