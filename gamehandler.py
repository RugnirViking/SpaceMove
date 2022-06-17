import sys
import pygame
from pygame import Rect

import colors
from button import Button
from colors import WHITE
from engine import Engine
from input_handlers import EventHandler


class GameHandler(EventHandler):

    def __init__(self, engine: Engine,surf: pygame.Surface):
        super().__init__(engine)

        self.titletext = self.engine.titlefont.render('Started!', True, WHITE)
        self.textRect = self.titletext.get_rect()
        self.textRect.centerx = surf.get_rect().centerx
        self.textRect.centery = surf.get_rect().height/4



    def on_render(self, surf) -> None:
        self.engine.draw(surf)


    def ev_keydown(self, key, event: pygame.event):
        if key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    def ev_mousemove(self, pos, event: pygame.event):
        pass

    def ev_mouseup(self, pos, mouse_btn, event: pygame.event):
        self.engine.mouseup(pos,mouse_btn,event)
