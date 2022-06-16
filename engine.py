import sys

from input_handlers import BaseEventHandler
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
        self.logger = Logger()
        #Set up fonts
        self.smallfont = pygame.font.SysFont(None, 48)

        self.logger.log("Engine load complete")

    def draw(self,surf) -> None:
        pass
