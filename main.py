import pygame
import asyncio
from player import Player

screen_width = 1280
screen_height = 720

class Shooter_Game:
    def __init__(self):
        pygame.init()
        self.screen= pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Survivor-Shooter")
        self.clock  = pygame.time.Clock()
        self.FPS = 60
        self.gameState = True
        self.all_sprites = pygame.sprite.Group()
        self.player = Player((600, 400), self.all_sprites)
        


    async def runGame(self):
        while self.gameState:
            delta_t = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("LÖSCHEN")
                    self.gameState = False
               
            print("Hallo")
            self.screen.fill((0,200,0))
            
            self.all_sprites.update(delta_t)
            self.all_sprites.draw(self.screen)

            #self.clock.tick(self.FPS)
            pygame.display.flip()
            await asyncio.sleep(0)

        pygame.quit()
        

async def main():
    game = Shooter_Game()
    await game.runGame()

if __name__ == "__main__":
    asyncio.run(main())