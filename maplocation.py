import pygame

from engine import Engine
from utils import rot_center


class MapLocation:
    def __init__(self, x, y, filename, name, category,angle=0,scale=1):
        self.scaled = pygame.image.load(filename).convert_alpha()
        self.img = pygame.transform.scale(self.scaled, (int(self.scaled.get_width()*scale), int(self.scaled.get_height()*scale)))
        self.highlighted = self.img.copy()
        brighten = 64
        self.highlighted.fill((0, brighten, brighten), special_flags=pygame.BLEND_SUB)




        self.hovered = False
        self.category = category
        self.x = x
        self.y = y
        self.name = name
        self.angle = angle

    def mouse_over(self, mouse_pos):
        if self.get_rect().collidepoint(mouse_pos):
            self.hovered = True
            return
        self.hovered = False

    def draw(self, surf,engine):
        if self.hovered:
            # rotate then blit the image
            rotated_image, rrect = rot_center(self.highlighted, self.get_rect(), self.angle)
            surf.blit(rotated_image, rrect)

            # draw the name
            name_text = engine.sectorfont.render(self.name, True, (255, 255, 255))
            name_rect = name_text.get_rect()
            name_rect.centerx = self.x+self.img.get_width()/2+150
            name_rect.centery = self.y+75
            if surf.get_rect().contains(name_rect):
                surf.blit(name_text, name_rect)
            else:
                name_rect.centerx = self.x+self.img.get_width()/2+150
                name_rect.centery = self.y-75
                surf.blit(name_text, name_rect)

            # draw a line under the name
            pygame.draw.line(surf, (255, 255, 255), (name_rect.left,name_rect.bottom), (name_rect.right, name_rect.bottom), 1)
            # draw a line from the center to the bottom of the name
            pygame.draw.line(surf, (255, 255, 255), (self.x,self.y), (name_rect.left, name_rect.bottom), 1)


        else:
            # rotate then blit the image
            rotated_image, rrect = rot_center(self.img, self.get_rect(), self.angle)
            surf.blit(rotated_image, rrect)


    def get_rect(self):
        rect = self.img.get_rect()
        rect.centerx = self.x
        rect.centery = self.y
        return rect

    def get_center(self):
        return self.x+self.img.get_width()/2, self.y+self.img.get_height()/2

    def set_center(self,pos):
        self.x = pos[0] - self.img.get_width()/2
        self.y = pos[1] - self.img.get_height()/2

    def mouse_up(self, mouse_pos):
        if self.get_rect().collidepoint(mouse_pos):
            return True
        return False