import sys
from logging import Logger
from typing import Optional, Any, Union

import pygame
from pygame.font import FontType
from pygame.ftfont import Font

from colors import WHITE


class Engine:
    textRect: pygame.rect
    smallfont: Union[Font, FontType]
    titletext: pygame.Surface

    logger: Logger

    def __init__(self,surf) -> None:
        #Set up fonts
        self.smallfont = pygame.font.SysFont(None, 48)
        self.titletext = self.smallfont.render('Asteroid Mining Ltd.', True, WHITE)
        self.textRect = self.titletext.get_rect()
        self.textRect.centerx = surf.get_rect().centerx
        self.textRect.centery = surf.get_rect().centery

        self.logger = Logger()

    def draw(self,surf) -> None:
        surf.blit(self.titletext,self.textRect)

    def handle_events(self,events) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()