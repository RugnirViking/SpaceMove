import pygame, sys, os
from pygame.locals import *

from engine import Engine

os.environ['SDL_VIDEO_CENTERED'] = '1'

VERSIONMAJOR = 0
VERSIONMINOR = 1

def setup():
    # Set up pygame
    pygame.init()
    d_info = pygame.display.Info()
    screen_width, screen_height = d_info.current_w, d_info.current_h
    # Set up the window
    windowSurface = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
    pygame.display.set_caption(f'Asteroid Mining Ltd. V{VERSIONMAJOR}.{VERSIONMINOR}')
    engine:Engine = Engine(windowSurface)
    mainloop(windowSurface,engine)

def mainloop(surface,engine):
    # Run the game loop
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        engine.handle_events(events)


        do_draw(surface,engine)


#Draw the window onto the screen
def do_draw(surf,engine):
    surf.fill((0,0,0))

    engine.draw(surf)

    pygame.display.flip()


if __name__ == "__main__":
    setup()
