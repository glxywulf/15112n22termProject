from cmu_112_graphics import *
from Line import *

testLine = Line(0, 0, 800, 800)

def redrawAll(app, canvas):
    testLine.drawLine(app, canvas)
    
    
runApp(width = 800, height = 800)