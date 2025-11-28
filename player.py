import pygame
from os.path import join
from os import walk
import math
from globals import SCRREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, health, ammunition, obstacle_group, enemy_group):
        super().__init__(groups)
        self.all_movements = {'down': [], 'up': [], 'left': [], 'right': []}
        self.load_animations()
        self.image = self.all_movements['left'][0]
        self.pos = pos
        self.rect = self.image.get_frect(center = self.pos)
        self.obstacle_group = obstacle_group
        self.enemy_group = enemy_group
        self.direction = pygame.Vector2(0, 0)
        self.additional_speed = 520
        self.hitbox = self.rect.inflate(-55, -110)
        self.type = 'player'
        self.index = 0
        self.health = health
        self.ammunition = ammunition
        self.recovery_time = 200
        self.sprinting = False

        self.hit_sound = pygame.mixer.Sound(join('sound','hit_sound.mp3'))
        self.hit_sound.set_volume(1.5)

    #handles the keyboard input (WASD)
    def input_handling(self):
        keys = pygame.key.get_pressed()
        self.sprinting = int(keys[pygame.K_LSHIFT]) * 0.35
        self.direction.x = (int(keys[pygame.K_d]) - int(keys[pygame.K_a])) * (0.75 + self.sprinting)
        self.direction.y = (int(keys[pygame.K_s]) - int(keys[pygame.K_w])) * (0.75 + self.sprinting)

        if self.direction.x != 0 and self.direction.y != 0:
            self.direction.x *= math.sqrt(0.5)
            self.direction.y *= math.sqrt(0.5) 
            # -> a^2 + b^2 = c^2, hat endlich mal was gebracht im Leben :)
            # -> sqrt(0.5)^2 * sqrt(0.5)^2 = 1 -> normiert
            if self.direction.x > 0: self.animation_maker('right')
            if self.direction.x < 0: self.animation_maker('left')
        else:    
            if self.direction.x > 0: self.animation_maker('right')
            if self.direction.x < 0: self.animation_maker('left')
            if self.direction.y > 0: self.animation_maker('down')
            if self.direction.y < 0: self.animation_maker('up')
 
    #load all pictures of Player from the folder image/player
    def load_animations(self):
        for direction in self.all_movements.keys():
            for path, subfolder, files in walk(join('images', 'player', direction)): #walk return names of files in a list
                for file in files:
                    surf = pygame.image.load(join(path, file)).convert_alpha()
                    self.all_movements[direction].append(surf)
                    print(join(path, file))

    #animate the player based on the direction
    def animation_maker(self, state):
        self.index += 0.035 #Geschwindigkeit der Animation
        if self.sprinting:
            self.index += 0.02
        self.index %= 4     #Anzahl Bilder pro richtung
        self.image = self.all_movements[state][int(self.index)]

    #calculates the new position after imput handling
    def movement_handling(self, delta_t):
        self.hitbox.x += self.direction.x * self.additional_speed * delta_t
        self.collision_handling()
        self.hitbox.y += self.direction.y * self.additional_speed * delta_t
        self.collision_handling()
        self.rect.center = self.hitbox.center  

    def check_enemy_collision(self):
        self.recovery_time += 1
        for enemy in self.enemy_group:
            if self.recovery_time > 400: # You have 400ms to flee away from enemies
                if self.hitbox.colliderect(enemy.hitbox):
                    self.hit_sound.play()
                    self.health -= 1
                    self.recovery_time = 0

    #handles collision between player and obstacles
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
        self.check_enemy_collision()
        