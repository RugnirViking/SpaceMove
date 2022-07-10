import math
import sys
import random

from pygame import SurfaceType

import colors
from AI import EnemyAI, SquarePatrolAI
from Asteroid import Asteroid
from asteroid_manager import AsteroidManager
from background import Background, newstar
from entity import Entity
from input_handlers import BaseEventHandler
from gamelogging import Logger
from typing import Optional, Any, Union, List

import pygame
from pygame.font import FontType
from pygame.ftfont import Font

from colors import WHITE, DARKGREY, LIGHTGREY, YELLOW
from marker import Marker
from object import Object
from optionsmenu import OptionsMenu
from particlemanager import ParticleManager
from player import Player
from projectilemanager import ProjectileManager
from utils import Singleton, rot_center, QuadEaseInOut
import gameUIcontroller



class Engine:
    # some magic to ward away evil spirits
    __metaclass__ = Singleton


    mastervolume: float
    textRect: pygame.rect
    objects: List[Object]
    bg_tiles: List[Background]
    surface: SurfaceType
    deltaTime: int
    getTicksLastFrame: int
    smallfont: Union[Font, FontType]
    titlefont: Union[Font, FontType]
    titletext: pygame.Surface
    player: Player

    @property
    def mastervolume(self):
        return self._mastervolume

    @mastervolume.setter
    def mastervolume(self, val):
        self._mastervolume = val
        pygame.mixer.music.set_volume(self.mastervolume * self.musicvolume)

    @property
    def musicvolume(self):
        return self._musicvolume

    @musicvolume.setter
    def musicvolume(self, val):
        self._musicvolume = val
        pygame.mixer.music.set_volume(self.mastervolume * self.musicvolume)

    @property
    def sound_effect_volume(self):
        return self._sound_effect_volume

    @sound_effect_volume.setter
    def sound_effect_volume(self, val):
        self._sound_effect_volume = val

    @property
    def width(self):
        return self.surface.get_width()

    @property
    def height(self):
        return self.surface.get_height()

    logger: Logger

    def __init__(self,surf: pygame.SurfaceType) -> None:
        self.targetsprite = None
        self.logger = Logger()
        self.surface = surf
        self.asteroid_manager = AsteroidManager()

        self.player: Player = Player("resources/img/lightfoot.png",self)
        self.getTicksLastFrame = 0
        self.deltaTime = 0
        #Set up fonts
        self.smallfont = pygame.font.SysFont(None, 48)
        self.smallfont2 = pygame.font.SysFont(None, 24)
        self.titlefont = pygame.font.Font("resources/fonts/Bungee-Regular.ttf", 72)

        self.targetpx = 0
        self.targetpy = 0

        self.objects = []
        self.bg_tiles = []
        self.star_field_slow = []
        self.star_field_medium = []
        self.star_field_fast = []

        self._mastervolume = 0.5
        self._musicvolume = 1
        self._sound_effect_volume = 1
        self.flashrising = True
        self.mouse_pos = (0,0)

        self.explosion_group = pygame.sprite.Group()

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

        self.bg_tiles.append(Background("resources/img/sun.png",100,100,1,1,False))
        self.bg_tiles.append(Background("resources/img/planet1.png",1000,100,0.8,0.5))
        self.station = Object("resources/img/spacestation.png",1000,1000,1,"Station")
        self.objects.append(self.station)
        self.objects.append(Entity("resources/img/flea.png",1800,1000,0.5,"Flea-class Fighter",self,SquarePatrolAI(self),100))

        # spawn four asteroids
        self.asteroids = []
        for i in range(178):
            self.asteroids.append(Asteroid(random.randrange(-2730,2730),random.randrange(-1330,1330),0.5,"Asteroid",self,self.asteroid_manager))
            self.objects.append(self.asteroids[i])

        pygame.mixer.init()
        pygame.mixer.music.load('resources/sound/SpaceMining.mp3')
        pygame.mixer.music.play(-1)

        self.alert_sound = pygame.mixer.Sound("resources/sound/alert.wav")

        self._mastervolume = self.mastervolume
        self._musicvolume = self.musicvolume
        self._sound_effect_volume = self.sound_effect_volume

        self.mastervolume = 0.5
        self.musicvolume = 1
        self.sound_effect_volume = 1
        pygame.mixer.music.set_volume(self.mastervolume * self.musicvolume)

        self.flash_end_time = 0
        self.flash_start_time = 0
        self.t = 0

        self.clock = pygame.time.Clock()
        self.logger.log("Engine load complete")

        self.sectorfont = pygame.font.Font("resources/fonts/batmanfa.ttf", 24)
        self.particlemanager = ParticleManager(self)
        self.projectilemanager = ProjectileManager(self)
        self.gameUIcontroller = gameUIcontroller.GameUIController(self)
        self.damagetext = []
        self.damagefont = pygame.font.Font(None, 24)

    def is_in_radar_range(self,x,y):
        return (x + self.player.x - self.width / 2) ** 2 + (
                    y + self.player.y - self.height / 2) ** 2 < self.player.minimapradius ** 2

    def is_in_bounds(self,x,y):
        return abs(x) < 2730 and abs(y) < 1330

    def is_on_screen(self,x,y):
        return x > -self.player.x-self.width/2 and x < -self.player.x+self.width/2 and y > -self.player.y-self.height/2 and y < -self.player.y+self.height/2

    def distance_to_entity(self, entity, x: int, y: int) -> float:
        if isinstance(entity, Entity):
            return math.sqrt((entity.x - x) ** 2 + (entity.y - y) ** 2)
        elif isinstance(entity, Player):
            return math.dist((-self.player.x + self.width/2,-self.player.y + self.height/2),(x,y))

        #math.dist((self.entity.x, self.entity.y),
        #          (-self.engine.px + self.engine.surface.get_width() / 2,
        #           -self.engine.py + self.engine.surface.get_height() / 2))

    def playsound(self,sound,vol=0.95):
        sound.set_volume(vol * self.mastervolume * self.sound_effect_volume)
        pygame.mixer.find_channel(True).play(sound)

    def Render_Text(self, what, font:pygame.font.FontType, color, where, surf, centered=False):
        text:pygame.SurfaceType = font.render(what, 1, color)
        if centered:
            rect = text.get_rect()
            rect.centerx = where[0]
            rect.centery = where[1]
            surf.blit(text, rect)
        else:
            surf.blit(text, where)
    def minimap_dist_convert(self, dist: float) -> float:
        w_minimapwidth = 2730*2
        w_minimapheight = 1330*2
        s_minimapwidth = 468
        s_minimapheight = 238
        return dist * (s_minimapwidth / w_minimapwidth)


    def draw(self,surf: pygame.SurfaceType) -> None:

        self.clock.tick()
        t = pygame.time.get_ticks()
        self.t = t
        # deltaTime in seconds.
        self.deltaTime = (t - self.getTicksLastFrame) / 1000.0
        self.getTicksLastFrame = t
        mx, my = pygame.mouse.get_pos()
        self.mouse_pos = (mx, my)

        self.update()
        if t > self.flash_end_time:
            self.flash_end_time = t + 500
            self.flash_start_time = t

            self.flashrising = not self.flashrising

        for bg in self.bg_tiles:
            bg.draw(surf,self.player.x,self.player.y)
        width, height = surf.get_width(),surf.get_height()

        # animate some motherfucking stars

        for star in self.star_field_slow:
            pos = (int(star[0]+self.player.x*1.2),int(star[1]+self.player.y*1.2))
            if not surf.get_rect().collidepoint(pos):
                newstar(width,height,self,star,1.2)

            pygame.draw.circle(surf, DARKGREY, pos, 3)

        for star in self.star_field_medium:
            pos = (int(star[0]+self.player.x*2),int(star[1]+self.player.y*2))
            if not surf.get_rect().collidepoint(pos):
                newstar(width,height,self,star,2)

            pygame.draw.circle(surf, LIGHTGREY, pos, 3)

        for star in self.star_field_fast:
            pos = (int(star[0]+self.player.x*4),int(star[1]+self.player.y*4))
            if not surf.get_rect().collidepoint(pos):
                newstar(width,height,self,star,4)

            pygame.draw.circle(surf, YELLOW, pos, 3)

        pos = self.world_to_screen((-2730, -1330))
        pygame.draw.rect(surf, colors.RED, (pos[0],pos[1],2730*2,1330*2), 15)

        self.explosion_group.draw(surf)
        self.explosion_group.update(self.deltaTime)

        count = 0


        for object in self.objects:
            count += object.draw(surf,self.player.x,self.player.y)
            if object.dead:
                self.objects.remove(object)

        # draw a reticle around the targeted enemy, if there is one
        if self.player.target is not None:
            fac = 0.75
            transparentsurface = pygame.Surface(
                (self.player.target.width * 2 * fac, self.player.target.width * 2 * fac), pygame.SRCALPHA)

            pygame.draw.circle(transparentsurface, (255, 0, 0),
                               (self.player.target.width * fac, self.player.target.width * fac),
                               self.player.target.width * fac, 2)
            transparentsurface.set_alpha(128)
            surf.blit(transparentsurface, (
            int(self.player.target.x + self.player.x - self.player.target.width * fac),
            int(self.player.target.y + self.player.y - self.player.target.width * fac)))

        self.particlemanager.draw(surf)
        self.projectilemanager.draw(surf)
        self.player.draw(surf)

        self.gameUIcontroller.draw(surf,width,height)

    def update(self):
        self.particlemanager.update(self.deltaTime)
        self.projectilemanager.update(self.deltaTime)
        for object in self.objects:
            if object.dead:
                self.objects.remove(object)

    def mouseup(self, pos, btn, event: pygame.event):
        x, y = pos
        if btn == pygame.BUTTON_LEFT:
            centerx = self.surface.get_rect().centerx
            centery = self.surface.get_rect().centery
            minimap = pygame.Rect(1455,840,465,240)
            if minimap.collidepoint(x,y):
                # clicked on the minimap
                mmx = x-1455
                mmy = y-846
                mmxr = mmx/452 # 452 is minimap width
                mmyr = mmy/220 # 220 is minimap height
                worldx = (mmxr*2727*2)-2727
                worldy = (mmyr*1330*2)-1330

                self.trim_markers()
                # it makes no sense that adding half the screen's size to this position would work, and yet here we are.
                self.objects.append(Marker("resources/img/marker2.png",worldx+self.surface.get_width()/2,worldy+self.surface.get_height()/2,500))
                self.targetpx = worldx
                self.targetpy = worldy
                pass
            else:
                worldpos = self.screen_to_world(pos)
                self.trim_markers()
                self.objects.append(Marker("resources/img/marker1.png",worldpos[0],worldpos[1],1000))
                self.targetpx = worldpos[0]-self.width/2
                self.targetpy = worldpos[1]-self.height/2
        elif btn == pygame.BUTTON_RIGHT:
            for entity in self.objects:
                if isinstance(entity,Entity):
                    if entity.get_rect().collidepoint(pos):
                        self.player.target = entity

    def trim_markers(self):
        count=0
        for object in reversed(self.objects):
            if isinstance(object,Marker):
                count+=1
                if count>3:
                    self.objects.remove(object)

    def screen_to_world(self,pos,fac=1):
        return (pos[0]-self.player.x*fac,pos[1]-self.player.y*fac)

    def world_to_screen(self,pos,fac=1):
        return (self.player.x*fac+pos[0]+self.width/2,self.player.y*fac+pos[1]+self.height/2)
