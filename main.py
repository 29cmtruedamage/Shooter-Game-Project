import pygame
import asyncio
from player import Player
from sprites import Obstacles, TileSprites, AllSprites, Gun, Bullet
from pytmx.util_pygame import load_pygame
#https://pytmx.readthedocs.io/en/latest/#tile-object-and-map-properties
from random import randint
from os.path import join


class Shooter_Game:
    def __init__(self):
        self.SCRREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.TILE_SIZE = 64
        pygame.init()
        self.screen= pygame.display.set_mode((self.SCRREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Survivor-Shooter")
        self.clock  = pygame.time.Clock()
        self.FPS = 60
        self.gameState = True
        self.all_sprites = AllSprites()
        self.obstacle_group = pygame.sprite.Group()
        
    def setup_map(self):
        map = load_pygame(join('assets', 'map', 'map.tmx'))
        
        #setup the underground (made by tiles)
        for x,y,surface in map.get_layer_by_name('Untergrund').tiles():
            TileSprites((self.TILE_SIZE * x,self.TILE_SIZE * y), surface, self.all_sprites)
        
        #setup all obstacles like trees
        for object in map.get_layer_by_name('obstacles'):
            Obstacles((object.x, object.y), object.image, (self.all_sprites, self.obstacle_group))

        #setup all borders
        for border in map.get_layer_by_name('borders'):
            Obstacles((border.x, border.y), pygame.Surface((border.width, border.height)), self.obstacle_group)

        #gets one predefined spawnpoint on map and let player spawn at this point
        for sp in map.get_layer_by_name('spawnpoint_player'):
            player_pos = (sp.x, sp.y)
        self.player = Player(player_pos, (self.all_sprites), self.obstacle_group)

        self.gun = Gun(self.player, self.all_sprites)
       
        
    async def runGame(self):
        while self.gameState:
            delta_t = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameState = False
            

            
            self.screen.fill((0,200,0))
            
            self.all_sprites.update(delta_t)
            
            self.all_sprites.draw(self.player.rect.center)

            #self.clock.tick(self.FPS)
            pygame.display.flip()
            await asyncio.sleep(0)

        pygame.quit()
        

async def main():
    game = Shooter_Game()
    game.setup_map()
    await game.runGame()

if __name__ == "__main__":
    asyncio.run(main())