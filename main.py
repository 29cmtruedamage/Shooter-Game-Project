import pygame
import asyncio
from player import Player
from sprites import Obstacles, TileSprites, Gun, Bullet, Enemy
from sprite_groups import AllSprites #, ShootingSprites
from pytmx.util_pygame import load_pygame
#https://pytmx.readthedocs.io/en/latest/#tile-object-and-map-properties
import random
from os.path import join
from os import walk
from globals import SCRREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE


class Shooter_Game:
    def __init__(self):
        #initial setup
        pygame.init()
        self.screen= pygame.display.set_mode((SCRREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Survivor-Shooter")
        self.clock  = pygame.time.Clock()
        self.FPS = 60
        self.gameState = True
        self.gameOver = True
        #Groups
        self.all_sprites = AllSprites()
        self.obstacle_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        
        #Gun parameters
        self.shoot_timer = 0
        self.shoot_rate = 50 #glock
        self.shoot_rate_uzi = 50

        #custom events
        self.enemie_spawnEvent = pygame.event.custom_type()
        self.enemie_spawnTime = 500
        pygame.time.set_timer(self.enemie_spawnEvent, self.enemie_spawnTime)
        self.enemie_spawnPlace = []
        
        #score 
        self.score = 0
        self.score_font = pygame.font.Font(join('textstyles','textStyle1.ttf'), 55)
        self.score_text = self.score_font.render("Kills: ", True, 'Red')
        
        #health
        #//
        
    #sounds
    def load_sounds(self):
        self.shoot_sound = pygame.mixer.Sound(join('sound','shoot_sound.wav'))
        self.shoot_sound.set_volume(0.4)
        self.deat_sound = pygame.mixer.Sound(join('sound','death_sound.wav'))
        self.deat_sound.set_volume(0.6)
        self.bg_sound = pygame.mixer.Sound(join('sound','bg_sound.mp3'))
        self.bg_sound.set_volume(0.6)
        self.bg_sound.play(5)

    def load_dynamic_images(self):
        self.bullet_surf = pygame.image.load(join('images', 'gun', 'bullet.png')).convert_alpha()
        self.enemies = {'bat': [], 'blob': [], 'skeleton': []}
        for enemie in self.enemies:
            for path, subfolder, files in walk(join('images', 'enemies', enemie)):
                for file in files:
                    surf = pygame.image.load(join(path, file)).convert_alpha()
                    self.enemies[enemie].append(surf)


    def setup_game(self):
        map = load_pygame(join('assets', 'map', 'map.tmx'))
        
        #setup the underground (made by tiles)
        for x,y,surface in map.get_layer_by_name('Untergrund').tiles():
            TileSprites((TILE_SIZE * x,TILE_SIZE * y), surface, self.all_sprites)
        
        #setup all obstacles like trees
        for object in map.get_layer_by_name('obstacles'):
            Obstacles((object.x, object.y), object.image, (self.all_sprites, self.obstacle_group))

        #setup all borders
        for border in map.get_layer_by_name('borders'):
            Obstacles((border.x, border.y), pygame.Surface((border.width, border.height)), self.obstacle_group)

        #setup Enemies
        for enemy in map.get_layer_by_name('enemies'):
            self.enemie_spawnPlace.append((enemy.x, enemy.y))

        #gets one predefined spawnpoint on map and let player spawn at this point
        for sp in map.get_layer_by_name('spawnpoint_player'):
            player_pos = (sp.x, sp.y)

        self.player = Player(player_pos, (self.all_sprites), self.obstacle_group, self.enemy_group)
        self.gun = Gun(self.player, self.all_sprites)
        self.score_rect = self.score_text.get_rect(center=(SCRREEN_WIDTH / 10, 50))

    def update_score(self):
        self.score_text = self.score_font.render(f"KILLS: {self.score}", True, (189,61,61))

    def input_handling(self):
        leftclick = pygame.mouse.get_pressed()[0]
        self.shoot_timer += 1

        if leftclick and self.shoot_timer > self.shoot_rate:
            pos = self.gun.rect.center + self.gun.player_dir * 100
            self.shoot_sound.play()
            Bullet(self.bullet_surf, pos, self.gun.player_dir, (self.all_sprites, self.bullet_group), self.enemy_group)
            self.shoot_timer = 0
            

    def check_bullet_enemy_collision(self):
        for bullet in self.bullet_group:
            for enemy in self.enemy_group:
                if bullet.rect.colliderect(enemy.rect):
                    self.score += 1
                    enemy.kill()
                    bullet.kill()
                    self.deat_sound.play()

    def check_death(self):
        #unser leben: self.health
        if self.player.health < 1:      
            self.gameOver = False
            print("DU BSIT TOOOOOOOOOOOOOT")
    
    def gameOver_screen(self):
        pass

    def runGame(self):
        self.setup_game()
        self.load_dynamic_images()
        self.load_sounds()
        while self.gameState:
            
            delta_t = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameState = False
                if event.type == self.enemie_spawnEvent:
                    type = random.choice(['bat', 'blob', 'skeleton'])
                    pos = random.choice(self.enemie_spawnPlace)
                    
                    Enemy(self.enemies[type], pos, self.player, (self.all_sprites, self.enemy_group), self.obstacle_group, self.bullet_group)
            
            self.check_death()
            self.input_handling()
            self.update_score()
            self.screen.fill((0,200,0))
            self.check_bullet_enemy_collision()
            self.all_sprites.update(delta_t)
            
            self.all_sprites.draw(self.player.rect.center)
            self.screen.blit(self.score_text, self.score_rect)
            pygame.display.flip()
            print(f"Your Healt: {self.player.health}, Your Recovery Time: {self.player.recovery_time}")
            
            
            pygame.display.flip()
        pygame.quit()

def main():
    game = Shooter_Game()
    game.runGame()

if __name__ == "__main__":
    main()
