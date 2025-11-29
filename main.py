import pygame
import time
from player import Player
from sprites import Obstacles, TileSprites, Gun, Bullet, Enemy, Packs
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
        
        #game states
        self.gameState = True
        self.gameOn = False
        self.gameOver = False
        self.start_screen_state = True
        #Groups
        self.all_sprites = AllSprites()
        self.obstacle_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.pack_group = pygame.sprite.Group()
        #Gun parameters
        self.shoot_timer = 0
        self.shoot_rate_glock = 350 #glock
        self.shoot_rate_uzi = 200 #uzi
        self.current_gun_rate = self.shoot_rate_glock
        self.shoot_rate = pygame.time.get_ticks() + self.current_gun_rate
        
        self.ammunition = 100


        #custom events / time based eventy
        self.enemie_spawnEvent = pygame.event.custom_type()
        self.enemie_spawnTime = 400
        pygame.time.set_timer(self.enemie_spawnEvent, self.enemie_spawnTime)
        self.enemie_spawnPlace = []
        self.sp_pos = (0,0)
        self.kills_to_change_gun = 30
        self.hardmode = False

        #packs
        self.pack_spawnEvent = pygame.event.custom_type()
        self.pack_spawnTime = 10000
        pygame.time.set_timer(self.pack_spawnEvent, self.pack_spawnTime)
        self.pack_spawnPos = []
        self.pack_spawnAllowence = {}


        #colours
        self.LightGrey = (230, 230, 230)
        self.DarkGrey =  (130, 130, 130)
        self.colourBeige = (255,222,173)
        self.colourGreen = (0, 139, 69)
        self.Grey = (31,31,31)
        #score 
        self.score = 0
        
        #load
        self.load_fonts()

    def load_fonts(self):
        #Ammunition Font
        self.ammu_font = pygame.font.Font(join('textstyles','textStyle1.ttf'), 53)
        self.ammu_text = self.ammu_font.render("Ammu: ", True, self.Grey)
        self.ammu_rect = self.ammu_text.get_rect(center=(SCRREEN_WIDTH / 10, 150))
        
        
        #score Fonts
        self.score_font = pygame.font.Font(join('textstyles','textStyle1.ttf'), 53)
        self.score_text = self.score_font.render("Kills: ", True, 'Red')
        self.score_rect = self.score_text.get_rect(center=(SCRREEN_WIDTH / 10, 100))

        #health
        self.heart =  pygame.transform.rotozoom(pygame.image.load(join('images', 'heart', 'heart.png')).convert_alpha(), 0, 1.9)
        self.heart_rect1 = self.heart.get_frect(center=(SCRREEN_WIDTH - 1345, 50))
        self.heart_rect2 = self.heart.get_frect(center=(SCRREEN_WIDTH - 1295, 50))
        self.heart_rect3 = self.heart.get_frect(center=(SCRREEN_WIDTH - 1245, 50))
        self.heart_list = [self.heart_rect1, self.heart_rect2, self.heart_rect3]

        #gameOver Fonts
        self.gameOverScreen_font = pygame.font.Font(join('textstyles','textStyle1.ttf'), 200)
        self.gameOverPressEnter_font = pygame.font.Font(join('textstyles', 'textStyle1.ttf'), 80)

        self.gameOverScreen_text = self.gameOverScreen_font.render("GAME OVER", False, self.colourBeige)
        self.gameOverScreen_rect = self.gameOverScreen_text.get_rect(center=(SCRREEN_WIDTH / 2, 200))
        
        self.gameOverPressEnter_text = self.gameOverPressEnter_font.render("PRESS ENTER TO RESTART", True, self.colourBeige)
        self.gameOverPressEnter_rect = self.gameOverPressEnter_text.get_rect(center=(SCRREEN_WIDTH / 2, 450))

        #start Screen Fonts
        self.text_font = pygame.font.Font(join('textstyles', 'textStyle1.ttf'), 150)
        self.text_text1 = self.text_font.render("Welcome to this Game!", True, self.colourBeige)
        self.text1_rect = self.text_text1.get_rect(center = (SCRREEN_WIDTH / 2, 170))

        self.sign_font = pygame.font.Font(join('textstyles', 'textStyle1.ttf'), 70)
        self.signt_text = self.sign_font.render("A Shooter Made by Muhammed Emir Akgül", True, self.colourBeige)
        self.sign_rect = self.signt_text.get_rect(center = (SCRREEN_WIDTH / 2, 320))
        
        self.defaultVektor_font = pygame.font.Font(join('textstyles', 'textStyle1.ttf'), 100)
        self.defaultVektor_text = self.defaultVektor_font.render("  Platzhalter  ", True, 'Black')
        self.defaultVektor_rect = self.defaultVektor_text.get_rect(center = (SCRREEN_WIDTH / 2, 520))
        
        self.vektor_font = pygame.font.Font(join('textstyles', 'textStyle1.ttf'), 70)
        self.vektor_GameText1 = self.vektor_font.render("Play", True, 'Black')
        self.vektor_rect1 = self.vektor_GameText1.get_rect(center = (SCRREEN_WIDTH / 2, 520))

    def display_startScreen(self):
        self.screen.fill(self.colourGreen)
        self.screen.blit(self.signt_text, self.sign_rect)
        self.screen.blit(self.text_text1, self.text1_rect)
        mouse_pos = pygame.mouse.get_pos()
        if self.defaultVektor_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.DarkGrey, self.defaultVektor_rect, 0, 50)
            self.check_clickOn_play()
        else:
            pygame.draw.rect(self.screen, self.LightGrey, self.defaultVektor_rect, 0, 50)
        self.screen.blit(self.vektor_GameText1, self.vektor_rect1)
    
    def check_clickOn_play(self):
        leftclick = pygame.mouse.get_pressed()[0]
        if leftclick:
            self.start_screen_state = False
            self.gameOn = True

    def running_StartScreen(self):
        while self.start_screen_state:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.start_screen_state = False
                    self.gameState = False
                    self.gameOn = False
                    self.gameOver = False
            self.display_startScreen()
            pygame.display.flip()

    #sounds
    def load_sounds(self):
        self.shoot_sound = pygame.mixer.Sound(join('sound','shoot_sound.wav'))
        self.shoot_sound.set_volume(0.4)
        self.deat_sound = pygame.mixer.Sound(join('sound','death_sound.wav'))
        self.deat_sound.set_volume(0.5)
        self.bg_sound = pygame.mixer.Sound(join('sound','bg_sound.mp3'))
        self.bg_sound.set_volume(0.1)
        self.menu_sound = pygame.mixer.Sound(join('sound','menu.mp3'))
        self.menu_sound.set_volume(0.4)
        self.update_sound = pygame.mixer.Sound(join('sound','update_sound.mp3'))
        self.update_sound.set_volume(2)
        self.heal_sound = pygame.mixer.Sound(join('sound','heal_sound.mp3'))
        self.heal_sound.set_volume(2)
        self.reload_sound = pygame.mixer.Sound(join('sound','reload_sound.mp3'))
        self.reload_sound.set_volume(2)
        
    def load_dynamic_images(self):
        #bullet
        self.bullet_surf = pygame.image.load(join('images', 'gun', 'bullet.png')).convert_alpha()
        #enemies
        self.enemies = {'bat': [], 'blob': [], 'skeleton': []}
        for enemie in self.enemies:
            for path, subfolder, files in walk(join('images', 'enemies', enemie)):
                for file in files:
                    surf = pygame.image.load(join(path, file)).convert_alpha()
                    self.enemies[enemie].append(surf)
        #ammu and health packs
        self.healthpack_surf = pygame.transform.rotozoom(pygame.image.load(join('images', 'gun', 'healthpack.png')).convert_alpha(), 0, 2.5)
        self.ammupack_surf = pygame.transform.rotozoom(pygame.image.load(join('images', 'gun', 'ammunition.png')).convert_alpha(), 0, 2.5)
        self.packs_surfList = {'ammu': self.ammupack_surf, 'health': self.healthpack_surf}

    def setup_map(self):
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
            self.enemie_spawnPlace.append((enemy.x, enemy.y))#-> list of all possible enemy spawnpoints

        for pack in map.get_layer_by_name('packs_spawnpoints'):
            pos = (pack.x, pack.y)
            self.pack_spawnPos.append(pos) #list of all possible positions
            self.pack_spawnAllowence[pos] = True #we tag a Bool to every pos, to check if pos is locked

        for sp in map.get_layer_by_name('spawnpoint_player'):
            self.sp_pos = (sp.x, sp.y)

    def setup_player(self):
        #gets one predefined spawnpoint on map and let player spawn at this point
        self.player = Player(self.sp_pos, (self.all_sprites), 3, 100, self.obstacle_group, self.enemy_group)
        self.glock = Gun(self.player, self.all_sprites, 'glock')
        self.gun = self.glock
    
    def update_gun(self):
        if self.score >= self.kills_to_change_gun and self.gun.type == 'glock':
            self.glock.kill()
            self.uzi = Gun(self.player, self.all_sprites, 'uzi')
            self.gun = self.uzi
            self.current_gun_rate = self.shoot_rate_uzi
            self.hardmode = True
            self.update_sound.play()

    def update_score(self):
        self.score_text = self.score_font.render(f"KILLS: {self.score}", True, (189,61,61))
        self.screen.blit(self.score_text, self.score_rect)

    def update_ammu(self):
        self.ammu_text = self.ammu_font.render(f"Ammu: {self.player.ammunition}", True, self.Grey)
        self.screen.blit(self.ammu_text, self.ammu_rect)

    #gun Shoot: Input handling
    def input_handling(self):
        leftclick = pygame.mouse.get_pressed()[0]
        self.shoot_timer = pygame.time.get_ticks()

        if leftclick and self.shoot_timer > self.shoot_rate and self.player.ammunition > 0:
            pos = self.gun.rect.center + self.gun.player_dir * 100
            self.shoot_sound.play()
            Bullet(self.bullet_surf, pos, self.gun.player_dir, (self.all_sprites, self.bullet_group), self.enemy_group)
            self.shoot_rate = pygame.time.get_ticks() + self.current_gun_rate
            self.player.ammunition -= 1
            
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
            self.gameOn = False
            self.gameOver = True
            print("DU BSIT TOOOOOOOOOOOOOT")
    
    def reset_game(self):
        self.player.health = 3
        self.score = 0
        for e in self.enemy_group:
            e.kill()
        self.bullet_group.empty()
        self.player.kill()
        self.gun.kill()
        self.shoot_rate = self.shoot_rate_glock
        self.hardmode = False

    def gameOver_screen(self):
        self.showScore_text = self.gameOverPressEnter_font.render(f"You got {self.score} kills", True, self.colourBeige)
        self.showScore_rect = self.showScore_text.get_rect(center=(SCRREEN_WIDTH / 2, 350))
        self.screen.fill(self.colourGreen)
        self.screen.blit(self.showScore_text, self.showScore_rect)
        self.screen.blit(self.gameOverScreen_text, self.gameOverScreen_rect)
        self.screen.blit(self.gameOverPressEnter_text, self.gameOverPressEnter_rect)
        #self.screen.blit(self.returnBackMenu_text, self.returnBackMenu_rect)

    def display_health(self):
        for i in range(0, self.player.health):
            self.screen.blit(self.heart, self.heart_list[i])

    #GameLogic if gameOn
    def running_GameOn(self):
        self.setup_player()
        self.bg_sound.play(5)
        while self.gameOn:
            delta_t = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameState = False
                    self.gameOn = False
                    self.gameOver = False
                
                if event.type == self.enemie_spawnEvent:
                    type = random.choice(['bat', 'blob', 'skeleton'])
                    pos = random.choice(self.enemie_spawnPlace)
                    Enemy(self.enemies[type], pos, self.player, (self.all_sprites, self.enemy_group), self.obstacle_group, self.bullet_group, self.hardmode)
                
                if event.type == self.pack_spawnEvent:
                    pos = random.choice(self.pack_spawnPos)
                    if self.pack_spawnAllowence[pos]:
                        if self.player.health < 3:
                            type = random.choice(['health'])
                        if self.player.health >= 3:
                            type = random.choice(['ammu', 'ammu', 'ammu', 'ammu', 'health'])   
                        Packs(type, self.packs_surfList[type],  pos, self.player, self.pack_group, (self.pack_group, self.all_sprites), self.pack_spawnAllowence)
                        self.pack_spawnAllowence[pos] = False
                        
            self.check_death()
            self.input_handling()
        
            self.screen.fill((0,200,0))
            self.check_bullet_enemy_collision()
            self.update_gun()
            self.all_sprites.update(delta_t)
            self.all_sprites.draw(self.player.rect.center)
            
            self.display_health()
            self.update_score()
            self.update_ammu()
            pygame.display.flip()
            #print(pygame.time.get_ticks())
            #print(f"Your Healt: {self.player.health}, Your Recovery Time: {self.player.recovery_time}")
            print(f"A: {self.player.time_now}, B: {self.player.time_till_full_recovery}")
            #print(self.pack_group)

    #GameLogic if gameOver
    def running_GameOver(self):
        self.gameOver_screen()
        self.reset_game()
        time.sleep(0.2)
        self.menu_sound.play(2)
        while self.gameOver:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameState = False
                    self.gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.gameOver = False
                        self.gameOn = True
                        
            pygame.display.flip()



    #The Whole Game
    def runWholeGame(self):#
        self.load_sounds()
        self.setup_map()
        self.load_dynamic_images()

        while self.gameState:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameState = False
            self.running_StartScreen()

            self.running_GameOn()
            self.bg_sound.stop()

            self.running_GameOver()
            self.menu_sound.stop()

        pygame.quit()


def main():
    game = Shooter_Game()
    game.runWholeGame()

if __name__ == "__main__":
    main()
