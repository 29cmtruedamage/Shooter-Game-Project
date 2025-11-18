import pygame
from os.path import join
import math
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player', 'down', '3.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        
        self.direction = pygame.Vector2(0, 0)
        self.speed = 520

    def input_handling(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a]) 
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        if self.direction.x != 0 and self.direction.y != 0:
            self.direction.x *= math.sqrt(0.5)
            self.direction.y *= math.sqrt(0.5) 
        # -> a^2 + b^2 = c^2, hat endlich mal was gebracht im Leben :)
        # -> sqrt(0.5)^2 * sqrt(0.5)^2 = 1 -> normiert

    def movement_handling(self, delta_t):
        self.rect.center += self.direction * self.speed * delta_t

    def update(self, delta_t):
        self.input_handling()
        self.movement_handling(delta_t)
        