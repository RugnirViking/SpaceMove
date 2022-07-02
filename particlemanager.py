import random

import pygame

class Particle():
    def __init__(self,pos,vel,color,size,life, gravity=700):
        self.startingpos = pos
        self.pos=pos
        self.vel=vel
        self.color=color
        self.size=size
        self.startingsize=size
        self.life=life
        self.dead=False
        self.age=0
        self.max_age=life
        self.gravity=gravity
        self.offset=[0,0]
        self.setoffset = False

    def update(self,dt,width,height,engine):
        if not self.setoffset:
            self.startingpos = [engine.player.x,engine.player.y]
            self.offset = [0,0]
            self.setoffset = True
        else:
            self.offset = [self.startingpos[0]-engine.player.x,self.startingpos[1]-engine.player.y]
        self.pos[0] += self.vel[0]*dt
        self.pos[1] += self.vel[1]*dt
        self.vel[1] += self.gravity*dt
        self.age += dt

        self.size = self.startingsize*(1-self.age/self.max_age)

        if self.age > self.max_age:
            self.dead=True
        if self.pos[0] < 0 or self.pos[0] > width:
            self.dead=True
        if self.pos[1] < 0 or self.pos[1] > height:
            self.dead=True



    def draw(self,surface,engine):
        pygame.draw.circle(surface,(self.color[0],self.color[1],self.color[2]),[self.pos[0]-self.offset[0],self.pos[1]-self.offset[1]],self.size)

class ParticleManager():
    def __init__(self, engine):
        self.particles = []
        self.engine= engine

    def add_particle(self, pos, vel, color, size, life, gravity=700):
        self.particles.append(Particle(pos, vel, color, size, life, gravity))

    def update(self, dt):
        width, height  = self.engine.surface.get_size()

        for particle in self.particles:
            particle.update(dt,width,height,self.engine)
            if particle.dead:
                self.particles.remove(particle)


    def draw(self, surf):
        for particle in self.particles:
            particle.draw(surf, self.engine)

