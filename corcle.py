'''
corcle.py

'Imagine super hexagon X two cars'

Nicholas Ruggles
'''

from __future__ import division
import pygame, sys, math
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 800
WINDOWHEIGHT = 600

#                  R    G    B
DARKTURQUOISE = (  3,  54,  73)
BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)

BGCOLOR = DARKTURQUOISE

# Paddle attributes
PADDIAMETER = 200
PADLENGTH = math.pi/4
PADSPEED = math.pi/20
PADWIDTH = 50

# Pit attributes
PITRADIUS = 50

def main():

    global DISPLAYSURF

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    
    arcPos = 0
    
    whitePaddle = paddle(WHITE, PADDIAMETER, PADLENGTH, PADWIDTH, arcPos)
    blackPit = pit(BLACK, PITRADIUS)
    
    dotSpeed = 5
    whiteDot = spawnDot(WHITE, math.pi , dotSpeed)
    
    while True:
    
        # Event Code & Game Logic
    
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()   
        
        keys = pygame.key.get_pressed()
        if keys[K_a]:
            whitePaddle.move(PADSPEED)
        if keys[K_s]:
            whitePaddle.move(-PADSPEED)
        
        whiteDot.move()
        
        # Draw Code
        
        pygame.display.set_caption('Corcle Panic %f' % whitePaddle.collide(whiteDot.getPos()) )
        DISPLAYSURF.fill(BGCOLOR)
        
        blackPit.draw()
        whitePaddle.draw()
        whiteDot.draw()
        
        # Update Screen & wait for next frame
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

class paddle(object):
    
    def __init__(self, color, diameter, arcLength, arcWidth, arcPos):
    
        self.color = color
        self.diameter = diameter
        self.arcLength = arcLength
        self.arcWidth = arcWidth
        self.arcPos = arcPos
        
        
        self.circleRect = pygame.Rect((WINDOWWIDTH - diameter)/2, (WINDOWHEIGHT - diameter)/2, diameter, diameter)
    
    def draw(self):
        
        pygame.draw.arc(DISPLAYSURF, self.color, self.circleRect, self.arcPos, self.arcPos + self.arcLength, self.arcWidth)
        
    def move(self, arcDelta):
        
        self.arcPos = self.arcPos + arcDelta
        
        if self.arcPos > 2*math.pi:
            self.arcPos -= 2*math.pi
            
        if self.arcPos < 0:
            self.arcPos += 2*math.pi
        
    def collide(self, pos):
        
        distance = ( (pos[0] - self.circleRect.center[0])**2 + (pos[1] - self.circleRect.center[1])**2 )**0.5
        
        if pos[1] < self.circleRect.center[1]:
            theta = math.atan2( -(pos[1] - self.circleRect.center[1]), (pos[0] - self.circleRect.center[0]) )
        else:
            theta = math.pi - math.atan2( -(pos[1] - self.circleRect.center[1]), -(pos[0] - self.circleRect.center[0]) )
        
        return (distance < self.diameter/2) and (distance > self.diameter/2 - self.arcWidth) \
            and (theta > self.arcPos) and (theta < self.arcPos + self.arcLength)
    
class pit(object):
    
    def __init__(self, color, radius):
        
        self.color = color
        self.radius = radius
        
        self.pitPos = (WINDOWWIDTH//2, WINDOWHEIGHT//2)
        
    def draw(self):
        
        pygame.draw.circle(DISPLAYSURF, self.color, self.pitPos, self.radius)

    def collide(self, pos):
        # Returns True if x, y in pit
        
        distance = ((pos[0] - self.pitPos[0])**2 + (pos[1] - self.pitPos[1])**2)**0.5
        
        return distance < self.radius

class dot(object):
    
    def __init__(self, color, xPos, yPos, direction, speed):
        
        self.color = color
        self.direction = direction
        self.xPos = xPos - 5
        self.yPos = yPos - 5
        self.speed = speed
        
        self.dotRect = (self.xPos, self.yPos, 10, 10)
        
    def draw(self):
        
        pygame.draw.rect(DISPLAYSURF, self.color, self.dotRect)
        
    def move(self):
    
        self.xPos = self.xPos + self.speed * math.cos(self.direction)
        self.yPos = self.yPos + self.speed * math.sin(self.direction)
        
        self.dotRect = (self.xPos, self.yPos, 10, 10)
        
    def getPos(self):
        
        return (self.xPos, self.yPos)
        
def spawnDot(color, angle, speed):
    #returns dot object positioned at edge of screen, facing center.
    
    x = WINDOWWIDTH//2 + WINDOWHEIGHT*math.cos(angle)
    y = WINDOWHEIGHT//2 + WINDOWHEIGHT*math.sin(angle)
    newDot = dot(color, x, y, angle + math.pi, speed)
    
    return newDot

def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
