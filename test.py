from cmu_112_graphics import *
from Line import *


def appStarted(app):
    app.height = 820
    app.width = 1180

def redrawAll(app, canvas):
    testLine = Line(0, app.height - 100, app.width, app.height - 100)
    
    testLine.drawLine(app, canvas)
    

runApp(width = 1180, height = 820)