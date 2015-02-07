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

# Pit attributes
PITRADIUS = 50

def main():

    global DISPLAYSURF

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    
    arcPos = 2
    
    whitePaddle = paddle(WHITE, PADDIAMETER, PADLENGTH, arcPos)
    blackPit = pit(BLACK, PITRADIUS)
    whiteDot = dot(WHITE, 10, 300, 0 , 5)
    
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
        
        pygame.display.set_caption('Corcle Panic %f' % blackPit.collide(whiteDot.getPos()) )
        DISPLAYSURF.fill(BGCOLOR)
        
        blackPit.draw()
        whitePaddle.draw()
        whiteDot.draw()
        
        # Update Screen & wait for next frame
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

class paddle(object):
    
    def __init__(self, color, diameter, arcLength, arcPos):
    
        self.color = color
        self.diameter = diameter
        self.arcLength = arcLength
        self.arcPos = arcPos
        
        self.circleRect = ((WINDOWWIDTH - diameter)/2, (WINDOWHEIGHT - diameter)/2, diameter, diameter)
    
    def draw(self):
        
        pygame.draw.arc(DISPLAYSURF, self.color, self.circleRect, self.arcPos, self.arcPos + self.arcLength, 5)
        
    def move(self, arcDelta):
        
        self.arcPos = self.arcPos + arcDelta
    
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
        self.xPos = xPos
        self.yPos = yPos
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
        

def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
