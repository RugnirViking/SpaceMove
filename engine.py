import math
import sys
import random

from pygame import SurfaceType

import colors
from AI import EnemyAI, SquarePatrolAI
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
from player import Player
from utils import Singleton, rot_center, QuadEaseInOut


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

    logger: Logger

    def __init__(self,surf: pygame.SurfaceType) -> None:
        self.targetsprite = None
        self.logger = Logger()
        self.surface = surf

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

        self.bg_tiles.append(Background("resources/img/sun.png",100,100,1))
        self.bg_tiles.append(Background("resources/img/planet1.png",1000,100,0.8,0.5))
        self.station = Object("resources/img/spacestation.png",1000,1000,1,"Station")
        self.objects.append(self.station)
        self.objects.append(Entity("resources/img/flea.png",1800,1000,0.5,"Flea-class Fighter",self,SquarePatrolAI(self)))

        pygame.mixer.init()
        pygame.mixer.music.load('resources/sound/SpaceMining.mp3')
        pygame.mixer.music.play(-1)

        self.alert_sound = pygame.mixer.Sound("resources/sound/alert.wav")
        self.warning_symbol = pygame.image.load("resources/img/warning.png").convert_alpha()
        w_width, w_height = self.warning_symbol.get_width(), self.warning_symbol.get_height()  # get size
        self.warning_symbol = pygame.transform.scale(self.warning_symbol, (int(w_width/4), int(w_height/4)))

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

        self.headerui = pygame.image.load("resources/img/uiheader.png").convert_alpha()
        self.headerui = pygame.transform.scale(self.headerui, (int(self.headerui.get_rect().width/2), int(self.headerui.get_rect().height/2)))
        self.headeruiflipped = pygame.transform.flip(self.headerui, True, False)
        self.clock = pygame.time.Clock()
        self.logger.log("Engine load complete")

        self.sectorfont = pygame.font.Font("resources/fonts/batmanfa.ttf", 24)
        self.sectortext = self.sectorfont.render("Sector 12-1-AB", True, colors.BLACK)
        self.sectortextrect = self.sectortext.get_rect()
        self.sectortextrect.center = (self.surface.get_width()/2, 18)

        self.damagetext = []


    def distance_to_entity(self, entity, x: int, y: int) -> float:
        if isinstance(entity, Entity):
            return math.sqrt((entity.x - x) ** 2 + (entity.y - y) ** 2)
        elif isinstance(entity, Player):
            return math.dist((-self.player.x + self.surface.get_width()/2,-self.player.y + self.surface.get_height()/2),(x,y))

        #math.dist((self.entity.x, self.entity.y),
        #          (-self.engine.px + self.engine.surface.get_width() / 2,
        #           -self.engine.py + self.engine.surface.get_height() / 2))

    def Render_Text(self, what, font:pygame.font.FontType, color, where, surf, centered=False):
        text:pygame.SurfaceType = font.render(what, 1, color)
        if centered:
            rect = text.get_rect()
            rect.centerx = where[0]
            rect.centery = where[1]
            surf.blit(text, rect)
        else:
            surf.blit(text, where)

    def draw(self,surf: pygame.SurfaceType) -> None:

        self.clock.tick()
        t = pygame.time.get_ticks()
        self.t = t
        # deltaTime in seconds.
        self.deltaTime = (t - self.getTicksLastFrame) / 1000.0
        self.getTicksLastFrame = t
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

        self.explosion_group.draw(surf)
        self.explosion_group.update(self.deltaTime)

        # draw a reticle around the targeted enemy, if there is one
        if self.player.target is not None:
            transparentsurface = pygame.Surface((85*2, 85*2), pygame.SRCALPHA)
            pygame.draw.circle(transparentsurface,(255,0,0,64),(85,85),85,2)
            surf.blit(transparentsurface,(int(self.player.target.x+self.player.x-85),int(self.player.target.y+self.player.y-85)))
        count = 0
        for object in self.objects:
            count += object.draw(surf,self.player.x,self.player.y)
            if object.dead:
                self.objects.remove(object)

        self.player.draw(surf)

        if self.player.is_in_radiation:
            # render the warning symbol partially transparent
            t_surf = pygame.Surface((self.warning_symbol.get_width(), self.warning_symbol.get_height()),
                                    pygame.SRCALPHA)
            a = int(QuadEaseInOut(0,255,500).ease(t-self.flash_start_time))
            if self.flashrising:
                a = 255-a
            self.warning_symbol.set_alpha(a)
            w_rect = self.warning_symbol.get_rect()
            w_rect.centerx = self.surface.get_width() - 240
            w_rect.bottom = self.surface.get_height() - 300
            t_surf.blit(self.warning_symbol, (0, 0))
            surf.blit(t_surf, w_rect)

            self.Render_Text("Radiation", self.sectorfont, colors.RED, (w_rect.centerx, w_rect.centery - 80), surf, centered=True)


        pygame.draw.rect(surf, (0, 0, 0), pygame.Rect(0, 0, 80, 50))
        self.Render_Text(str(int(self.clock.get_fps())), self.smallfont2, (255, 0, 0), (24, 18),surf)

        pygame.draw.rect(surf,(0,0,0),pygame.Rect(80,0,surf.get_width()-80,50))

        minirect = pygame.Rect(width-480+6, height-250+6, 480-12, 250-12)
        pygame.draw.rect(surf, (45,45,45), pygame.Rect(width-480+6, height-250+6, 480-12, 250-12))
        pygame.draw.rect(surf, LIGHTGREY, pygame.Rect(width-480+6, height-250+6, 480-12, 250-12),12)

        pygame.draw.circle(surf,(255,0,0),(int(minirect.centerx-self.player.x/12),int(minirect.centery-self.player.y/12)),6)
        pygame.draw.circle(surf,(255,255,0),(int(minirect.centerx+self.targetpx/12),int(minirect.centery+self.targetpy/12)),2)

        # if the player is close enough to the space station to dock, display a text notification
        if self.player.distance_to(self.station) < 250:
            self.Render_Text("DOCK", self.smallfont2, (255, 255, 255), (135,25), surf, centered=True)


        for object in self.objects:
            if not isinstance(object,Marker):
                if isinstance(object, Entity):
                    if self.player.target == object:
                        # draw a cross on the minimap at the player's targeted enemy
                        tpos = (int(minirect.centerx + (object.x - width / 2) / 12), int(minirect.centery + (object.y - height / 2) / 12))
                        pygame.draw.circle(surf, (255, 255, 0),
                                           (tpos[0]+1,
                                            tpos[1]+1),3)
                        pygame.draw.line(surf, (255, 255, 0),(tpos[0]-5,tpos[1]-5),(tpos[0]+5,tpos[1]+5),2)
                        pygame.draw.line(surf, (255, 255, 0),(tpos[0]-5,tpos[1]+5),(tpos[0]+5,tpos[1]-5),2)
                        pygame.draw.circle(surf, (0, 128, 255),
                                       (int(minirect.centerx + (object.ai.targetpos[0] - width / 2) / 12),
                                        int(minirect.centery + (object.ai.targetpos[1] - height / 2) / 12)), 2)
                    else:
                        pygame.draw.circle(surf, (0, 128, 255),
                                       (int(minirect.centerx + (object.ai.targetpos[0] - width / 2) / 12),
                                        int(minirect.centery + (object.ai.targetpos[1] - height / 2) / 12)), 2)
                        pygame.draw.circle(surf, (255, 255, 255),
                               (int(minirect.centerx + (object.x-width/2) / 12), int(minirect.centery + (object.y-height/2) / 12)), 4)



        self.Render_Text(f"{round(self.player.x)}, {round(self.player.y)}", self.smallfont2, (255, 255, 255), (width-580, height-20),surf,True)
        mx, my = pygame.mouse.get_pos()
        mp = (mx,my)
        mp_world = self.screen_to_world(mp)
        self.Render_Text(f"{round(mx)}, {round(my)} ({round(mp_world[0]-surf.get_width()/2)}, {round(mp_world[1]-surf.get_height()/2)})", self.smallfont2, (255, 255, 255), (width-580, height-45),surf,True)

        self.Render_Text(f"{round(self.targetpx)}, {round(self.targetpy)}", self.smallfont2, (255, 255, 255), (width-580, height-70),surf,True)

        if self.player.target and not self.targetsprite:
            twidth, theight = self.player.target.target_sprite.get_width(), self.player.target.target_sprite.get_height()
            self.targetsprite = self.player.target.target_sprite#pygame.transform.scale(self.player.target.target_sprite, (int(twidth), int(theight)))
        elif self.player.target and self.targetsprite:

            trect: pygame.rect.RectType = self.targetsprite.get_rect()
            twidth, theight = trect.width, trect.height
            largest = max(twidth,theight)/1.5
            pygame.draw.circle(surf,(45,45,45),(100,400),int(largest))
            pygame.draw.circle(surf,(165,165,165),(100,400),int(largest),2)

            trect.centerx = 100
            trect.centery = 400
            rotated_image, rrect = rot_center(self.targetsprite, trect, self.player.target.ai.look_angle)
            surf.blit(rotated_image,rrect)

            self.Render_Text(f"Dist: {round(self.player.target.ai.dist_to_player(),1)}", self.smallfont2, (255, 255, 255),
                             (100, 500), surf, True)

        # update and draw all the damagetext
        for text in self.damagetext:
            text.update(self.deltaTime)
            text.draw(surf)
            if not text.active:
                self.damagetext.remove(text)


        # render the hp bar under the overlay
        hull_pct = self.player.hull / self.player.max_hull
        hull_rect = pygame.Rect(0,0,int(hull_pct*410),10)
        hull_rect.right = width/2-210
        hull_rect.bottom = 35
        pygame.draw.rect(surf,(0,180,0),hull_rect)


        # render the player shield bar under the overlay
        hull_pct = self.player.hull / self.player.max_hull
        hull_rect = pygame.Rect(0,0,int(hull_pct*420),10)
        hull_rect.right = width/2-215
        hull_rect.bottom = 20
        pygame.draw.rect(surf,(0,80,255),hull_rect)

        # render the player energy bar under the overlay
        hull_pct = self.player.energy / self.player.max_energy
        hull_rect = pygame.Rect(0,0,int(hull_pct*420),10)
        hull_rect.left = width/2+215
        hull_rect.bottom = 20
        pygame.draw.rect(surf,(255,255,0),hull_rect)

        # render the player heat bar under the overlay
        hull_pct = self.player.heat / self.player.max_heat
        hull_rect = pygame.Rect(0,0,int(hull_pct*410),10)
        hull_rect.left = width/2+210
        hull_rect.bottom = 35
        pygame.draw.rect(surf,(200,80,0),hull_rect)

        #  render the overlay
        headerRect = self.headerui.get_rect()
        headerRect.right = width/2+50
        headerRect.top = 0
        surf.blit(self.headerui,headerRect)

        headeruiflipped = self.headeruiflipped.get_rect()
        headeruiflipped.left = width/2-50
        headeruiflipped.top = 0
        surf.blit(self.headeruiflipped,headeruiflipped)

        # render the sector
        surf.blit(self.sectortext,self.sectortextrect)



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
                self.objects.append(Marker("resources/img/marker1.png",worldx+self.surface.get_width()/2,worldy+self.surface.get_height()/2,500))
                self.targetpx = worldx
                self.targetpy = worldy
                pass
            else:
                worldpos = self.screen_to_world(pos)
                self.trim_markers()
                self.objects.append(Marker("resources/img/marker1.png",worldpos[0],worldpos[1],1000))
                self.targetpx = worldpos[0]-self.surface.get_width()/2
                self.targetpy = worldpos[1]-self.surface.get_height()/2
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
        return (self.player.x*fac+pos[0],self.player.y*fac+pos[1])
