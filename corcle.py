'''
corcle.py

'Imagine super hexagon X two cars'

Nicholas Ruggles
'''

import pygame, sys, math
from pygame.locals import *

FPS = 60
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
        
        # Draw Code
        
        pygame.display.set_caption('Corcle Panic %f' % FPSCLOCK.get_fps() )
        DISPLAYSURF.fill(BGCOLOR)
        
        blackPit.draw()
        whitePaddle.draw()
        
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
        
        self.pitPos = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
        
    def draw(self):
        
        pygame.draw.circle(DISPLAYSURF, self.color, self.pitPos, self.radius)

def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
