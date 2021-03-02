import pygame
import math
import random
import BoidsEngine

WHITE = (255,255,255)
BLACK = (  0,  0,  0)
RED   = (255,  0,  0)
GREEN = (  0,255,  0)
BLUE  = (  0,  0,255)
GREY  = ( 30, 30, 30)


WIDTH = 800
HEIGHT = 800


''' EXPERIMENTING WITH '''
ALLIGN = 100
COHESION = 100
SEPARATION = 100
MAXSPEED = 10
SEPFORCE = 25

def makeFlock(length):
    flock = []
    for i in range(length):
        flock.append(BoidsEngine.boid(win, ALLIGN, COHESION, SEPARATION, SEPFORCE, MAXSPEED, WHITE, wrap = True))
    #one red to help debugging, and visualisation
    flock.append(BoidsEngine.boid(win, ALLIGN, COHESION, SEPARATION, SEPFORCE, MAXSPEED, RED))
    return flock

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.init()
clock = pygame.time.Clock()
win.fill(BLACK)

#100 boids
flock = makeFlock(100)

FPS = 144

running = True
while running:
    delta = clock.tick(FPS)/1000
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            break
    #drawing and updating all the boids
    #ripples as updating 1 by 1
    #not exactly correct
    win.fill(BLACK)
    for boid in flock:
        boid.update(flock, delta)
        boid.show()
    pygame.display.update()
    
        
