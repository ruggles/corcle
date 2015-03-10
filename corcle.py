'''
corcle.py

'Imagine super hexagon X two cars'

Nicholas Ruggles
'''

from __future__ import division
import pygame, sys, math, random, os, time, copy
from pygame.locals import *

FPS = 60
WINDOWWIDTH = 1000
WINDOWHEIGHT = 700

#                  R    G    B
DARKTURQUOISE = (  3,  54,  73)
BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)
BLUE =          (  0,   0, 255)
DARKBLUE =      (  0,   0, 127)
RED =           (255,   0,   0)
PURPLE =        (255,   0, 255)
GREEN =         (  0, 255,   0)
YELLOW =        (255, 255,   0)
ORANGE =        (255, 127,   0)

BGCOLOR = BLACK
PITCOLOR = BLACK
LINECOLOR = DARKBLUE
COLOR1 = RED
COLOR2 = GREEN
FONTCOLOR = WHITE

# Paddle attributes
PADDIAMETER = 150
PADLENGTH = math.pi/3
PADSPEED = math.pi/24
PADWIDTH = 5

# Pit attributes
PITRADIUS = 25

# Dot attributes
DOTSPEED = 3.5
BASEFREQ = 180

NUMLINES = 20
FONTSIZE = 25
WAITTIME = 500

SPAWNINTERVAL = 900 # How often we change the spawn regime, in frames
BLANKINTERVAL = 120 # Free time given between spawn regimes

def main():

    global DISPLAYSURF, FPSCLOCK, GAMEFONT
    
    # Font junk
    dataDir = 'data'
    fontName = 'FreeSansBold.ttf'
    myFontFile = resource_path(os.path.join(dataDir, fontName))
    
    # print myFontFile
    
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    GAMEFONT = pygame.font.Font( myFontFile, FONTSIZE)
    
    pygame.display.set_caption('Corcle')

    startScreen()    
    
    while True:
    
        timeAlive = runGame()
        endScreen(timeAlive)

