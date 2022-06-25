import math

import pygame

from object import Object
from utils import rot_center, ANGULAR_VELOCITY

from AI import EnemyAI, AI


# something with a
class Entity(Object):
    sprite: pygame.SurfaceType

    def __init__(self, image, x, y, fac,name, engine,ai: AI,speed=200):
        super().__init__(image, x, y, fac,name)
        self.ai=ai

        self.ai.entity = self
        self.angle = -90
        self.angle_target = 0.0
        self.engine = engine
        self.loadcheck = False
        self.target_sprite = self.sprite.copy().convert_alpha()
        brighten = 255
        self.target_sprite.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD)
        self.lastrect = None
        self.snapped=False
        self.speed=speed
        self.hull = 100.0
        self.max_hull = 100.0

    def dist_to_player(self):
        return self.engine.distance_to_entity(self.engine.player, self.x, self.y)

    def draw(self, surf: pygame.SurfaceType, px, py):

        if self.loadcheck:
            self.do_movement(surf, px, py)
        else:
            self.loadcheck = True

        rect: pygame.rect.RectType = self.sprite.get_rect()
        rect.centerx = self.x + px
        rect.centery = self.y + py
        rotated_image, rrect = rot_center(self.sprite, rect, self.ai.look_angle)
        self.lastrect = rrect

        if rect.colliderect(surf.get_rect()):
            surf.blit(rotated_image, rrect)
            return 1
        else:
            return 0

    def move(self,speed,angle):
        xmove = math.sin(angle * (math.pi / 180)) * speed * self.engine.deltaTime
        ymove = math.cos(angle * (math.pi / 180)) * speed * self.engine.deltaTime
        self.x += xmove
        self.y += ymove

    def do_movement(self, surf, px, py):
        self.angle = self.angle % 360

        angle_error = (self.angle - self.angle_target) % 360

        if 0 < angle_error <= 180:
            self.angle -= ANGULAR_VELOCITY * self.engine.deltaTime
            if angle_error < ANGULAR_VELOCITY * self.engine.deltaTime:
                self.angle = self.angle_target
        elif angle_error > 180:
            self.angle += ANGULAR_VELOCITY * self.engine.deltaTime
            if angle_error < ANGULAR_VELOCITY * self.engine.deltaTime:
                self.angle = self.angle_target
        self.ai.retarget(True)
        ang = self.angle - self.angle_target % 360
        if abs(ang) < 5:
            self.angle = self.angle_target

            snapped  =False
            err = math.dist((self.x, self.y), (self.ai.targetpos[0], self.ai.targetpos[1]))
            if err < (200 * self.engine.deltaTime):
                self.x = self.ai.targetpos[0]
                self.y = self.ai.targetpos[1]
                snapped = True
            else:
                self.x -= self.speed * math.sin(self.angle * (math.pi / 180)) * self.engine.deltaTime
                self.y -= self.speed * math.cos(self.angle * (math.pi / 180)) * self.engine.deltaTime

            if err > (2000 * self.engine.deltaTime) and not snapped:
                o = self.ai.targetpos[0] - self.x
                a = self.ai.targetpos[1] - self.y
                angle = math.atan2(o, a)
                self.set_new_angle(angle * (180 / math.pi) - 180)


        for entity in self.engine.objects:
            if isinstance(entity, Entity) and entity != self:
                dist = self.engine.distance_to_entity(entity, self.x,self.y)
                if dist<100:
                    # get angle between me and entity
                    o = entity.x - self.x
                    a = entity.y - self.y
                    orthangle = math.atan2(o, a)

                    # move away from entity
                    self.x -= 200 * (100-dist)/100 * math.sin(orthangle) * self.engine.deltaTime
                    self.y -= 200 * (100-dist)/100 * math.cos(orthangle) * self.engine.deltaTime


    def set_new_angle(self, angle):
        self.angle_target = angle % 360

    def get_rect(self) -> pygame.rect.RectType:
        return self.lastrect
