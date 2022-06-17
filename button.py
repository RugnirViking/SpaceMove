from typing import Tuple, Callable, Any

import pygame
from pygame.font import FontType
from pygame.rect import RectType


class Button:
    on_pressed: Callable
    color: Tuple[int, int, int]
    font: FontType
    rect: RectType
    text: str
    hovered: bool

    def __init__(self, text: str, font: FontType, rect: RectType, color: Tuple[int, int, int], on_pressed: Callable):
        self.text = text
        self.rect = rect
        self.font = font
        self.color = color
        self.hovered = False
        self.on_pressed = on_pressed

        self.titletext = self.font.render(text, True, color)
        self.textRect = self.titletext.get_rect()
        self.textRect.centerx = rect.centerx
        self.textRect.centery = rect.centery

    def mouseupdate(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            self.hovered = True
        else:
            self.hovered = False

    def draw(self, surf):
        surf.blit(self.titletext, self.textRect)
        if self.hovered:
            pygame.draw.rect(surf, self.color, self.rect, 4)
        else:
            pygame.draw.rect(surf, self.color, self.rect, 2)

    def mouseup(self, pos, button):
        if self.rect.collidepoint(pos[0], pos[1]):
            return self.on_pressed(button)
