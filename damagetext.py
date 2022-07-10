import random

import pygame


class DamageText():
    def __init__(self, x, y, text, color, font):
        self.x = x
        self.y = y
        self.dx = random.randrange(-200, 200)
        self.dy = 100

        self.text = font.render(str(text), True, color)
        self.text_outline = font.render(str(text), True, (10, 10, 10))
        self.width = self.text.get_width()
        self.height = self.text.get_height()
        self.timer = 0
        self.active = True

    def update(self, dt):
        self.timer += dt
        if self.timer > 1:
            self.active = False
        self.dy-=9.81*dt*10
        self.y-=self.dy*dt
        self.x+=self.dx*dt

    def draw(self, surface):
        newsurf = pygame.Surface((self.width+4, self.height+4))
        newsurf.blit(self.text_outline, (0, 0))
        newsurf.blit(self.text_outline, (0, 4))
        newsurf.blit(self.text_outline, (4, 0))
        newsurf.blit(self.text_outline, (4, 4))

        newsurf.blit(self.text, (2,2))
        newsurf.set_alpha(255-self.timer*255)
        newsurf.set_colorkey((0, 0, 0))
        surface.blit(newsurf, (self.x, self.y))
