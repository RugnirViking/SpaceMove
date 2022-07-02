import math
import random

import pygame

def newstar(width,height,engine,star,fac=1):
    lr_prop = math.sin(engine.player.angle * (math.pi / 180))
    udprop = math.cos(engine.player.angle * (math.pi / 180))

    side = random.random()
    topleft = (0, 0)
    topleft2 = (0, 0)
    if lr_prop < 0 and udprop < 0:
        topleft = (width, height)
        topleft2 = (0, 0)
    elif lr_prop < 0:
        topleft = (width, 0)
        topleft2 = (0, 0)
    elif udprop < 0:
        topleft = (0, height)
        topleft2 = (0, 0)
    topleftworld = engine.screen_to_world(topleft, fac)
    topleftworld2 = engine.screen_to_world(topleft2, fac)

    if side > abs(lr_prop):
        star[0] = random.randrange(int(topleftworld2[0]), int(topleftworld2[0] + width))
        star[1] = int(topleftworld[1])
    else:
        star[0] = int(topleftworld[0])
        star[1] = random.randrange(int(topleftworld2[1]), int(topleftworld2[1] + height))



class Background():
    sprite: pygame.SurfaceType

    def __init__(self, image, x, y, factor,scale=1,a=True):
        self.x=x
        self.y=y
        self.factor = factor
        if a:
            self.sprite = pygame.image.load(image).convert_alpha()
        else:
            self.sprite = pygame.image.load(image).convert()
        self.width, self.height = self.sprite.get_width(), self.sprite.get_height()  # get size
        self.sprite = pygame.transform.scale(self.sprite, (int(self.width*scale), int(self.height*scale)))

    def draw(self,surf,px,py):
        surf.blit(self.sprite,(self.x+px/self.factor-self.width/2,self.y+py/self.factor-self.height/2))