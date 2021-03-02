import pygame
import math
import random
from pygame import gfxdraw

#constant colours
WHITE = (255,255,255)
BLACK = (  0,  0,  0)
RED   = (255,  0,  0)
GREEN = (  0,255,  0)
BLUE  = (  0,  0,255)
GREY  = ( 30, 30, 30)

#defining vector2D
#using vector2D as it is what im used to in C#
vector2D = pygame.math.Vector2

class boid():
    def __init__(self, win, allignSight, cohesionSight, separationSight, separationForce, maxSpeed, colour, wrap = True):
        #window to draw to and the dimensions of said window
        self.win = win
        self.width, self.height = self.win.get_size()

        #whether the boids can leave one side and come through other
        self.wrap = wrap

        #colour of boid
        self.colour = colour

        #maxSpeed -> int
        self.maxSpeed = maxSpeed
        #random position -> vector2D
        self.position = vector2D(random.randint(0, self.width), random.randint(0, self.height))

        #the perception of the the boid during different functions
        self.allignSight = allignSight
        self.cohesionSight = cohesionSight
        self.separationSight = separationSight
        self.separationForce = separationForce

        #velocity and acceleration of the boid
        self.vel = vector2D(random.uniform(-self.maxSpeed, self.maxSpeed), random.uniform(-self.maxSpeed, self.maxSpeed))
        self.acc = vector2D(0, 0)

    #wrap arounds the screen or avoids it
    ''' WORK IN PROGRESS ON AVOIDING EDGES'''
    def wrapAround(self):
        if self.wrap:
            if self.position.x > self.width:
                self.position.x = 0
            elif self.position.x < 0:
                self.position.x = self.width
            
            if self.position.y > self.height:
                self.position.y = 0
            elif self.position.y < 0:
                self.position.y = self.height
            return
        
    #updates the boids position and velocity
    def update(self, flock, delta):
        self.acc = vector2D(0, 0) 
        self.acc += self.allign(flock)
        self.acc += self.cohesion(flock)
        for i in flock:
            if i != self:
                self.acc += self.separation(i.position) 
        #multiplying by time delta so it moves at same speed on different FPS
        self.vel += self.acc * delta
        #normalising the vector then scaling
        if self.vel != vector2D(0,0):
            self.vel = self.vel.normalize() * self.maxSpeed
        self.position += self.vel
        self.wrapAround()

    def otherBoidInSight(self, boid, sight):
        if math.hypot(self.position.x - boid.position.x, self.position.y - boid.position.y) <= sight:
            return True
        return False

    def allign(self, flock):
        total = vector2D(0, 0)
        count = 0
        #going through the flock
        for boid in flock:
            if boid != self:
                #if it is in the range of the boid
                if self.otherBoidInSight(boid, self.allignSight):
                    if boid.vel.x != 0 and boid.vel.y != 0:
                        #adding the other boids velocity so we can calculate the average velocity
                        total += boid.vel.normalize() * self.maxSpeed
                        count += 1
        if count != 0:
            total /= count
            allign = total - self.vel
            if allign.length() > self.maxSpeed:
                allign.normalize() * self.maxSpeed
            return allign
        
        return vector2D(0,0)

    #move to centre of near boids
    def cohesion(self, flock):
        '''needs fine tuning'''
        coStrength = 1.2
        totalPos = vector2D(0, 0)
        count = 0
        for boid in flock:
            if boid != self:
                if self.otherBoidInSight(boid, self.cohesionSight):
                    totalPos += boid.position
                    count += 1
        if count != 0:
            avgPos = totalPos / count
            cohes = avgPos - self.position  
            return cohes * coStrength
        return vector2D(0,0)
     
    #keep boids appart
    def separation(self, target):
        steer = vector2D(0,0)
        dist = self.position - target
        desired = vector2D(0,0)

        if dist.x != 0 and dist.y != 0 :
            if dist.length() < self.separationSight:
                desired = dist.normalize() * self.maxSpeed
            else:
                desired = self.vel.normalize() * self.maxSpeed
        steer = desired - self.vel
        if steer.length() > self.separationForce:
            steer.scale_to_length(self.separationForce)
        return steer

    #draw/show boid on the window
    def show(self):
        gfxdraw.filled_circle(self.win, int(self.position.x), int(self.position.y), 7, self.colour)
