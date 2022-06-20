import sys
import pygame
from pygame import Rect

import colors
from button import Button
from colors import WHITE
from engine import Engine
from input_handlers import EventHandler



class PauseMenuHandler(EventHandler):

    def __init__(self, engine: Engine, gamehandler):
        super().__init__(engine)
        self.gamehandler = gamehandler
        self.buttons = []
        surf = self.engine.surface
        startbuttonrect = Rect(0,0,200,50)
        startbuttonrect.centerx = surf.get_rect().centerx
        startbuttonrect.centery = surf.get_rect().height/4+100
        self.buttons.append(Button("Resume",self.engine.smallfont,startbuttonrect,colors.WHITE,self.resume))

        startbuttonrect2 = Rect(0,0,200,50)
        startbuttonrect2.centerx = surf.get_rect().centerx
        startbuttonrect2.centery = surf.get_rect().height/4+200
        self.buttons.append(Button("Quit",self.engine.smallfont,startbuttonrect2,colors.WHITE,self.quit))

        self.titletext = self.engine.titlefont.render('PAUSED', True, WHITE)
        self.textRect = self.titletext.get_rect()
        self.textRect.centerx = surf.get_rect().centerx
        self.textRect.centery = surf.get_rect().height/4


    def resume(self, button):
        return self.gamehandler

    def quit(self, button):
        pygame.quit()
        sys.exit()

    def on_render(self, surf) -> None:
        rect = Rect(0,0,350,500)
        rect.centerx = surf.get_width()/2
        rect.top = surf.get_rect().height/4-75

        pygame.draw.rect(surf,(0,0,0),rect)

        surf.blit(self.titletext,self.textRect)
        for button in self.buttons:
            button.draw(surf)

        # update delta time so we don't get big jumps when unpausing

        self.engine.clock.tick()
        t = pygame.time.get_ticks()
        # deltaTime in seconds.
        self.engine.deltaTime = (t - self.engine.getTicksLastFrame) / 1000.0
        self.engine.getTicksLastFrame = t


    def ev_keydown(self, key, event: pygame.event):
        pass

    def ev_mousemove(self, pos, event: pygame.event):
        for button in self.buttons:
            button.mouseupdate(pos)

    def ev_mouseup(self, pos, mouse_btn, event: pygame.event):
        for button in self.buttons:
            a = button.mouseup(pos, mouse_btn)
            if a is not None:
                return a
