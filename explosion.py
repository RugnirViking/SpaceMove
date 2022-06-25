import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y,delay=0):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 0
        self.active = True

        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"resources/img/exp{num}.png")
            img = pygame.transform.scale(img, (100, 100))
            self.images.append(img)

        self.index = 0
        self.image = pygame.Surface((10,10))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0
        self.delay = delay
        self.delayed = True

    def update(self, dt):
        explosion_speed = 0.1
        #update explosion animation
        self.counter += 1*dt
        if self.counter>self.delay and self.delayed:
            self.delayed = False
            self.counter = 0
            self.image = self.images[self.index]

        if self.counter >= explosion_speed and self.index < len(self.images) - 1 and not self.delayed:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        #if the animation is complete, reset animation index
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.active = False

            self.kill()

    def draw(self, surface):
        if not self.delayed:
            surface.blit(self.image, self.rect)