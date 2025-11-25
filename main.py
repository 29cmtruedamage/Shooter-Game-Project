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

        #Groups
        self.all_sprites = AllSprites()
        self.obstacle_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        
        #Gun parameters
        self.shoot_timer = 0
        self.shoot_rate = 50

        #custom events
        self.enemie_spawnEvent = pygame.event.custom_type()
        self.enemie_spawnTime = 500
        pygame.time.set_timer(self.enemie_spawnEvent, self.enemie_spawnTime)
        self.enemie_spawnPlace = []

        #score
        self.score = 0

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
        self.player = Player(player_pos, (self.all_sprites), self.obstacle_group)

        self.gun = Gun(self.player, self.all_sprites)

    def input_handling(self):
        leftclick = pygame.mouse.get_pressed()[0]
        self.shoot_timer += 1

        if leftclick and self.shoot_timer > self.shoot_rate:
            pos = self.gun.rect.center + self.gun.player_dir * 100
            print("Shoot")
            Bullet(self.bullet_surf, pos, self.gun.player_dir, (self.all_sprites, self.bullet_group), self.enemy_group)
            self.shoot_timer = 0
            

    def check_bullet_enemy_collision(self):
        for bullet in self.bullet_group:
            for enemy in self.enemy_group:
                if bullet.rect.colliderect(enemy.rect):
                    self.score += 1
                    enemy.kill()
                    bullet.kill()


    async def runGame(self):
        self.setup_game()
        self.load_dynamic_images()

        while self.gameState:
            delta_t = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameState = False
                if event.type == self.enemie_spawnEvent:
                    type = random.choice(['bat', 'blob', 'skeleton'])
                    pos = random.choice(self.enemie_spawnPlace)
                    print(type)
                    Enemy(self.enemies[type], pos, self.player, (self.all_sprites, self.enemy_group), self.obstacle_group, self.bullet_group)
                    
            self.input_handling()
            
            self.screen.fill((0,200,0))
            self.check_bullet_enemy_collision()
            self.all_sprites.update(delta_t)
            
            self.all_sprites.draw(self.player.rect.center)

            pygame.display.flip()
            await asyncio.sleep(0)
            
        pygame.quit()
        

async def main():
    game = Shooter_Game()
    await game.runGame()

if __name__ == "__main__":
    asyncio.run(main())