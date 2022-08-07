
class Level:
    def __init__(self, lines, num):
        self.lines = lines
        self.isIce = False
        self.isWind = False
        self.cantMove = False
        self.levelNum = num
        