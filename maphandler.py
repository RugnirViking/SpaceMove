import pygame
from pygame.font import Font

import colors
import utils
from engine import Engine
from input_handlers import EventHandler
from maplocation import MapLocation


class MapHandler(EventHandler):
    systemfont: pygame.font.FontType

    def __init__(self, engine: Engine, parent: EventHandler):
        super().__init__(engine)

        self.parent = parent
        # loads the map svg
        self.map = pygame.image.load('resources/img/system.svg')
        self.maprect = self.map.get_rect()
        self.maprect.top = 200
        self.map = self.map.convert_alpha()

        self.nebula = pygame.image.load('resources/img/mapnebula.png')

        self.systemfont = pygame.font.Font("resources/fonts/batmanfa.ttf", 44)
        self.subduedfont = pygame.font.Font("resources/fonts/Bungee-Regular.ttf", 24)

        self.locations = []
        self.locations.append(
            MapLocation(200, 550, 'resources/img/asteroidfield.svg', "12-2-AB", "Asteroid Field", angle=160, scale=0.8))
        self.locations.append(MapLocation(1100, 650, 'resources/img/asteroidfield.svg', "12-1-AB", "Asteroid Field", angle=0))
        self.locations.append(MapLocation(700, 300, 'resources/img/asteroidfield2.svg', "12-3-AB", "Asteroid Field", angle=90))
        self.locations.append(MapLocation(1200, 850, 'resources/img/asteroidfield3.svg', "12-4-AB", "Asteroid Field", angle=135))

        self.locations.append(MapLocation(220, 850, 'resources/img/planet.svg', "12-PN-1", "Planet", angle=11))
        self.locations.append(MapLocation(1100, 305, 'resources/img/planet.svg', "12-PN-2", "Planet", angle=130))
        self.locations.append(MapLocation(715, 1010, 'resources/img/planet.svg', "12-PN-3", "Planet", angle=22))

        self.selected = None

    def ev_mousemove(self, pos, event: pygame.event):
        for location in self.locations:
            location.mouse_over(pos)

    def ev_mouseup(self, pos, mouse_btn, event: pygame.event):
        for location in self.locations:
            if location.mouse_up(pos):
                self.selected = location

    def on_render(self, surf) -> None:

        surf.fill(colors.BLACK)
        surf.blit(self.nebula, (0, self.engine.surface.get_height() - self.nebula.get_height()))
        pygame.draw.rect(surf, colors.WHITE,
                         pygame.Rect(-1, self.engine.surface.get_height() - self.nebula.get_height(),
                                     self.nebula.get_width(), self.nebula.get_height() + 1), 1)
        pygame.draw.rect(surf, colors.WHITE,
                         pygame.Rect(-1, -1,
                                     self.nebula.get_width(),
                                     self.engine.surface.get_height() - self.nebula.get_height() + 1), 1)

        surf.blit(self.map, self.maprect)

        self.engine.Render_Text(f"SYSTEM 12-S \"Beta Cepheles\"", self.systemfont, colors.WHITE, (55, 55), surf=surf)

        for location in self.locations:
            location.draw(surf, self.engine)

        # update delta time so we don't get big jumps when unpausing

        self.engine.clock.tick()
        t = pygame.time.get_ticks()
        # deltaTime in seconds.
        self.engine.deltaTime = (t - self.engine.getTicksLastFrame) / 1000.0
        self.engine.getTicksLastFrame = t

        # draw the selected location larger and on the right of the screen
        if self.selected:
            # scale up the image
            scalerect = self.selected.get_rect()
            scalerect.center = (self.engine.surface.get_width()-235,
                                170)

            surf.blit(self.selected.scaled, scalerect)
            # draw the name of the location
            self.engine.Render_Text(self.selected.name, 
                                    self.systemfont, 
                                    colors.WHITE, 
                                    (self.nebula.get_width() + (self.engine.surface.get_width() - self.nebula.get_width()) / 2,
                                    355), surf=surf, centered=True)
            # draw the category of the location
            self.engine.Render_Text(f"Unclassified {self.selected.category}",
                                    self.subduedfont,
                                    colors.DARKGREY,
                                    (self.nebula.get_width() + (
                                                self.engine.surface.get_width() - self.nebula.get_width()) / 2,
                                     400), surf=surf, centered=True)
            
            
        pygame.draw.rect(surf, colors.WHITE,(self.nebula.get_width()+25,25,self.engine.surface.get_width() -self.nebula.get_width()- 50,300),1)

        
        
    def ev_keydown(self, key, event: pygame.event):
        if key == pygame.K_ESCAPE:
            return self.parent
