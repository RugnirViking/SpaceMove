import math

import pygame

from object import Object
from utils import rot_center, ANGULAR_VELOCITY

# something with a 
class Entity(Object):
    sprite: pygame.SurfaceType

    def __init__(self, image, x, y, fac, engine):
        super().__init__(image, x, y, fac)
        self.target = (x - 300, y - 300)
        self.angle = -90
        self.angle_target = 0.0
        self.engine = engine
        self.loadcheck = False
        self.player_target = False
        self.fireangle = 0
        self.target_sprite = self.sprite.copy().convert_alpha()
        brighten = 255
        self.target_sprite.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD)
        self.lastrect = None

    def draw(self, surf: pygame.SurfaceType, px, py):

        if self.loadcheck:
            self.do_movement(surf, px, py)
        else:
            self.loadcheck = True

        rect: pygame.rect.RectType = self.sprite.get_rect()
        rect.centerx = self.x + px
        rect.centery = self.y + py
        rotated_image, rrect = rot_center(self.sprite, rect, self.fireangle)
        self.lastrect = rrect

        if rect.colliderect(surf.get_rect()):
            surf.blit(rotated_image, rrect)
            return 1
        else:
            return 0

    def do_movement(self, surf, px, py):
        self.angle = self.angle % 360

        angle_error = (self.angle - self.angle_target) % 360

        if 0 < angle_error < 180:
            self.angle -= ANGULAR_VELOCITY * self.engine.deltaTime
            if angle_error < ANGULAR_VELOCITY * self.engine.deltaTime:
                self.angle = self.angle_target
        elif angle_error > 180:
            self.angle += ANGULAR_VELOCITY * self.engine.deltaTime
            if angle_error < ANGULAR_VELOCITY * self.engine.deltaTime:
                self.angle = self.angle_target
        if abs(self.angle - self.angle_target) < 5:
            self.angle = self.angle_target

            # do player control

            err = math.dist((self.x, self.y), (self.target[0], self.target[1]))
            snapped = False
            self.retarget(False)
            if err < (200 * self.engine.deltaTime):
                self.x = self.target[0]
                self.y = self.target[1]
                snapped = True
                self.retarget(True)
            else:
                self.x -= 200 * math.sin(self.angle * (math.pi / 180)) * self.engine.deltaTime
                self.y -= 200 * math.cos(self.angle * (math.pi / 180)) * self.engine.deltaTime

            if err > (2000 * self.engine.deltaTime) and not snapped:
                o = self.target[0] - self.x
                a = self.target[1] - self.y
                angle = math.atan2(o, a)
                self.set_new_angle(angle * (180 / math.pi) - 180)
        if self.player_target:

            playerpos = (-self.engine.px + self.engine.surface.get_width() / 2,
                           -self.engine.py + self.engine.surface.get_height() / 2)
            o = playerpos[0] - self.x
            a = playerpos[1] - self.y
            angle = math.atan2(o, a)
            self.fireangle = (angle * (180 / math.pi) - 180) % 360
        else:
            self.fireangle = self.angle

    def retarget(self, aquire_bearing=False):
        dist = 9999
        if self.player_target:
            dist = self.dist_to_player()
        if self.player_target and dist>1600:
            self.target = (self.x, self.y)
            self.player_target = False
        if not self.player_target:
            if self.dist_to_player() < 400:
                self.player_target = True
        elif aquire_bearing:
            if self.player_target and dist < 1600:
                self.target = (-self.engine.px + self.engine.surface.get_width() / 2,
                               -self.engine.py + self.engine.surface.get_height() / 2)


    def dist_to_player(self) -> float:
        return math.dist((self.x, self.y),
                         (-self.engine.px + self.engine.surface.get_width() / 2,
                          -self.engine.py + self.engine.surface.get_height() / 2))

    def set_new_angle(self, angle):
        self.angle_target = angle % 360

    def get_rect(self) -> pygame.rect.RectType:
        return self.lastrect
