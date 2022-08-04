# x1,x2,x3,x4,y1,y2,y3,y4 = 980,980,640,640,0,820,620,685

# print(((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)))

# def checkCollision(self, player):
#         # line coords
#         x1 = self.x1
#         y1 = self.y1
#         x2 = self.x2
#         y2 = self.y2
        
#         # player line coords
#         # player's left
#         lx1, ly1, lx2, ly2 = (player.cx,
#                               player.cy,
#                               player.cx,
#                               player.cy + (player.height // 2))
        
#         # player's right
#         rx1, ry1, rx2, ry2 = (player.cx + player.width,
#                               player.cy,
#                               player.cx + player.width,
#                               player.cy + player.height)
        
#         # player's top
#         tx1, ty1, tx2, ty2 = (player.cx,
#                               player.cy,
#                               player.cx + player.width,
#                               player.cy)
        
#         # player's bottom
#         bx1, by1, bx2, by2 = (player.cx,
#                               player.cy + player.height,
#                               player.cx + player.width,
#                               player.cy + player.height)
        
#         # check if player has collided with any lines
#         # left
#         hitLeft = self.checkLineLine(x1, y1, x2, y2, lx1, ly1, lx2, ly2)
        
#         # right
#         hitRight = self.checkLineLine(x1, y1, x2, y2, rx1, ry1, rx2, ry2)
        
#         # top
#         hitTop = self.checkLineLine(x1, y1, x2, y2, tx1, ty1, tx2, ty2)
        
#         # bottom
#         hitBottom = self.checkLineLine(x1, y1, x2, y2, bx1, by1, bx2, by2)
        
#         if(hitLeft):
#             pass
#         elif(hitRight):
#             pass
#         elif(hitTop):
#             pass
#         elif(hitBottom):
#             player.onGround = True
#             player.cy = self.y1 - player.height
            
            
            
            
            
            
            
            
#             # check if line is horizontal
#         if(line.isHorizontal):
#             # see if the player is within the x of any line
#             interX = ((line.x1 < self.cx and self.cx < line.x2) or
#                       (line.x1 < self.cx + self.width and 
#                        self.cx + self.width < line.x2) or 
#                       (self.cx < line.x1 and  line.x1 < self.cx + self.width) or
#                       (self.cx < line.x2 and line.x2 <  self.cx + self.width))
            
#             # see if the player is within the y of any line
#             interY = self.cy < line.y1 and line.y1 < self.cy + self.height
            
#             # if both are true, we're colliding with something
#             return interX and interY
        
#         # check if line is vertical
#         elif(line.isVertical):
#             # see if the player is within the y of any line
#             interY = ((line.y1 < self.cy and self.cy < line.y2) or 
#                       (line.y1 < self.cy + self.height and 
#                        self.cy + self.height < line.y2) or 
#                       (self.cy < line.y1 and line.y1 < self.cy + self.height) or
#                       (self.cy < line.y2 and line.y2 < self.cy + self.height))
#             # see if the player is within the x of any line
#             interX = self.cx < line.x1 and line.x1 < self.cx + self.width
            
#             # if both are true, we're colliding with something
#             return interY and interX
        
#         # if it's neither, then it's diagonal
#         else:
#             pass