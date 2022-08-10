# Images and level line coordinates copied from: https://github.com/Code-Bullet/Jump-King/tree/321506e725ef448654936837672d9fe8fba123bb 
# Image loading code from: https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
# Specific player acceleration values and movement speeds copied from link above and tweaked to fit the timing of CMU graphics
# Idea on how to implement collision priority: https://www.youtube.com/watch?v=DmQ4Dqxs0HI
# Diagonal line collision formula taken from: https://www.jeffreythompson.org/collision-detection/line-line.php 

from cmu_112_graphics import *
from Line import *
from Player import *
from Level import *
from LevelSetup import *

# Model ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def appStarted(app):    
    # window dimensions
    app.width = 1200
    app.height = 900
    
    # make the player
    app.player = Player()
    
    # keep track of all the lines
    app.levelLines = LevelSetup()
    
    # test first level stuff
    # ? Also you prolly have to edit each one of the lines in order to make sure y1 < y2
    app.level = 0
    
    # * time stuff test
    app.time = 0
    
    # * test image stuffs; work on putting it all in
    # image stuff
    app.bgrdImage = app.loadImage('lvlImages/1.png')
    app.avatar = app.loadImage('playerStuff/idle.png')
    app.squatAva = app.loadImage('playerStuff/squat.png')
        
    # set default walk speed for player
    app.timerDelay = 1
    app.walkSpeed = 4
    
# Controller ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def keyPressed(app, event):
    # the player has different modes that it can be in when on the ground
    
    # when it's not getting ready to jump and the level allows the player to move
    # while on the ground, the player should walk left or right
    if(app.player.onGround and not app.player.squatting and not app.levelLines.gameLevelList[app.level].cantMove):
        if(event.key == 'Left'):
            app.player.isMoving = True
            app.player.moveLeft = True
            app.player.setDeltas(-app.walkSpeed, 0)
        elif(event.key == 'Right'):
            app.player.isMoving = True
            app.player.moveRight = True
            app.player.setDeltas(app.walkSpeed, 0)
            
    # if it is getting ready to jump, horizontal movement should get disallowed
    elif(app.player.onGround and app.player.squatting):
        # booleans are used in the player jump function to determine 
        # which direction the player should jump
        
        # if left is pressed/held the player should jumpleft.
        if(event.key == 'Left'):
            app.player.jumpLeft = True
        
        # if right is pressed/held the player should jumpRight
        elif(event.key == 'Right'):
            app.player.jumpRight = True
            
        # if neither are held, player should jump straight up
    
    # if the space key is pressed squatting, a variable saying when the player
    # is getting ready to jump, is turned to True and the jump gets charged up
    # if it's less than the maximum jump speed
    if(event.key == 'Space'):
        if(app.player.onGround):
            app.player.setDeltas(0, 0)
            app.player.squatting = True
            if(app.player.vertJumpSpeed < app.player.maxVertJump):
                app.player.vertJumpSpeed += 1
    
    # debug, restarts the app to beginning state.
    if(event.key == 'r'):
        appStarted(app)
    
        
def keyReleased(app, event):
    # once the space key is released the player should jump
    if(event.key == 'Space' and app.player.onGround):
        app.player.jump()
        app.player.onGround = False
        app.player.vertJumpSpeed = app.player.minVertJump
        
    # if player is on the ground
    if(app.player.onGround):
        # if the right key is released, right movement should stop as well
        # jumpRight set to False
        if(event.key == 'Right'):
            # jumpRight set to False and deltas set to 0
            app.player.jumpRight = False
            app.player.setDeltas(0, 0)
            
            # if the level is an ice level this allows you to stop properly
            if(app.levelLines.gameLevelList[app.level].isIce):
                app.player.isMoving = False
                app.player.moveRight = False

                app.player.applyIce(app.levelLines.gameLevelList[app.level].lines)
            
            
                
        elif(event.key == 'Left'):
            # jumpLeft set to False and deltas set to 0
            app.player.jumpLeft = False
            app.player.setDeltas(0, 0)
            
            # if the level is an ice level this allows you to stop properly
            if(app.levelLines.gameLevelList[app.level].isIce):
                app.player.isMoving = False
                app.player.moveLeft = False

                app.player.applyIce(app.levelLines.gameLevelList[app.level].lines)
    
    # if 'n' is pressed and released it moves the level to the next one so long
    # as app.level is within the range of the gameLevelList. this also changes
    # the background to match the level
    if(event.key == 'n' and app.level < len(app.levelLines.gameLevelList) - 1):
        app.level += 1
        app.player.onGround = False # so the player doesn't float when level is changed
        if(app.level >= 0 and app.level < len(app.levelLines.gameLevelList)):
            app.bgrdImage = app.loadImage(f'lvlImages/{app.level + 1}.png')
    

def timerFired(app):        
    if(app.level >= 0 and app.level < len(app.levelLines.gameLevelList)):
        if(app.player.changeLevel()[0]):
            app.bgrdImage = app.loadImage(f'lvlImages/{app.level + 1 + app.player.changeLevel()[1]}.png')
             
            if(app.player.changeLevel()[1] == -1):
                app.level += app.player.changeLevel()[1]
                app.player.cy = 0 - app.player.height
            elif(app.player.changeLevel()[1] == +1):
                app.level += app.player.changeLevel()[1]
                app.player.cy = app.height
                
        if(app.levelLines.gameLevelList[app.level].isIce):
            app.player.applyIce(app.levelLines.gameLevelList[app.level].lines)
                    
        if(app.levelLines.gameLevelList[app.level].isWind):
            app.time += app.timerDelay
            if(app.time % 500 == 0):
                app.player.windMoveRight = not app.player.windMoveRight
                app.time = 0
            app.player.applyWind()
            
        app.player.checkCollisions(app.levelLines.gameLevelList[app.level].lines, app.levelLines.gameLevelList[app.level])
        app.player.movePlayer(app.levelLines.gameLevelList[app.level], app.levelLines.gameLevelList[app.level].lines)        

# View ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def redrawAll(app, canvas):
    # lines and stuff
    # for line in app.levelLines.gameLevelList[app.level].lines:
    #     line.drawLine(app, canvas)
    
    # * test image stuff
    canvas.create_image(0, 0, image = ImageTk.PhotoImage(app.bgrdImage), anchor = 'nw')
    
    app.player.drawPlayer(app, canvas)
    
    
runApp(width = 1200, height = 900)