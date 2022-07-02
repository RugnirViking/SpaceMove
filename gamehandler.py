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
        keys = pygame.key.get_pressed()
        self.engine.gameUIcontroller.selections[1] = keys[pygame.K_2]


    def ev_keydown(self, key, event: pygame.event):
        if key == pygame.K_ESCAPE:
            return PauseMenuHandler(self.engine,self)
        if key == pygame.K_SPACE:
            if self.engine.player.distance_to(self.engine.station) < 250:
                return DockMenuHandler(self.engine,self)
        if key == pygame.K_m:
            return MapHandler(self.engine,self)
        if key == pygame.K_1:
            self.engine.gameUIcontroller.selections[0] = not self.engine.gameUIcontroller.selections[0]
        if key == pygame.K_3:
            self.engine.gameUIcontroller.selections[2] = not self.engine.gameUIcontroller.selections[2]
        if key == pygame.K_4:
            self.engine.gameUIcontroller.selections[3] = not self.engine.gameUIcontroller.selections[3]
        if key == pygame.K_5:
            self.engine.gameUIcontroller.selections[4] = not self.engine.gameUIcontroller.selections[4]
        if key == pygame.K_l:
            self.engine.player.mouselookmode = not self.engine.player.mouselookmode

    def ev_mousemove(self, pos, event: pygame.event):
        pass

    def ev_mouseup(self, pos, mouse_btn, event: pygame.event):
        self.engine.mouseup(pos,mouse_btn,event)
