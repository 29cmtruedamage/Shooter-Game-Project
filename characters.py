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
        
        #packs
        self.health = health
        self.ammunition = ammunition
        
        #recovery
        self.time_now = pygame.time.get_ticks() 
        self.recovery_time = 3000
        self.time_till_full_recovery = self.time_now + self.recovery_time 
        
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
                    
                    

    #animate the player based on the direction
    def animation_maker(self, state):
        #Geschwindigkeit der Animation
        if self.sprinting:
            self.index = int(pygame.time.get_ticks() / 60) % 4
        else:
            self.index = int(pygame.time.get_ticks() / 80) % 4     #Anzahl Bilder pro richtung
        self.image = self.all_movements[state][int(self.index)]

    #calculates the new position after imput handling
    def movement_handling(self, delta_t):
        self.hitbox.x += self.direction.x * self.additional_speed * delta_t
        self.collision_handling()
        self.hitbox.y += self.direction.y * self.additional_speed * delta_t
        self.collision_handling()
        self.rect.center = self.hitbox.center  

    def check_enemy_collision(self):
        self.time_now = pygame.time.get_ticks()
        for enemy in self.enemy_group:
            if self.time_now > self.time_till_full_recovery: # You have 400ms to flee away from enemies
                if self.hitbox.colliderect(enemy.hitbox):
                    self.hit_sound.play()
                    self.health -= 1
                    self.time_till_full_recovery = self.time_now + self.recovery_time

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
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self, frames, pos, player, groups, obstacle_group, bullet_group, hardMode):
        super().__init__(groups)
        self.frames = frames
        self.player = player
        self.obstacle_group = obstacle_group
        self.bullet_group = bullet_group
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_frect(center = pos)
        self.hitbox = self.rect.inflate(-20, -40)
        self.direction = pygame.Vector2()
        self.type = 'enemy'
        self.speed = 160
        if hardMode: self.speed = 220
        self.health = 1
        self.deat_sound = pygame.mixer.Sound(join('sound','death_sound.wav'))
        self.deat_sound.set_volume(0.5)
        
    def animation_maker(self):
        self.index = int(pygame.time.get_ticks() / 80) % 4    #Anzahl Bilder pro richtung
        self.image = self.frames[int(self.index)]

    def movement(self, delta_t):
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        self.direction = (player_pos - enemy_pos).normalize()
      
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

    def check_death(self):
        if self.health < 1:
            self.deat_sound.play()
            self.kill()
            return True
            
    def update(self, delta_t): 
        self.check_death
        self.movement(delta_t)
        self.animation_maker()
        
class BossEnemy(Enemy):
    def __init__(self, frames, pos, player, groups, obstacle_group, bullet_group, hardMode):
        super().__init__(frames, pos, player, groups, obstacle_group, bullet_group, hardMode)
        self.health = 4
        self.speed = 100
        self.hitbox = self.rect.inflate(-60, -80)
        
