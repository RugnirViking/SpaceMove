import math

import pygame


class Projectile():
    def __init__(self, x, y, vx, vy, img, color, target=None,onhit=None):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.angle = math.atan2(vy, vx)
        self.img = pygame.image.load(img).convert_alpha()
        self.color = color
        self.dead = False
        self.target = target
        self.onhit = onhit

    def update(self, dt,engine):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.angle = math.atan2(self.vy, self.vx)
        if not engine.is_on_screen(self.x,self.y) and not self.target:
            self.dead = True

        if self.target:
            if self.target.dead:
                self.dead = True
            else:
                distance = math.sqrt((self.x+engine.width/2-self.target.x)**2 + (self.y+engine.height/2-self.target.y)**2)
                if distance < self.target.radius:
                    self.dead = True
                    if self.onhit:
                        self.onhit(self.target)


    def draw(self, surf, engine):
        tempsurf = pygame.Surface((self.img.get_width(), self.img.get_height()))
        tempsurf.set_alpha(0)
        tempsurf.blit(self.img, (0, 0))
        tempsurf = pygame.transform.rotate(tempsurf, -math.degrees(self.angle))

        rot_image = pygame.transform.rotozoom(self.img, -math.degrees(self.angle), 1)
        surf.blit(rot_image, engine.world_to_screen((self.x-tempsurf.get_width()/2, self.y-tempsurf.get_height()/2)))

class ProjectileManager:
    def __init__(self,engine):
        self.projectiles = []
        self.engine = engine

    def update(self, dt):
        for projectile in self.projectiles:
            projectile.update(dt,self.engine)

            if projectile.dead:
                self.projectiles.remove(projectile)

    def draw(self, surf):
        for projectile in self.projectiles:
            projectile.draw(surf, self.engine)

    def add_projectile(self, x, y, vx, vy, img, color,target=None,onhit=None):
        self.projectiles.append(Projectile(x, y, vx, vy, img, color,target,onhit))