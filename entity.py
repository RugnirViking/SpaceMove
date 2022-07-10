import math
import random

import pygame

from damagetext import DamageText
from object import Object
from utils import rot_center, ANGULAR_VELOCITY, PAR_SPREAD

from AI import EnemyAI, AI


# something with a
class Entity(Object):
    sprite: pygame.SurfaceType

    def __init__(self, image, x, y, fac,name, engine,ai: AI,hull,speed=200):
        super().__init__(image, x, y, fac,name)
        self.ai=ai

        self.ai.entity = self
        self.angle = -90
        self.angle_target = 0.0
        self.engine = engine
        self.loadcheck = False
        self.target_sprite = self.sprite.copy().convert_alpha()
        self.hull=hull
        # scale the target sprite so it fits into a 100x100 box while keeping its aspect ratio
        if self.target_sprite.get_width()>self.target_sprite.get_height():
            self.target_sprite = pygame.transform.scale(self.target_sprite, (100, int(100 * self.target_sprite.get_height() / self.target_sprite.get_width())))
        else:
            self.target_sprite = pygame.transform.scale(self.target_sprite, (int(100 * self.target_sprite.get_width() / self.target_sprite.get_height()), 100))
        #self.target_sprite = pygame.transform.scale(self.target_sprite, (int(self.target_sprite.get_width() * 0.5), int(self.target_sprite.get_height() * 0.5)))
        brighten = 255
        self.target_sprite.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD)
        self.lastrect = None
        self.snapped=False
        self.speed=speed
        self.hull = 100.0
        self.max_hull = 100.0
        self.radius = self.sprite.get_width() // 2

    def die(self):
        # release a large burst of particles
        for i in range(0, 100):
            pos = (self.x+self.engine.player.x,self.y+self.engine.player.y)
            if random.random()>0.5:
                grey = random.randint(0, 255)
                self.engine.particlemanager.add_particle([pos[0], pos[1]],
                                                         [random.randint(-500, 500), random.randint(-500, 500)],
                                                         (255, grey, 0), random.randint(3, 5), random.random() * 0.2 + 0.2, 0)
            else:

                grey = random.randint(0, 255)
                self.engine.particlemanager.add_particle([pos[0], pos[1]],
                                                         [random.randint(-500, 500), random.randint(-500, 500)],
                                                         (grey, grey, grey), random.randint(3, 5), random.random() * 0.2 + 0.2, 0)

    def take_damage(self, damage):
        self.hull -= damage
        if self.hull <= 0:
            self.dead = True
            self.die()
        else:
            pos = (self.x+self.engine.player.x,self.y+self.engine.player.y)
            self.engine.damagetext.append(
                DamageText(pos[0],pos[1],f"-{round(damage)}", (255, 180, 80), self.engine.damagefont))
            # release a burst of particles
            for i in range(10):
                grey = random.randint(128, 255)
                self.engine.particlemanager.add_particle([pos[0], pos[1]],
                                                         [random.randint(-500, 500), random.randint(-500, 500)],
                                                         (255, 255, 255), random.randint(3, 5), random.random()*0.2 + 0.2, 0)

    def is_on_screen(self, surf: pygame.SurfaceType) -> bool:
        return self.lastrect.colliderect(surf.get_rect())

    def dist_to_player(self):
        return self.engine.distance_to_entity(self.engine.player, self.x, self.y)

    def collision_radius(self) -> int:
        return max(self.sprite.get_width(), self.sprite.get_height()) // 2

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
        if abs(ang) < ANGULAR_VELOCITY * self.engine.deltaTime:
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

            width, height = self.engine.surface.get_size()
            if random.random() > 0.5:
                color = (255,random.randrange(0,255),0)
                self.engine.particlemanager.add_particle(
                    [self.x+self.engine.player.x, self.y+self.engine.player.y],
                    [400 * math.sin((self.angle + random.randrange(-PAR_SPREAD, PAR_SPREAD, 1)) * (math.pi / 180)),
                     400 * math.cos((self.angle + random.randrange(-PAR_SPREAD, PAR_SPREAD, 1)) * (math.pi / 180))], color,
                    random.randint(3, 5), random.random() + 1, 0
                )

        if err > (2000 * self.engine.deltaTime) and not snapped:
            o = self.ai.targetpos[0] - self.x
            a = self.ai.targetpos[1] - self.y
            angle = math.atan2(o, a)
            self.angle_target = (angle * (180 / math.pi) - 180) % 360


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

    def get_rect(self) -> pygame.rect.RectType:
        return self.lastrect

    def out_of_bounds(self):
        return abs(self.x) > 2730 or abs(self.y) > 1330