import math
from typing import TYPE_CHECKING

import pygame
from pygame import Rect

from colors import WHITE

if TYPE_CHECKING:
    from engine import Engine

ANGULAR_VELOCITY = 350

def rot_center(image, rect, angle):
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image,rot_rect

class Player():
    sprite: pygame.image
    angle: float
    angle_target: float

    def __init__(self,img_path,engine):
        self.angle = 0.0
        self.sprite = pygame.image.load(img_path).convert_alpha()
        self.angle_target = 0.0
        self.engine = engine
        width, height = self.sprite.get_width(), self.sprite.get_height()  # get size
        self.sprite = pygame.transform.scale(self.sprite, (int(width/4), int(height/4)))

    def draw(self,surf):
        self.angle = self.angle % 360

        angle_error = (self.angle - self.angle_target) % 360

        if 0<angle_error<180:
            self.angle-=ANGULAR_VELOCITY*self.engine.deltaTime
            if angle_error<ANGULAR_VELOCITY*self.engine.deltaTime:
                self.angle = self.angle_target
        elif angle_error>180:
            self.angle+=ANGULAR_VELOCITY*self.engine.deltaTime
            if angle_error<ANGULAR_VELOCITY*self.engine.deltaTime:
                self.angle = self.angle_target
        if abs(self.angle-self.angle_target)<5:
            self.angle = self.angle_target

        rect = Rect(surf.get_rect().centerx-self.sprite.get_width()/2,surf.get_rect().centery-self.sprite.get_height()/2,self.sprite.get_width(),self.sprite.get_height())
        rotated_image, rect = rot_center(self.sprite, rect, self.angle)

        surf.blit(rotated_image,rect)


    def set_new_angle(self, angle):
        self.angle_target = angle % 360