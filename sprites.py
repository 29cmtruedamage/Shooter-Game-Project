import pygame
from random import randint
from os.path import join
from math import degrees, atan2
SCRREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 64

#Class stand for every tile in the underground. If map is 2x2, there are 4 tile classes
class TileSprites(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(topleft = pos)
        self.type = 'tile'

#Class represents all obstacles like trees, rocks etc
class Obstacles(pygame.sprite.Sprite):
    def __init__(self, pos, image, groups):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_frect(topleft = pos)
        self.type = 'obstacle'

class Gun(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.player = player
        self.player_dir = pygame.Vector2(0,1)
        self.distance = 100
        self.gun_surf = pygame.image.load(join('images', 'gun', 'gun.png')).convert_alpha()
        self.image = self.gun_surf
        self.rect = self.image.get_frect(center = self.player.rect.center + self.player_dir * self.distance)
        self.type = 'gun'

    def get_direction(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        default_pos = pygame.Vector2(SCRREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.player_dir = (mouse_pos - default_pos).normalize()

    def rotate_gun(self):
        angle = degrees(atan2(self.player_dir.x, self.player_dir.y)) - 90
        if self.player_dir.x > 0.5: 
            self.image = pygame.transform.rotozoom(self.gun_surf, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.gun_surf, angle*-1, 1)
            self.image = pygame.transform.flip(self.image, False, True)

    def update(self, _):
        self.get_direction()
        self.rotate_gun()
        self.rect.center = self.player.rect.center + self.distance * self.player_dir

    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.player = player
        self.player_dir = pygame.Vector2(0,1)
        self.distance = 160
        self.gun_surf = pygame.image.load(join('images', 'gun', 'bullet.png')).convert_alpha()
        self.image = self.gun_surf
        self.rect = self.image.get_frect(center = self.player.rect.center + self.player_dir * self.distance)
        self.type = 'bullet'

    def get_direction(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        default_pos = pygame.Vector2(SCRREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.player_dir = (mouse_pos - default_pos).normalize()

    def rotate_gun(self):
        angle = degrees(atan2(self.player_dir.x, self.player_dir.y)) - 90
        if self.player_dir.x > 0.5: 
            self.image = pygame.transform.rotozoom(self.gun_surf, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.gun_surf, angle*-1, 1)
            self.image = pygame.transform.flip(self.image, False, True)

    def update(self, _):
        self.get_direction()
        self.rotate_gun()
        self.rect.center = self.player.rect.center + self.distance * self.player_dir

#Class is a group, like a list, in which all classes which can be seen are in, like player, tiles, obst.
# We have to add them all up in this class, to manage the screening of all instances/Objects in the game
# with certain structure and logic
class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen_copy = pygame.display.get_surface()
        self.direction = pygame.Vector2(0,0)
    
    #@Override
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

