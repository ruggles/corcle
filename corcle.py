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

# Arc attributes
DIAMETER = 200
ARCLENGTH = math.pi/4

# Pit attributes
PITRADIUS = 50

def main():

    global DISPLAYSURF, WINDOWWIDTH, WINDOWHEIGHT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    
    arcPos = 2
    
    while True:
    
        pygame.display.set_caption('Corcle Panic %f' % FPSCLOCK.get_fps() )
        DISPLAYSURF.fill(BGCOLOR)
        
        # Draw game objects
        drawPaddle(arcPos, DIAMETER, ARCLENGTH, WHITE)
        drawPit(BLACK, PITRADIUS)
    
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()   
        
        keys = pygame.key.get_pressed()
        if keys[K_a]:
            arcPos += math.pi/30
        if keys[K_s]:
            arcPos -= math.pi/30
                    
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    
def terminate():
    pygame.quit()
    sys.exit()
    
def drawPaddle(arcPos, diameter, arcLength, color):
    circleRect = ((WINDOWWIDTH - diameter)/2, (WINDOWHEIGHT - diameter)/2, diameter, diameter)
    pygame.draw.arc(DISPLAYSURF, color, circleRect, arcPos, arcPos + arcLength, 5)
    
def drawPit(color, radius):
    pitPos = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
    pygame.draw.circle(DISPLAYSURF, color, pitPos, radius)

if __name__ == '__main__':
    main()
