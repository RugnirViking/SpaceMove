import pygame, sys, os
from pygame.locals import *

from engine import Engine
from input_handlers import BaseEventHandler
from mainmenuhandler import MainMenuHandler

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
    # start the game on the main menu
    handler = MainMenuHandler(engine,surface)

    # Run the game loop
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            handler.handle_events(event)

        do_draw(surface,handler)


#Draw the window onto the screen
def do_draw(surf,handler:BaseEventHandler):
    surf.fill((0,0,0))

    handler.on_render(surf)

    pygame.display.flip()


if __name__ == "__main__":
    setup()
