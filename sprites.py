import pygame
from random import randint
from os.path import join
from math import degrees, atan2
from globals import SCRREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE

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
        self.speed = 20
        if hardMode: self.speed = 220

    def animation_maker(self):
        self.index += 0.035 #Geschwindigkeit der Animation
        self.index %= 4     #Anzahl Bilder pro richtung
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


    def update(self, delta_t): 
        self.movement(delta_t)
        self.animation_maker()

class Gun(pygame.sprite.Sprite):
    def __init__(self, player, groups, gunType):
        super().__init__(groups)
        self.player = player
        self.player_dir = pygame.Vector2(0,1)
        self.distance = 80

        if gunType=='glock': 
            self.gun_surf = pygame.transform.rotozoom(pygame.image.load(join('images', 'gun', 'gun.png')), 0, 0.8).convert_alpha()
            self.type = 'glock'
        if gunType=='uzi':   
            self.gun_surf = pygame.transform.rotozoom(pygame.image.load(join('images', 'gun', 'Uzi.png')), 0, 0.25).convert_alpha()
            self.type = 'uzi'
        self.image = self.gun_surf
        self.rect = self.image.get_frect(center = self.player.rect.center + self.player_dir * self.distance)
        

    def get_direction(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        default_pos = pygame.Vector2(SCRREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.player_dir = (mouse_pos - default_pos).normalize()

    def rotate_gun(self):
        angle = degrees(atan2(self.player_dir.x, self.player_dir.y)) - 90
        if self.player_dir.x > 0: 
            self.image = pygame.transform.rotozoom(self.gun_surf, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.gun_surf, angle*-1, 1)
            self.image = pygame.transform.flip(self.image, False, True)

    def update(self, _):
        self.get_direction()
        self.rotate_gun()
        self.rect.center = self.player.rect.center + self.distance * self.player_dir

class Score(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.player = player

class Bullet(pygame.sprite.Sprite):
    def __init__(self, surf, pos, direction, groups, enemy_group):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.direction = direction
        self.speed = 1200
        self.type = 'bullet'
        self.born_date = pygame.time.get_ticks()
        self.death_time= self.born_date + 2000
        self.current_lifetime = 0
        self.enemy_group = enemy_group

    def check_collision(self):
        pass
        # for enemy in self.enemy_group:
        #     if self.rect.colliderect(enemy.rect):
        #         self.kill()

    def update(self, delta_t):
        self.check_collision()
        self.current_lifetime += 5
        self.rect.center += self.direction * self.speed * delta_t
        if self.death_time - self.current_lifetime < self.born_date:
            self.kill()

class Packs(pygame.sprite.Sprite):
    def __init__(self, type, frame, pos, player, pack_group, groups, spawn_allowence):
        super().__init__(groups)
        self.spawn_allowence = spawn_allowence
        self.pos = pos
        self.image = frame
        self.rect = self.image.get_frect(center= pos)
        self.player = player
        self.type = type
        self.pack_group = pack_group
    
    # def check_if_already_exists(self):
    #     for pack in self.pack_group:
    #         if pack.pos == self.pos:
    #             self.kill()

    def collide_with_player(self):
        if self.rect.colliderect(self.player.hitbox):
            if self.type == 'health' and self.player.health < 3:
                self.player.health += 1
                self.kill()
                self.spawn_allowence[self.pos] = True
            if self.type == 'ammu':
                self.player.ammunition = 100
                self.kill()
                self.spawn_allowence[self.pos] = True

    def update(self, _):
        #self.check_if_already_exists()
        self.collide_with_player()
  