import math
import sys
import random

from pygame import SurfaceType

from background import Background, newstar
from input_handlers import BaseEventHandler
from logging import Logger
from typing import Optional, Any, Union, List

import pygame
from pygame.font import FontType
from pygame.ftfont import Font

from colors import WHITE, DARKGREY, LIGHTGREY, YELLOW
from marker import Marker
from object import Object
from player import Player
from utils import Singleton


class Engine:
    # some magic to ward away evil spirits
    __metaclass__ = Singleton


    textRect: pygame.rect
    objects: List[Object]
    bg_tiles: List[Background]
    surface: SurfaceType
    deltaTime: int
    getTicksLastFrame: int
    smallfont: Union[Font, FontType]
    titlefont: Union[Font, FontType]
    titletext: pygame.Surface


    logger: Logger

    def __init__(self,surf: pygame.SurfaceType) -> None:
        self.logger = Logger()
        self.surface = surf

        self.player = Player("resources/img/fighter.png",self)
        self.getTicksLastFrame = 0
        self.deltaTime = 0
        #Set up fonts
        self.smallfont = pygame.font.SysFont(None, 48)
        self.titlefont = pygame.font.Font("resources/fonts/Bungee-Regular.ttf", 72)

        self.px = 0
        self.py = 0

        self.targetpx = 0
        self.targetpy = 0

        self.objects = []
        self.bg_tiles = []
        self.star_field_slow = []
        self.star_field_medium = []
        self.star_field_fast = []

        for slow_stars in range(50):  # birth those plasma balls, baby
            star_loc_x = random.randrange(0, self.surface.get_width())
            star_loc_y = random.randrange(0, self.surface.get_height())
            self.star_field_slow.append([star_loc_x, star_loc_y])

        for medium_stars in range(35):
            star_loc_x = random.randrange(0, self.surface.get_width())
            star_loc_y = random.randrange(0, self.surface.get_height())
            self.star_field_medium.append([star_loc_x, star_loc_y])

        for fast_stars in range(15):
            star_loc_x = random.randrange(0, self.surface.get_width())
            star_loc_y = random.randrange(0, self.surface.get_height())
            self.star_field_fast.append([star_loc_x, star_loc_y])

        self.bg_tiles.append(Background("resources/img/sun.png",100,100,1))
        self.bg_tiles.append(Background("resources/img/planet1.png",1000,100,0.8,0.5))

        pygame.mixer.init()
        pygame.mixer.music.load('resources/sound/SpaceMining.mp3')
        pygame.mixer.music.play(-1)

        self.clock = pygame.time.Clock()
        self.logger.log("Engine load complete")

    def Render_Text(self, what, color, where, surf):
        text = self.smallfont.render(what, 1, color)
        surf.blit(text, where)

    def draw(self,surf: pygame.SurfaceType) -> None:

        self.clock.tick()
        t = pygame.time.get_ticks()
        # deltaTime in seconds.
        self.deltaTime = (t - self.getTicksLastFrame) / 1000.0
        self.getTicksLastFrame = t

        for bg in self.bg_tiles:
            bg.draw(surf,self.px,self.py)
        width, height = surf.get_width(),surf.get_height()
        # animate some motherfucking stars

        for star in self.star_field_slow:
            pos = (int(star[0]+self.px*1.2),int(star[1]+self.py*1.2))
            if not surf.get_rect().collidepoint(pos):
                newstar(width,height,self,star,1.2)

            pygame.draw.circle(surf, DARKGREY, pos, 3)

        for star in self.star_field_medium:
            pos = (int(star[0]+self.px*2),int(star[1]+self.py*2))
            if not surf.get_rect().collidepoint(pos):
                newstar(width,height,self,star,2)

            pygame.draw.circle(surf, LIGHTGREY, pos, 3)

        for star in self.star_field_fast:
            pos = (int(star[0]+self.px*4),int(star[1]+self.py*4))
            if not surf.get_rect().collidepoint(pos):
                newstar(width,height,self,star,4)

            pygame.draw.circle(surf, YELLOW, pos, 3)

        count = 0
        for object in self.objects:
            count += object.draw(surf,self.px,self.py)
            if object.dead:
                self.objects.remove(object)

        self.player.draw(surf)

        pygame.draw.rect(surf, (0, 0, 0), pygame.Rect(0, 0, 80, 50))
        self.Render_Text(str(int(self.clock.get_fps())), (255, 0, 0), (10, 10),surf)

        err = math.dist((self.px,self.py), (-self.targetpx,-self.targetpy))


        snapped = False
        if err < (200 * self.deltaTime):
            self.px = -self.targetpx
            self.py = -self.targetpy
            snapped = True
        else:
            self.px += 200 * math.sin(self.player.angle * (math.pi / 180)) * self.deltaTime
            self.py += 200 * math.cos(self.player.angle * (math.pi / 180)) * self.deltaTime

        if err>(2000 * self.deltaTime) and not snapped:
            o = self.targetpx+self.px
            a = self.targetpy+self.py
            angle = math.atan2(o,a)
            self.player.set_new_angle(angle*(180/math.pi)-180)

        pygame.draw.rect(surf,(80,80,80),pygame.Rect(80,0,surf.get_width()-80,50))

        minirect = pygame.Rect(width-480+6, height-250+6, 480-12, 250-12)
        pygame.draw.rect(surf, (45,45,45), pygame.Rect(width-480+6, height-250+6, 480-12, 250-12))
        pygame.draw.rect(surf, LIGHTGREY, pygame.Rect(width-480+6, height-250+6, 480-12, 250-12),12)

        pygame.draw.circle(surf,(255,0,0),(int(minirect.centerx-self.px/12),int(minirect.centery-self.py/12)),6)

    def mouseup(self, pos, btn, event: pygame.event):
        x, y = pos
        centerx = self.surface.get_rect().centerx
        centery = self.surface.get_rect().centery


        worldpos = self.screen_to_world(pos)
        self.objects.append(Marker("resources/img/marker1.png",worldpos[0],worldpos[1],1000))
        self.targetpx = worldpos[0]-self.surface.get_width()/2
        self.targetpy = worldpos[1]-self.surface.get_height()/2

    def screen_to_world(self,pos,fac=1):
        return (pos[0]-self.px*fac,pos[1]-self.py*fac)

    def world_to_screen(self,pos,fac=1):
        return (self.px*fac+pos[0],self.py*fac+pos[1])
