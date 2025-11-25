
import pygame
from globals import SCRREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE


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
