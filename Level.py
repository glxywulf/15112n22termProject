
class Level:
    def __init__(self, lines, num):
        self.lines = lines
        self.isIce = False
        self.isWind = False
        self.cantMove = False
        self.levelNum = num
        
    def getIce(self):
        return self.isIce
    
    def getWind(self):
        return self.isWind
    
    def getMove(self):
        return self.cantMove
        