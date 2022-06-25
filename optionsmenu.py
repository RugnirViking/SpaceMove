import pygame
from pygame import Rect

import colors
from button import Button
from input_handlers import EventHandler
from slidercontrol import SliderControl


class OptionsMenu(EventHandler):

    def __init__(self, engine, surf: pygame.Surface,parent: EventHandler):
        super().__init__(engine)
        self.surf: pygame.SurfaceType = surf
        self.parent = parent

        self.buttons = []

        resumebuttonrect = Rect(0,0,200,50)
        resumebuttonrect.centerx = surf.get_rect().centerx
        resumebuttonrect.centery = surf.get_rect().height*3/4+100
        self.buttons.append(Button("Resume",self.engine.smallfont,resumebuttonrect,colors.WHITE,self.resume))

        self.mastervolumeslider = SliderControl(500,100,400,50,"Master Volume",colors.NEONGREEN,value=self.engine.mastervolume)
        self.musicvolumeslider = SliderControl(500,200,400,50,"Music Volume",colors.NEONGREEN,value=self.engine.musicvolume)
        self.soundeffectvolumeslider = SliderControl(500,300,400,50,"Sound Effect Volume",colors.NEONGREEN,value=self.engine.sound_effect_volume)



    def resume(self, button):
        self.engine.surface.fill((0,0,0))
        self.engine.draw(self.engine.surface)
        return self.parent

    def on_render(self, surf) -> None:
        for button in self.buttons:
            button.draw(surf)
        self.mastervolumeslider.draw(surf,self.engine)
        self.musicvolumeslider.draw(surf,self.engine)
        self.soundeffectvolumeslider.draw(surf,self.engine)

    def ev_mouseup(self, pos, mouse_btn, event: pygame.event):
        if mouse_btn == pygame.BUTTON_LEFT:
            if self.mastervolumeslider.mouseup(pos):
                self.engine.mastervolume = self.mastervolumeslider.value
            if self.musicvolumeslider.mouseup(pos):
                self.engine.musicvolume = self.musicvolumeslider.value
            if self.soundeffectvolumeslider.mouseup(pos):
                self.engine.sound_effect_volume = self.soundeffectvolumeslider.value

            for button in self.buttons:
                a = button.mouseup(pos, mouse_btn)
                if a is not None:
                    return a

    def ev_mousedown(self, pos, button, event: pygame.event):
        # when the mouse is pressed, start a drag event if the mouse is over a slider
        if button == pygame.BUTTON_LEFT:
            self.mastervolumeslider.mousedown(pos)
            self.musicvolumeslider.mousedown(pos)
            self.soundeffectvolumeslider.mousedown(pos)

    def ev_mousemove(self, pos, event: pygame.event):
        self.mastervolumeslider.mousemove(pos)
        self.musicvolumeslider.mousemove(pos)
        self.soundeffectvolumeslider.mousemove(pos)

    def ev_keydown(self, key, event: pygame.event):
        if key == pygame.K_ESCAPE:
            self.engine.surface.fill((0,0,0))
            self.engine.draw(self.engine.surface)
            return self.parent