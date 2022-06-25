import math

import pygame

import utils
from object import Object


class Marker(Object):
    sprite: pygame.SurfaceType

    def __init__(self, image, x, y, time):
        super().__init__(image, x, y,0.25,"Marker")

        self.start = pygame.time.get_ticks()
        self.end = time


    def draw(self,surf:pygame.SurfaceType,px,py):
        time = pygame.time.get_ticks()
        if (time-self.start)/self.end<1:
            alpha = 255-(utils.lerp(0,self.end,(time-self.start)/self.end)/1000)*255
        else:
            alpha = 0
            self.dead = True


        rect:pygame.rect.RectType = self.sprite.get_rect()
        rect.centerx = self.x+px
        rect.centery = self.y+py

        if rect.colliderect(surf.get_rect()) and alpha>0:
            #newimage = self.sprite.copy()
            #newimage.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
            self.sprite.set_alpha(alpha)
            surf.blit(self.sprite,rect)
            return 1
        else:
            return 0