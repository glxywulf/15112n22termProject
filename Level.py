# Images and level line coordinates copied from: https://github.com/Code-Bullet/Jump-King/tree/321506e725ef448654936837672d9fe8fba123bb 
# Image loading code from: https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
# Specific player acceleration values and movement speeds copied from link above and tweaked to fit the timing of CMU graphics
# Idea on how to implement collision priority: https://www.youtube.com/watch?v=DmQ4Dqxs0HI
# Diagonal line collision formula taken from: https://www.jeffreythompson.org/collision-detection/line-line.php 

class Level:
    def __init__(self, lines, num):
        self.lines = lines
        self.isIce = False
        self.isWind = False
        self.cantMove = False
        self.levelNum = num

        