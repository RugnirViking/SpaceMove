import math
from typing import TYPE_CHECKING, Optional

import pygame
from pygame import Rect

from colors import WHITE
from entity import Entity
from object import Object
from utils import rot_center, ANGULAR_VELOCITY

if TYPE_CHECKING:
    from engine import Engine





class Player():
    target: Optional[Entity]
    sprite: pygame.image
    angle: float
    angle_target: float

    def __init__(self, img_path, engine):
        self.angle = 0.0
        self.sprite = pygame.image.load(img_path).convert_alpha()
        self.angle_target = 0.0
        self.engine = engine
        self.angular_vel = 0
        self.max_angular_vel = 350
        width, height = self.sprite.get_width(), self.sprite.get_height()  # get size
        self.sprite = pygame.transform.scale(self.sprite, (int(width / 6), int(height / 6)))
        self.target = None
        self.hull = 100.0
        self.max_hull = 100.0
        self.shields = 100.0
        self.max_shields = 100.0
        self.energy = 100.0
        self.max_energy = 100.0
        self.heat = 50
        self.max_heat = 100.0

    def draw(self, surf):
        self.angle = self.angle % 360

        angle_error = (self.angle - self.angle_target) % 360

        if 0 < angle_error < 180:
            self.angle -= self.max_angular_vel * self.engine.deltaTime
            if angle_error < self.max_angular_vel * self.engine.deltaTime:
                self.angle = self.angle_target
        elif angle_error > 180:
            self.angle += self.max_angular_vel * self.engine.deltaTime
            if angle_error < self.max_angular_vel * self.engine.deltaTime:
                self.angle = self.angle_target
        if abs(self.angle - self.angle_target) < 5:
            self.angle = self.angle_target

        # do player control

        err = math.dist((self.engine.px,self.engine.py), (-self.engine.targetpx,-self.engine.targetpy))
        snapped = False
        if err < (400 * self.engine.deltaTime):
            self.engine.px = -self.engine.targetpx
            self.engine.py = -self.engine.targetpy
            snapped = True
        else:
            self.engine.px += 400 * math.sin(self.angle * (math.pi / 180)) * self.engine.deltaTime
            self.engine.py += 400 * math.cos(self.angle * (math.pi / 180)) * self.engine.deltaTime

        if err>(2000 * self.engine.deltaTime) and not snapped:
            o = self.engine.targetpx+self.engine.px
            a = self.engine.targetpy+self.engine.py
            angle = math.atan2(o,a)
            self.set_new_angle(angle*(180/math.pi)-180)


        rect = Rect(surf.get_rect().centerx - self.sprite.get_width() / 2,
                    surf.get_rect().centery - self.sprite.get_height() / 2, self.sprite.get_width(),
                    self.sprite.get_height())

        rotangle = 0
        if self.target:
            rotangle = self.targetAngle()
        else:
            rotangle = self.angle
        rotated_image, rect = rot_center(self.sprite, rect, rotangle)





        surf.blit(rotated_image, rect)

    def set_new_angle(self, angle):
        self.angle_target = angle % 360

    def targetAngle(self) -> float:

        playerpos = (-self.engine.px + self.engine.surface.get_width() / 2,
                           -self.engine.py + self.engine.surface.get_height() / 2)

        o = self.target.x- playerpos[0]
        a =  self.target.y - playerpos[1]
        angle = math.atan2(o, a)
        return (angle * (180 / math.pi) - 180) % 360

    def distance_to(self, object: Object) -> float:
        return math.dist(
            (-self.engine.px + self.engine.surface.get_width() / 2, -self.engine.py + self.engine.surface.get_height() / 2),
            (object.x, object.y))

