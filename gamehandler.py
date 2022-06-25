import sys
import pygame
from pygame import Rect

import colors
from PauseMenuHandler import PauseMenuHandler
from button import Button
from colors import WHITE
from dockmenuhandler import DockMenuHandler
from engine import Engine
from input_handlers import EventHandler
from maphandler import MapHandler


class GameHandler(EventHandler):

    def __init__(self, engine: Engine,surf: pygame.Surface):
        super().__init__(engine)



    def on_render(self, surf) -> None:
        self.engine.draw(surf)


    def ev_keydown(self, key, event: pygame.event):
        if key == pygame.K_ESCAPE:
            return PauseMenuHandler(self.engine,self)
        if key == pygame.K_SPACE:
            if self.engine.player.distance_to(self.engine.station) < 250:
                return DockMenuHandler(self.engine,self)
        if key == pygame.K_m:
            return MapHandler(self.engine,self)
        if key == pygame.K_r:
            self.engine.player.reset()

    def ev_mousemove(self, pos, event: pygame.event):
        pass

    def ev_mouseup(self, pos, mouse_btn, event: pygame.event):
        self.engine.mouseup(pos,mouse_btn,event)
