import random

import pygame


class DamageText():
    def __init__(self, x, y, text, color, font):
        self.x = x
        self.y = y
        self.dx = random.randrange(-20, 20)
        self.dy = 0

        self.text = font.render(str(text), True, color)
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
        self.text.set_alpha(255-self.timer*255)
        surface.blit(self.text, (self.x, self.y))
