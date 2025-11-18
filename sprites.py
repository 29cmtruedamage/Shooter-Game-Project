import pygame
from random import randint


class Obstacles(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((randint(0, 300), randint(0, 100)))
        self.image.fill((255,0,0))
        self.rect = self.image.get_frect(topleft = pos)




