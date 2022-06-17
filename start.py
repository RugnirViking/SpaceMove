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
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    d_info = pygame.display.Info()
    screen_width, screen_height = d_info.current_w, d_info.current_h
    # Set up the window
    flags = pygame.NOFRAME | DOUBLEBUF
    windowSurface = pygame.display.set_mode((screen_width, screen_height), flags)
    pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP,MOUSEBUTTONDOWN,MOUSEBUTTONUP,MOUSEMOTION])
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
            new = handler.handle_events(event)
            if isinstance(new,BaseEventHandler):
                handler = new

        do_draw(surface,handler)


#Draw the window onto the screen
def do_draw(surf,handler:BaseEventHandler):
    pygame.draw.rect(surf,(0,0,0),pygame.Rect(0,50,surf.get_width(),surf.get_height()-50))
    handler.on_render(surf)

    pygame.display.flip()


if __name__ == "__main__":
    setup()
