import sys
import pygame
from pygame import Rect

import colors
from button import Button
from colors import WHITE
from engine import Engine
from gamehandler import GameHandler
from input_handlers import EventHandler


class MainMenuHandler(EventHandler):

    def __init__(self, engine: Engine,surf: pygame.Surface):
        super().__init__(engine)

        self.titletext = self.engine.titlefont.render('Asteroid Mining Ltd.', True, WHITE)
        self.textRect = self.titletext.get_rect()
        self.textRect.centerx = surf.get_rect().centerx
        self.textRect.centery = surf.get_rect().height/4

        self.buttons = []
        startbuttonrect = Rect(0,0,200,50)
        startbuttonrect.centerx = surf.get_rect().centerx
        startbuttonrect.centery = surf.get_rect().height/4+100
        self.buttons.append(Button("Start",self.engine.smallfont,startbuttonrect,colors.WHITE,self.start))

    def start(self, button):
        return GameHandler(self.engine,self.engine.surface)

    def on_render(self, surf) -> None:
        #self.engine.draw(surf)

        surf.blit(self.titletext,self.textRect)

        for button in self.buttons:
            button.draw(surf)

    def ev_keydown(self, key, event: pygame.event):
        if key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    def ev_mousemove(self, pos, event: pygame.event):
        for button in self.buttons:
            button.mouseupdate(pos)

    def ev_mouseup(self, pos, mouse_btn, event: pygame.event):
        for button in self.buttons:
            return button.mouseup(pos, mouse_btn)
