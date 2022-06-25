import pygame
from pygame import Rect

import colors
from button import Button
from engine import Engine
from input_handlers import EventHandler


class DockMenuHandler(EventHandler):
    def __init__(self, engine: Engine, prev_handler: EventHandler):
        self.engine = engine
        self.prev_handler = prev_handler
        self.buttons = []
        surf = self.engine.surface
        startbuttonrect = Rect(0, 0, 200, 50)
        startbuttonrect.left = surf.get_rect().width - 300
        startbuttonrect.centery = surf.get_rect().height*3.25 / 4 + 100
        self.buttons.append(Button("Undock", self.engine.smallfont, startbuttonrect, colors.WHITE, self.undock))

    def undock(self, button):
        return self.prev_handler

    def on_render(self, surf) -> None:
        surf.fill((0, 0, 0))
        # draw a title that says "Dock"
        font = self.engine.titlefont
        text = font.render("Dock", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.centerx = surf.get_rect().centerx
        text_rect.centery = surf.get_rect().height / 16
        surf.blit(text, text_rect)

        for button in self.buttons:
            button.draw(surf)

        # update delta time so we don't get big jumps when unpausing

        self.engine.clock.tick()
        t = pygame.time.get_ticks()
        # deltaTime in seconds.
        self.engine.deltaTime = (t - self.engine.getTicksLastFrame) / 1000.0
        self.engine.getTicksLastFrame = t


    def ev_keydown(self, key, event: pygame.event):
        if key == pygame.K_ESCAPE:
            return self.prev_handler

    def ev_mousemove(self, pos, event: pygame.event):
        for button in self.buttons:
            button.mouseupdate(pos)


    def ev_mouseup(self, pos, mouse_btn, event: pygame.event):

        for button in self.buttons:
            a = button.mouseup(pos,mouse_btn)
            if isinstance(a, EventHandler):
                return a

