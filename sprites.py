import pygame
from random import randint
from pytmx import load_pygame


class TileSprites(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(topleft = pos)


class Obstacles(pygame.sprite.Sprite):
    def __init__(self, pos, image, groups):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_frect(topleft = pos)


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen_copy = pygame.display.get_surface()
        self.direction = pygame.Vector2(-1000, -1000)

    def custom_draw(self, player_vec):
        self.direction.x -= player_vec.x
        self.direction.y -= player_vec.y
        for sprite in self:
            self.screen_copy.blit(sprite.image, sprite.rect.topleft + self.direction)

