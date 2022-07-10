import pygame

from AI import AI
from entity import Entity
import random

from utils import rot_center


class RockAI:
    # moves in a random direction, spinning at a particular speed
    def __init__(self, entity: Entity):
        self.entity = entity
        self.vel = [random.randrange(-100,100),random.randrange(-100,100)]
        self.angular_vel = random.randint(50, 180)
        if random.random()>0.5:
            self.angular_vel *= -1
        self.look_angle = 0

    def update(self):
        self.look_angle = self.entity.angle

    def retarget(self,b):
        pass

    def dist_to_player(self):
        return self.entity.dist_to_player()

class Asteroid(Entity):
    def __init__(self, x, y, fac, name, engine,asteroid_manager):
        rocks = [0,1,2,3,4,5,6,7,8]
        img = random.choice(rocks)
        self.ai = RockAI(engine)
        self.rotations = asteroid_manager.rockimgs[img]
        self.sprite = self.rotations[0][0]
        super().__init__("skip", x, y, fac, name, engine, self.ai,100)
        self.width, self.height = self.sprite.get_width(), self.sprite.get_height()  # get size



    def update(self, dt):
        self.angle = self.angle + self.ai.angular_vel * dt
        self.x = self.x + self.ai.vel[0] * dt
        self.y = self.y + self.ai.vel[1] * dt

        self.do_movement(self.engine.surface, 0, 0)
        self.ai.update()

    def do_movement(self, surf, px, py):
        pass

    def draw(self, surf: pygame.SurfaceType, px, py):
        self.update(self.engine.deltaTime)

        # draw the asteroid at the correct angle
        rect: pygame.rect.RectType = self.rotations[int(self.angle / 2) % 180][1]
        rect.centerx = self.x + px
        rect.centery = self.y + py
        self.lastrect = rect
        if rect.colliderect(surf.get_rect()):
            surf.blit(self.rotations[int(self.angle / 2) % 180][0], rect)

            return 1
        else:
            # we are cunting fucking shitty little bastard fucker out of the motherfucking screen
            if abs(self.x)>2730*2 or abs(self.y)>1330*2:
                while True:
                    candidate_position = [random.randrange(-2730*2,2730*2), random.randrange(-1330*2,1330*2)]
                    rect: pygame.rect.RectType = self.rotations[int(self.angle / 2) % 180][1]
                    rect.centerx = candidate_position[0] + px
                    rect.centery = candidate_position[1] + py
                    self.lastrect = rect
                    if not rect.colliderect(surf.get_rect()):
                        if abs(candidate_position[0])>2730 or abs(candidate_position[1])>1330:
                            self.x = candidate_position[0]
                            self.y = candidate_position[1]
                            break
            return 0