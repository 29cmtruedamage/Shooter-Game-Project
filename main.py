import pygame


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
        
    def runGame(self):
        while self.gameState:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("LÖSCHEN")
                    self.gameState = False
               
            print("Hallo")
            self.screen.fill((250, 240, 230))
            self.clock.tick(self.FPS)
            pygame.display.update()
        
        pygame.quit()
        
game = Shooter_Game()

game.runGame()
            
        
