'''
corcle.py

'Imagine super hexagon X two cars'

Nicholas Ruggles
'''

import pygame, sys
from pygame.locals import *

def main():

    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((400, 300))
    pygame.display.set_caption('Corcle Panic')
    
    while True:
       for event in pygame.event.get():
           if event.type == QUIT:
              pygame.quit()
              sys.exit()
            
    pygame.display.update()
    
if __name__ == '__main__':
    main()
