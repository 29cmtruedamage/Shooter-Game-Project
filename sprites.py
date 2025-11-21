import pygame
from random import randint
from pytmx import load_pygame

SCRREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 64

class TileSprites(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(topleft = pos)
        self.type = 'tile'

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, pos, image, groups):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_frect(topleft = pos)
        self.type = 'obstacle'

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen_copy = pygame.display.get_surface()
        self.direction = pygame.Vector2(0,0)
        
    def draw(self, pos):
        self.direction.x = -(pos[0] -  SCRREEN_WIDTH / 2)
        self.direction.y = -(pos[1] - SCREEN_HEIGHT / 2)

        tiles = []
        objects = []
        for sprite in self:
            if sprite.type == 'tile': tiles.append(sprite)
            else: objects.append(sprite)
               
        tiles.sort(key = lambda sprite: sprite.rect.centery)
        objects.sort(key = lambda sprite: sprite.rect.centery)
        for sprite in tiles:
            self.screen_copy.blit(sprite.image, sprite.rect.topleft + self.direction)
        for sprite in objects:
            self.screen_copy.blit(sprite.image, sprite.rect.topleft + self.direction)

