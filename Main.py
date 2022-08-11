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
    
    # level variable
    app.level = 0
    
    # time variable
    app.time = 0
    
    # image stuff
    app.bgrdImage = app.loadImage('lvlImages/1.png')
    app.avatar = app.loadImage('playerStuff/idle.png')
    app.invAva = app.avatar.transpose(Image.FLIP_LEFT_RIGHT)
    app.squatAva = app.loadImage('playerStuff/squat.png')
    
    # sprite animation stuff
    app.sprites = []
    app.sprite1 = app.loadImage('playerStuff/run1.png')
    app.sprite2 = app.loadImage('playerStuff/run2.png')
    app.sprite3 = app.loadImage('playerStuff/run3.png')
    
    app.sprites.append(app.sprite1)
    app.sprites.append(app.sprite2)
    app.sprites.append(app.sprite3)
    
    app.invSprites = []
    
    for inv in app.sprites:
        app.invSprites.append(inv.transpose(Image.FLIP_LEFT_RIGHT))
    
    app.currSprite = 0
    
    app.avaJump = app.loadImage('playerStuff/jump.png')
    app.avaFall = app.loadImage('playerStuff/fall.png')
        
    app.invJump = app.avaJump.transpose(Image.FLIP_LEFT_RIGHT)
    app.invFall = app.avaFall.transpose(Image.FLIP_LEFT_RIGHT)
    
    app.avaBump = app.loadImage('playerStuff/oof.png')
    app.invBump = app.avaBump.transpose(Image.FLIP_LEFT_RIGHT)
    
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
            app.player.faceRight = False
        elif(event.key == 'Right'):
            app.player.isMoving = True
            app.player.moveRight = True
            app.player.setDeltas(app.walkSpeed, 0)
            app.player.faceRight = True
            
    # if it is getting ready to jump, horizontal movement should get disallowed
    elif(app.player.onGround and app.player.squatting):
        # booleans are used in the player jump function to determine 
        # which direction the player should jump
        
        # if left is pressed/held the player should jumpleft.
        if(event.key == 'Left'):
            app.player.jumpLeft = True
            app.player.faceRight = False
        
        # if right is pressed/held the player should jumpRight
        elif(event.key == 'Right'):
            app.player.jumpRight = True
            app.player.faceRight = True
            
        # if neither are held, player should jump straight up
    
    # if the space key is pressed squatting, a variable saying when the player
    # is getting ready to jump, is turned to True and the jump gets charged up
    # if it's less than the maximum jump speed
    if(event.key == 'Space'):
        if(app.player.onGround):
            app.player.setDeltas(0, 0)
            app.player.isMoving = False
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
            app.player.isMoving = False
            app.player.jumpRight = False
            app.player.setDeltas(0, 0)
            
            # if the level is an ice level this allows you to stop properly
            if(app.levelLines.gameLevelList[app.level].isIce):
                app.player.isMoving = False
                app.player.moveRight = False

                app.player.applyIce(app.levelLines.gameLevelList[app.level].lines)
            
        # if the left key is released, left movement should stop
        elif(event.key == 'Left'):
            # jumpLeft set to False and deltas set to 0
            app.player.isMoving = False
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
    app.time += app.timerDelay
    
    if(app.player.isMoving and app.time % 6 == 0):
        app.currSprite = (1 + app.currSprite) % len(app.sprites)
    
    # if the level should change
    if(app.player.changeLevel()[0]):
        # update the background image
        app.bgrdImage = app.loadImage(f'lvlImages/{app.level + 1 + app.player.changeLevel()[1]}.png')
        
        # check if we're going up a level or down one level and place the player correctly
        if(app.player.changeLevel()[1] == -1):
            app.level += app.player.changeLevel()[1]
            app.player.cy = 0 - app.player.height
        elif(app.player.changeLevel()[1] == +1):
            app.level += app.player.changeLevel()[1]
            app.player.cy = app.height
    
    # if the level is an ice level lines should react like ice
    if(app.levelLines.gameLevelList[app.level].isIce):
        app.player.applyIce(app.levelLines.gameLevelList[app.level].lines)
    
    # if the level has wind, activate the wind
    if(app.levelLines.gameLevelList[app.level].isWind):
        # if app.time reaches 500 or something divisible by 500 then the wind 
        # should switch directions and reset app.time to 0
        if(app.time % 500 == 0):
            app.player.windMoveRight = not app.player.windMoveRight
            app.time = 0
            
        # apply wind physics to the player
        app.player.applyWind()
    
    # check collisions and move the player based on the current level
    app.player.checkCollisions(app.levelLines.gameLevelList[app.level].lines, app.levelLines.gameLevelList[app.level])
    app.player.movePlayer(app.levelLines.gameLevelList[app.level], app.levelLines.gameLevelList[app.level].lines)

# View ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def redrawAll(app, canvas):
    # lines and stuff
    for line in app.levelLines.gameLevelList[app.level].lines:
        line.drawLine(app, canvas)
    
    # background
    canvas.create_image(0, 0, image = ImageTk.PhotoImage(app.bgrdImage), anchor = 'nw')
    
    app.player.drawPlayer(app, canvas)
    
    
runApp(width = 1200, height = 900)