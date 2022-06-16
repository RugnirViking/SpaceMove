import sys
import pygame

from colors import WHITE
from engine import Engine
from input_handlers import EventHandler


class MainMenuHandler(EventHandler):

    def __init__(self, engine: Engine,surf: pygame.Surface):
        super().__init__(engine)

        self.titletext = self.engine.smallfont.render('Asteroid Mining Ltd.', True, WHITE)
        self.textRect = self.titletext.get_rect()
        self.textRect.centerx = surf.get_rect().centerx
        self.textRect.centery = surf.get_rect().centery

    def on_render(self, surf) -> None:
        #self.engine.draw(surf)

        surf.blit(self.titletext,self.textRect)

    def ev_keydown(self, key, event: pygame.event):
        if key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
