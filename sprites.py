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

    def update(self, delta_t):
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
        self.heal_sound = pygame.mixer.Sound(join('sound','heal_sound.mp3'))
        self.heal_sound.set_volume(2)
        self.reload_sound = pygame.mixer.Sound(join('sound','reload_sound.mp3'))
        self.reload_sound.set_volume(2)
        
    def collide_with_player(self):
        if self.rect.colliderect(self.player.hitbox):
            if self.type == 'health' and self.player.health < 3:
                self.player.health += 1
                self.kill()
                self.heal_sound.play()
                self.spawn_allowence[self.pos] = True
            if self.type == 'ammu':
                self.player.ammunition = 100
                self.kill()
                self.reload_sound.play()
                self.spawn_allowence[self.pos] = True

    def update(self, _):
        self.collide_with_player()
  