def startScreen():

    DISPLAYSURF.fill(BLACK)
    
    textSurf = GAMEFONT.render("Use A-S and K-L to move the paddles", False, FONTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = (WINDOWWIDTH//2.2, WINDOWHEIGHT//4)
    DISPLAYSURF.blit(textSurf, textRect)

    pressSurf = GAMEFONT.render("Press any key to continue", False, FONTCOLOR)
    pressRect = textSurf.get_rect()
    pressRect.center = (WINDOWWIDTH//2, WINDOWHEIGHT//2)
    DISPLAYSURF.blit(pressSurf, pressRect)
    
    pygame.display.update()
    pygame.time.wait(WAITTIME)
    pygame.event.get()

    while True:    
        checkForQuit()
        if checkForKeyPress():
            return

def runGame():
    global SPAWNCOLOR

    firstPaddle = paddle(COLOR1, PADDIAMETER, PADLENGTH, PADWIDTH, math.pi)
    secondPaddle = paddle(COLOR2, PADDIAMETER + PADWIDTH*2, PADLENGTH, PADWIDTH, 0)
    centerPit = pit(PITCOLOR, PITRADIUS)
    
    dotList = []
    
    frameCount = 0
    timeAlive = frameCount / 60
    lastSpawnTime = time.time()
    
    regimeList = [spawnSimultaneous, spawnRandom, spawnSame, spawnAlternating]
    dotSpawn = random.choice(regimeList)
    degrees = 0
    rotationSpeed = 0
   
    while True:
    
        # Event Code
    
        checkForQuit()
        pygame.event.get() # Clear event Queue
        
        keys = pygame.key.get_pressed()
        if keys[K_a]:
            firstPaddle.move(PADSPEED)
        if keys[K_s]:
            firstPaddle.move(-PADSPEED)
            
        if keys[K_k]:
            secondPaddle.move(PADSPEED)
        if keys[K_l]:
            secondPaddle.move(-PADSPEED)
        
        # Dot spawning functions either return None, or a list of dot objects
        if frameCount%SPAWNINTERVAL == 0:
            SPAWNCOLOR = random.choice((COLOR1, COLOR2))
            spawnRegime = copy.copy(regimeList)
            spawnRegime.remove(dotSpawn)
            dotSpawn = random.choice(spawnRegime)
            rotationSpeed = (random.uniform(0.25, 0.5)) * ((frameCount + 1800) / 1800) * random.choice((-1, 1))
        
        if (frameCount%SPAWNINTERVAL < SPAWNINTERVAL - BLANKINTERVAL):
            newDotList = dotSpawn(frameCount, time.time() - lastSpawnTime)
        
        if newDotList != None:
            lastSpawnTime = time.time()
            for dot in newDotList:
                dotList.append(dot)

        # Collision Code
        i = 0
        for dot in dotList:
            if firstPaddle.collide(dot.getPos()):
                if (firstPaddle.getColor() == dot.getColor()):
                    dotList.pop(i)
                else:
                    return timeAlive
            elif secondPaddle.collide(dot.getPos()):
                if (secondPaddle.getColor() == dot.getColor()):
                    dotList.pop(i)
                else:
                    return timeAlive

            elif centerPit.collide(dot.getPos()):
                return timeAlive
            else:
                dot.move()
            i += 1
        
        # Draw Code   
        
        DISPLAYSURF.fill(BGCOLOR)
        
        degrees +=  (math.sin((frameCount%1000)/1000) - 0.5) * rotationSpeed
        
        rotAngle = degrees*math.pi/180
        
        drawRadialLines(LINECOLOR, NUMLINES, rotAngle)
        
        centerPit.draw()

        firstPaddle.draw(rotAngle)
        secondPaddle.draw(rotAngle)
        
        # Framerate, for debug purposes
        #pygame.display.set_caption('%d' % FPSCLOCK.get_fps() )

        for dot in dotList:
            dot.draw(rotAngle)

        # Update Screen & wait for next frame
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        frameCount += 1
        timeAlive = frameCount / 60
    
def endScreen(timeAlive):
    
    DISPLAYSURF.fill(BLACK)
    scoreSurf = GAMEFONT.render("You stayed alive for %.2f seconds" % timeAlive, False, FONTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 4)
    DISPLAYSURF.blit(scoreSurf, scoreRect)
    
    playSurf = GAMEFONT.render("Press any key to play again", False, FONTCOLOR)
    playRect = playSurf.get_rect()
    playRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)
    DISPLAYSURF.blit(playSurf, playRect)
    
    pygame.display.update()
    pygame.time.wait(WAITTIME)
    pygame.event.get()
    
    while True:
        checkForQuit()
        if checkForKeyPress():
            return
        

class paddle(object):
    
    def __init__(self, color, diameter, arcLength, arcWidth, arcPos):
    
        self.color = color
        self.diameter = diameter
        self.arcLength = arcLength
        self.arcWidth = arcWidth
        self.arcPos = arcPos
        
        if self.arcPos > 2*math.pi:
            self.arcPos -= 2*math.pi
        if self.arcPos < 0:
            self.arcPos += 2*math.pi
        
        self.circleRect = pygame.Rect((WINDOWWIDTH - diameter)/2, (WINDOWHEIGHT - diameter)/2, diameter, diameter)
    
    def draw(self, rotAngle=0):        
        
        pygame.draw.arc(DISPLAYSURF, self.color, self.circleRect, self.arcPos - rotAngle, self.arcPos + self.arcLength - rotAngle, self.arcWidth)
        
    def move(self, arcDelta):
        
        self.arcPos = self.arcPos + arcDelta
        
        if self.arcPos > 2*math.pi:
            self.arcPos -= 2*math.pi
            
        if self.arcPos < 0:
            self.arcPos += 2*math.pi
        
    def collide(self, pos):
        
        distance = ( (pos[0] - self.circleRect.center[0])**2 + (pos[1] - self.circleRect.center[1])**2 )**0.5
        
        theta = getAngle(pos)
        
        if (theta < self.arcLength) and (self.arcPos + self.arcLength > 2*math.pi) :
            theta += 2*math.pi
        
        return (distance < self.diameter/2) and (distance > self.diameter/2 - self.arcWidth) \
            and (theta > self.arcPos) and (theta < self.arcPos + self.arcLength)
            
    def getColor(self):
        
        return self.color
    
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
        
    def draw(self, rotAngle=0):
        
        self.updateDrawRect(rotAngle)
        pygame.draw.rect(DISPLAYSURF, self.color, self.drawRect)
        
    def move(self):
    
        self.xPos = self.xPos - self.speed * math.cos(self.direction)
        self.yPos = self.yPos - self.speed * math.sin(self.direction)
        
        self.dotRect = (self.xPos, self.yPos, 10, 10)
        
    def updateDrawRect(self, rotAngle):
        
        angle = getAngle((self.xPos, self.yPos))
        centerX = WINDOWWIDTH // 2
        centerY = WINDOWHEIGHT // 2
        radius = ( (self.xPos + 5 - centerX )**2 + (self.yPos + 5 - centerY )**2 )**0.5
        
        drawX = math.cos(angle - rotAngle) * radius + centerX
        drawY = - math.sin(angle - rotAngle) * radius + centerY
        
        self.drawRect = pygame.Rect(drawX - 5, drawY - 5, 10, 10)
        
    def getPos(self):
        
        return (self.xPos + 5, self.yPos + 5)
        
    def getColor(self):
        
        return self.color
        
def spawnDot(color, angle, speed):
    #returns dot object positioned at edge of screen, facing center.
    
    x = WINDOWWIDTH//2 + WINDOWHEIGHT*math.cos(angle)
    y = WINDOWHEIGHT//2 - WINDOWHEIGHT*math.sin(angle)
    newDot = dot(color, x, y, -angle, speed)
    
    return newDot
    
def getAngle(pos):
    '''
    Gets angle from center of screen
    '''
    
    # Get coords relative to center
    x = pos[0] - WINDOWWIDTH//2
    y = pos[1] - WINDOWHEIGHT//2
    
    if y < 0:
        angle = math.atan2(-y, x)
    else:
        angle = math.pi - math.atan2(-y, -x)
    
    return angle    

def terminate():
    pygame.quit()
    sys.exit()
    
def checkForQuit():
    
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()   
            
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                terminate()
                    
        pygame.event.post(event)

def checkForKeyPress():
    
    for event in pygame.event.get():
        if event.type == KEYUP:
            return True
            
    return False
    
def spawnSimultaneous(frameCount, timeSinceSpawn):

    newDotList = []
    
    spawnThreshold = (BASEFREQ - (frameCount**0.5) )/FPS

    if timeSinceSpawn > spawnThreshold:
        firstSpawn = random.uniform(0, math.pi*2)
        newDotList.append(spawnDot(COLOR1, firstSpawn , DOTSPEED))
        newDotList.append(spawnDot(COLOR2, firstSpawn + random.uniform(PADLENGTH, math.pi*2 - PADLENGTH), DOTSPEED))
        return newDotList
    else:
        return None
        
def spawnRandom(frameCount, timeSinceSpawn):

    newDotList = []
    
    spawnThreshold = (BASEFREQ/1.6 - (frameCount**0.5) )/FPS
    
    if timeSinceSpawn > spawnThreshold:
        newDotList.append(spawnDot(random.choice((COLOR1, COLOR2)), random.uniform(0, math.pi*2), DOTSPEED))
        return newDotList
    
    return None
    
def spawnSame(frameCount, timeSinceSpawn):

    newDotList = []
    
    spawnThreshold = (BASEFREQ/2 - (frameCount**0.5))/FPS

    if timeSinceSpawn > spawnThreshold:
        newDotList.append(spawnDot(SPAWNCOLOR, random.uniform(0, math.pi*2), DOTSPEED))
        return newDotList
        
    return None

def spawnAlternating(frameCount, timeSinceSpawn):

    global SPAWNCOLOR
    newDotList = []
    
    spawnThreshold = ( BASEFREQ/1.7 - (frameCount**0.5)) /FPS
    
    if timeSinceSpawn > spawnThreshold:
    
        if SPAWNCOLOR == COLOR1:
            SPAWNCOLOR = COLOR2
        else:
            SPAWNCOLOR = COLOR1
    
        newDotList.append(spawnDot(SPAWNCOLOR, random.uniform(0, math.pi*2), DOTSPEED))
        
        return newDotList
    
    return None
        
def drawRadialLines(color, numLines, rotAngle=0):
    # Draws numLines number of lines radiating from center of screen
    
    assert numLines > 0
    
    lineDiff = 2 * math.pi / numLines
    center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)
    
    for i in range(numLines) :
        angle = lineDiff * i + rotAngle
        endX = center[0] + WINDOWHEIGHT*math.cos(angle)
        endY = center[1] + WINDOWHEIGHT*math.sin(angle)
        
        pygame.draw.line(DISPLAYSURF, color, center, (endX, endY))

def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

if __name__ == '__main__':
    main()
