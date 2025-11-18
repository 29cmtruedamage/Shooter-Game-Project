import pygame
from os.path import join
import math
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_group):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player', 'down', '3.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.obstacle_group = obstacle_group
        self.direction = pygame.Vector2(0, 0)
        self.speed = 520
        self.hitbox = self.rect.inflate(-55, 0)

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
        self.hitbox.x += self.direction.x * self.speed * delta_t
        self.collision_handling()
        self.hitbox.y += self.direction.y * self.speed * delta_t
        self.collision_handling()
        self.rect.center = self.hitbox.center  

    def collision_handling(self):
        for g in self.obstacle_group:
            if self.hitbox.colliderect(g.rect):
                
                if self.hitbox.right < g.rect.left + 20: self.hitbox.right = g.rect.left #links
                if self.hitbox.left > g.rect.right - 20: self.hitbox.left = g.rect.right #rechts
                if self.hitbox.bottom < g.rect.top + 20: self.hitbox.bottom = g.rect.top
                if self.hitbox.top > g.rect.bottom -20: self.hitbox.top = g.rect.bottom




    def update(self, delta_t):
        self.input_handling()
        self.movement_handling(delta_t)
        