from __future__ import annotations

import sys
from typing import Optional, TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from engine import Engine


class BaseEventHandler:
    def handle_events(self, event: pygame.event) -> BaseEventHandler:
        """Handle an event and return the next active event handler."""
        state = self.dispatch(event)
        if isinstance(state, BaseEventHandler):
            return state
        return self

    def dispatch(self, event: pygame.event) -> Optional[BaseEventHandler]:
        return None

    def on_render(self, surf) -> None:
        raise NotImplementedError()

    def ev_quit(self, events) -> None:
        raise SystemExit()


class EventHandler(BaseEventHandler):
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self, event: pygame.event) -> BaseEventHandler:
        """Handle an event and return the next active event handler."""
        state = self.dispatch(event)
        if isinstance(state, BaseEventHandler):
            return state
        return self

    def dispatch(self, event: pygame.event) -> Optional[BaseEventHandler]:
        if event.type == pygame.KEYDOWN:
            return self.ev_keydown(event.key, event)
        if event.type == pygame.KEYUP:
            return self.ev_keyup(event.key, event)
        if event.type == pygame.MOUSEMOTION:
            return self.ev_mousemove(event.pos, event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.ev_mousedown(event.pos, event.button, event)
        if event.type == pygame.MOUSEBUTTONUP:
            return self.ev_mouseup(event.pos, event.button, event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def on_render(self, surf) -> None:
        self.engine.draw(surf)

    def ev_keydown(self, key, event: pygame.event):
        pass

    def ev_keyup(self, key, event: pygame.event):
        pass

    def ev_mousemove(self, pos, event: pygame.event):
        pass

    def ev_mousedown(self, pos, button, event: pygame.event):
        pass

    def ev_mouseup(self, pos, button, event: pygame.event):
        pass


class GameOverHandler(BaseEventHandler):
    pass
