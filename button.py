from typing import Tuple

import pygame
from pygame.font import FontType
from pygame.rect import RectType


class Button:
    color: Tuple[int, int, int]
    font: FontType
    rect: RectType
    text: str

    def __init__(self, text: str, font: FontType, rect: RectType, color: Tuple[int, int, int]):
        self.text = text
        self.rect = rect
        self.font = font
        self.color = color

        self.titletext = self.font.render(text, True, color)
        self.textRect = self.titletext.get_rect()
        self.textRect.centerx = rect.centerx
        self.textRect.centery = rect.centery

    def draw(self, surf):
        surf.blit(self.titletext, self.textRect)
        pygame.draw.rect(surf, self.color, self.rect, 4)
