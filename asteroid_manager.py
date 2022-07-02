import pygame

from utils import rot_center


class AsteroidManager():
    def __init__(self):

        rocks = ["resources/img/stone1.png", "resources/img/stone2.png", "resources/img/stone3.png",
                 "resources/img/stone4.png", "resources/img/stone5.png", "resources/img/stone6.png",
                 "resources/img/stone7.png", "resources/img/stone8.png", "resources/img/stone9.png"]
        rockimgs = []
        for x in rocks:
            sprite = pygame.image.load(x).convert_alpha()
            self.rotations = []
            for i in range(180):
                self.rotations.append(rot_center(sprite.convert_alpha(), sprite.get_rect(), i * 2))
            rockimgs.append(self.rotations)
        self.rockimgs = rockimgs
