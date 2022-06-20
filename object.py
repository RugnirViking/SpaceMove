import pygame


class Object():
    sprite: pygame.SurfaceType

    def __init__(self, image, x, y,fac):
        self.x=x
        self.y=y
        self.sprite = pygame.image.load(image).convert_alpha()
        width, height = self.sprite.get_width(), self.sprite.get_height()  # get size
        self.sprite = pygame.transform.scale(self.sprite, (int(width*fac), int(height*fac)))
        self.dead = False

    def draw(self,surf:pygame.SurfaceType,px,py):

        rect:pygame.rect.RectType = self.sprite.get_rect()
        rect.centerx = self.x+px
        rect.centery = self.y+py

        if rect.colliderect(surf.get_rect()):
            surf.blit(self.sprite,rect)
            return 1
        else:
            return 0