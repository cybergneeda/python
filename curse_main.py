import pygame
import sys
from curse_logic import *
WIDTH = 1200
HEIGHT = 800
FPS = 60
WHITE = (255,255,255)
BLACK = (0,0,0)
SCALE = 40

def main():                 
    pygame.init()
    screen=pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('kill them all')
    clock=pygame.time.Clock()
    dm=Diffusion_model(30,8,0.03)
    while True:
        clock.tick(FPS)
        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()   
            for i in range(dm.height):
                for j in range(dm.width): 
                    if dm.field[i][j]=='x':
                        pygame.draw.rect(screen, WHITE,(j*SCALE,i*SCALE,SCALE,SCALE))
                    elif dm.field[i][j]==0:
                        pygame.draw.rect(screen, BLACK,(j*SCALE,i*SCALE,SCALE,SCALE))
                    else:
                        pygame.draw.rect(screen,(0,int(dm.field[i][j])+64,0),(j*SCALE,i*SCALE,SCALE,SCALE))
            pygame.display.flip()
            pygame.display.update()    
            pygame.time.delay(1000)
            dm.update()        
main()