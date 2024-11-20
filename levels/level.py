import pygame
from game_objects.character import Character
from game_objects.data_mananger import get_character_data, update_character_coins, update_character_deaths, update_character_level
from game_objects.enemy import Enemy
from game_objects.platform import Platform
from game_objects.coin import Coin
from game_objects.plant import Plant
from game_objects.pipe import Pipe
import threading
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, SKY_BLUE, WHITE
import os

class Level:
    def __init__(self, screen, character):
        self.screen = screen
        self.character = character

        # x, y, width, height
        
        self.platforms =[
            # level 1 
             [
                [Platform(50, 500, 100, 10, 0, 0), Platform(150, 400, 100, 10, 0, 0), Platform(250, 300, 100, 10, 1, 0)], # zone 1
                [Platform(50, 450, 100, 10, 0, 0), Platform(400, 350, 100, 10, 0, 0), Platform(650, 250, 120, 10, 0, 0)], # zone 2
                [Platform(0, 500, 600, 10, 0, 0)], # Zone 3
            ],

            # level 2
            [
                [Platform(100, 500, 100, 10, 0, 0), Platform(300, 460, 100, 10, 0, 0), Platform(500, 420, 100, 10, 0, 0), Platform(700, 380, 100, 10, 0, 0), Platform(900, 340, 100, 10, 0, 0)],  # zone 1
                [Platform(50, 500, 100, 10, 2, 0), Platform(200, 400, 100, 10, 2, 0), Platform(350, 300, 100, 10, 3, 0), Platform(500, 200, 120, 10, 1, 0)],  # zone 2
                [Platform(50, 500, 100, 10, 0, 0), Platform(150, 450, 100, 10, 0, 0), Platform(250, 400, 100, 10, 0, 0), Platform(350, 350, 100, 10, 0, 0), Platform(450, 300, 100, 10, 0, 0)],  # zone 3
            ],

            #level3
            [
                [Platform(100, 500, 100, 10, 0, 3),  # Fast vertical jump
                Platform(300, 400, 100, 10, 0, 4),  # Medium vertical jump
                Platform(500, 300, 100, 10, 0, 2),  # Slow vertical jump
                Platform(700, 250, 100, 10, 3, 0),  # Fast horizontal speed
                Platform(900, 200, 100, 10, 2, 0),  # Medium horizontal speed
                Platform(1100, 150, 100, 10, 1, 0)],  # Slow horizontal speed

                [Platform(50, 500, 100, 10, 0, 0),  # Stationary sinking platform
                Platform(150, 420, 100, 10, 0, 3),  # Fast sinking platform
                Platform(250, 350, 100, 10, 0, 1),  # Slow sinking platform

                Platform(500, 300, 50, 200, 2, 0),  # Fast wall (left-right motion)
                Platform(650, 250, 50, 200, 1, 0)],  # Slow wall (left-right motion)

                [Platform(100, 500, 100, 10, 0, 0),  # Stationary falling platform
                Platform(200, 450, 100, 10, 0, 4),  # Fast falling platform
                Platform(350, 400, 100, 10, 0, 2),  # Medium falling platform
                Platform(500, 350, 100, 10, 0, 3),  # Fast falling platform

                Platform(650, 300, 100, 10, 3, 0),  # Fast horizontal platform
                Platform(800, 200, 100, 10, 0, 4),  # Fast vertical platform
                Platform(950, 150, 100, 10, 1, 3)],  # Medium horizontal/vertical platform
            ],

            #level4
            [
                [Platform(100, 500, 80, 10, 0, 0), Platform(250, 450, 120, 10, 0, 3), Platform(400, 350, 100, 10, 3, 0), Platform(600, 250, 60, 10, 1, 0), Platform(250, 200, 100, 10, 0, 0)],  # Zone 1 (moving stairs)
                [Platform(100, 550, 80, 10, 0, 1), Platform(350, 450, 100, 10, 1, 0), Platform(500, 350, 120, 10, 0, 2), Platform(650, 250, 80, 10, 0, 0)],  # Zone 2 (downward)
                [Platform(0, 400, 150, 10, 3, 0), Platform(250, 100, 100, 10, 0, 2),  Platform(600, 100, 100, 10, 0, 2)],  # Zone 3 (additional)
            ],

            #level5
            [
                [Platform(100, 500, 80, 10, 1, 1), Platform(300, 450, 100, 10, 2, 1), Platform(500, 350, 120, 10, 1, 2), Platform(650, 200, 80, 10, 2, 1), Platform(250, 100, 120, 10, 1, 2)],  # Zone 1 (random)
                [Platform(100, 550, 100, 10, 1, 2), Platform(300, 450, 80, 10, 2, 1), Platform(500, 350, 100, 10, 0, 2), Platform(650, 200, 120, 10, 3, 1)],  # Zone 2 (bouncing)
                [Platform(200, 500, 100, 10, 0, 1), Platform(400, 350, 100, 10, 0, 1), Platform(600, 200, 100, 10, 0, 1), Platform(150, 300, 100, 10, 1, 1), Platform(300, 400, 100, 10, 1, -1), Platform(500, 500, 100, 10, -1, 1), Platform(250, 400, 100, 10, 0, 2), Platform(450, 150, 100, 10, 0, 2), Platform(550, 100, 100, 10, 0, 2)],  # Zone 3
            ],
        ]
        
        self.coins = [
             # level 1 
            [
                [Coin(100, 460), Coin(200, 360), Coin(300, 260)],  # zone 1
                [Coin(450, 230), Coin(300, 300), Coin(600, 100)],  # zone 2
                [Coin(50, 480), Coin(150, 480), Coin(250, 480), Coin(350, 480), Coin(450, 480), Coin(550, 480), Coin(650, 480), Coin(750, 480)]  # zone 3
            ],

            # level 2
            [
                [Coin(150, 490), Coin(350, 440), Coin(550, 400), Coin(750, 360), Coin(950, 320)],  # zone 1
                [Coin(150, 480), Coin(250, 420), Coin(400, 370), Coin(550, 280)],  # zone 2
                [Coin(100, 460), Coin(200, 410), Coin(300, 360), Coin(400, 310), Coin(500, 260)]  # zone 3
            ],

            #level3
            [
                [Coin(150, 490), Coin(300, 450), Coin(450, 410), Coin(600, 370), Coin(750, 330), Coin(850, 280),
                Coin(950, 240), Coin(1050, 190), Coin(1150, 140), Coin(1250, 100),
                Coin(50, 490), Coin(100, 450),  # Top left coins
                Coin(200, 250), Coin(300, 200)],  # Approaching middle top coins

                [Coin(150, 480), Coin(250, 420), Coin(400, 370), Coin(550, 280), Coin(600, 230), Coin(700, 180),
                Coin(800, 150), Coin(900, 120), Coin(1000, 90), Coin(1100, 60), Coin(1200, 30), Coin(1300, 0),
                Coin(50, 480), Coin(100, 420),  # Top left coins
                Coin(200, 250), Coin(300, 200)],  # Approaching middle top coins

                [Coin(100, 460), Coin(250, 400), Coin(350, 350), Coin(500, 300), Coin(600, 250), Coin(750, 200),
                Coin(850, 150), Coin(950, 100), Coin(1050, 50), Coin(1150, 0),
                Coin(50, 460), Coin(100, 400),  # Top left coins
                Coin(200, 250), Coin(300, 200)],  # Approaching middle top coins
            ],

            #level4
            [
                [Coin(100, 200), Coin(200, 460), Coin(300, 370), Coin(450, 280), Coin(600, 200)],  # Zone 1
                [Coin(100, 130), Coin(400, 230), Coin(600, 130), Coin(230, 400), Coin(300, 520)],  # Zone 2
                [Coin(50, 50), Coin(200, 50), Coin(350, 50)],  # Zone 3
            ],

            #level5
            [
                [Coin(150, 460), Coin(350, 370), Coin(550, 280)],  # Zone 1 (hard-to-reach)
                [Coin(100, 130), Coin(400, 230), Coin(600, 130)],  # Zone 2 (risky)
                [Coin(50, 50), Coin(250, 50), Coin(450, 50), Coin(150, 460), Coin(350, 370), Coin(550, 280), Coin(100, 130)],  # Zone 3 (timed challenge)
            ],
        ]

        self.enemies = [
            # level 1 
            [
                [Enemy(200, 460, 40, 40, 2), Enemy(400, 360, 40, 40, 4), Enemy(600, 260, 40, 40, 6)], # zone 1
                [Enemy(100, 320, 40, 40, 3), Enemy(250, 280, 40, 40, 2), Enemy(400, 230, 40, 40, 4), Enemy(600, 160, 40, 40, 3)],  # zone 2
                [Enemy(50, 490, 40, 40, 2), Enemy(150, 490, 40, 40, 3), Enemy(250, 490, 40, 40, 2), Enemy(350, 490, 40, 40, 4),
                Enemy(450, 490, 40, 40, 3), Enemy(550, 490, 40, 40, 4), Enemy(650, 490, 40, 40, 3), Enemy(750, 490, 40, 40, 2)]  # zone 3
            ],

            # level 2
            [
                [Enemy(150, 480, 40, 40, 2), Enemy(350, 430, 40, 40, 3), Enemy(550, 390, 40, 40, 2), Enemy(750, 350, 40, 40, 4)],  # zone 1
                [Enemy(150, 470, 40, 40, 3), Enemy(250, 380, 40, 40, 4), Enemy(400, 320, 40, 40, 2), Enemy(550, 230, 40, 40, 4)],  # zone 2
                [Enemy(100, 460, 40, 40, 3), Enemy(250, 350, 40, 40, 4), Enemy(400, 280, 40, 40, 2), Enemy(450, 200, 40, 40, 3)]  # zone 3
            ],

            #level3
            [
                [Enemy(200, 460, 40, 40, 3), Enemy(400, 420, 40, 40, 2), Enemy(600, 380, 40, 40, 4)],  # Zone 1
                [Enemy(150, 470, 40, 40, 3), Enemy(250, 380, 40, 40, 4), Enemy(400, 320, 40, 40, 2), Enemy(550, 230, 40, 40, 4)],  # Zone 2
                [Enemy(150, 400, 40, 40, 3), Enemy(350, 350, 40, 40, 5), Enemy(550, 250, 40, 40, 2), Enemy(700, 200, 40, 40, 4)]  # Zone 3
            ],

            #level4
            [
                [Enemy(150, 460, 40, 40, 7), Enemy(400, 350, 40, 40, 6), Enemy(600, 250, 40, 40, 8), Enemy(500, 450, 40, 40, 9)],  # Zone 1 (fast)
                [Enemy(200, 500, 40, 40, 6), Enemy(300, 400, 40, 40, 7), Enemy(500, 300, 40, 40, 5), Enemy(650, 200, 40, 40, 9)],  # Zone 2
                [Enemy(50, 50, 40, 40, 5), Enemy(200, 50, 40, 40, 6), Enemy(350, 50, 40, 40, 7), Enemy(500, 100, 40, 40, 6)],  # Zone 3
            ],

            #level5
            [
                [Enemy(150, 460, 40, 40, 10), Enemy(400, 350, 40, 40, 12), Enemy(600, 250, 40, 40, 14)],  # Zone 1 (super fast)
                [Enemy(400, 500, 40, 40, 4), Enemy(350, 400, 40, 40, 6), Enemy(550, 300, 40, 40, 8)],  # Zone 2 (spinning)
                [Enemy(0, 150, 40, 40, 2), Enemy(550, 250, 40, 40, 2), Enemy(400, 300, 40, 40, 2), Enemy(450, 200, 40, 40, 2), Enemy(120, 50, 40, 40, 3), Enemy(200, 50, 40, 40, 5)],  # Zone 3 (relentless)
            ],
        ]

        self.plants = [
            # level 1 
             [
                [Plant(SCREEN_WIDTH - 450, SCREEN_HEIGHT - 100, 50, 100 )], # zone 1
                [Plant(150, SCREEN_HEIGHT - 100, 50, 100 )], # zone 2
                [Plant(300, SCREEN_HEIGHT - 100, 50, 100 )] # zone 3
            ],

            # level 2
            [
                [Plant(300, SCREEN_HEIGHT - 100, 50, 100)],  # zone 1
                [Plant(300, SCREEN_HEIGHT - 100, 50, 100)],  # zone 2
                [Plant(450, SCREEN_HEIGHT - 100, 50, 100)]  # zone 3
            ],

            #level3
            [
                [Plant(300, SCREEN_HEIGHT - 100, 50, 100), Plant(500, SCREEN_HEIGHT - 100, 50, 100)],  # Additional plant
                [Plant(300, SCREEN_HEIGHT - 100, 50, 100), Plant(500, SCREEN_HEIGHT - 100, 50, 100), Plant(700, SCREEN_HEIGHT - 200, 50, 100), Plant(900, SCREEN_HEIGHT - 250, 50, 100)],  # Two additional plants
                [Plant(50, SCREEN_HEIGHT - 100, 50, 100), Plant(150, SCREEN_HEIGHT - 100, 50, 100), Plant(250, SCREEN_HEIGHT - 100, 50, 100), Plant(350, SCREEN_HEIGHT - 100, 50, 100), Plant(450, SCREEN_HEIGHT - 100, 50, 100), Plant(550, SCREEN_HEIGHT - 100, 50, 100)]  # Three additional plants
            ],

            #level4
            [
                [Plant(100, 500, 50, 50), Plant(150, SCREEN_HEIGHT - 80, 50, 100), Plant(450, SCREEN_HEIGHT - 80, 50, 100)],  # Zone 1 (more plants)
                [Plant(150, SCREEN_HEIGHT - 80, 50, 100), Plant(400, SCREEN_HEIGHT - 80, 50, 100)],  # Zone 2 (new plants)
                [Plant(50, SCREEN_HEIGHT - 150, 50, 100), Plant(150, SCREEN_HEIGHT - 150, 50, 100), Plant(250, SCREEN_HEIGHT - 150, 50, 100), Plant(350, SCREEN_HEIGHT - 150, 50, 100), Plant(450, SCREEN_HEIGHT - 150, 50, 100), Plant(550, SCREEN_HEIGHT - 150, 50, 100), Plant(650, SCREEN_HEIGHT - 150, 50, 100)],  # Zone 3 (added plants)
            ],

            #level5
            [
            [Plant(150, SCREEN_HEIGHT - 80, 50, 100), Plant(500, SCREEN_HEIGHT - 80, 50, 100)],  # Zone 1 (more plants)
            [Plant(180, SCREEN_HEIGHT - 80, 50, 100), Plant(400, SCREEN_HEIGHT - 80, 50, 100)],  # Zone 2 (dangerous)
            [Plant(50, SCREEN_HEIGHT - 100, 50, 100), Plant(450, SCREEN_HEIGHT - 100, 50, 100), Plant(200, SCREEN_HEIGHT - 100, 50, 100), Plant(400, SCREEN_HEIGHT - 100, 50, 100), Plant(600, SCREEN_HEIGHT - 100, 50, 100)],  # Zone 3 (added plants)
            ],
        ]

        self.pipe = Pipe(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100, 50, 100)

        self.zone = 0

    def update(self, keys):
        self.character.update(keys)

        pygame.mixer.init()

        coin_sound_path = os.path.join("sounds", "coin.mp3")
        coin_sound = pygame.mixer.Sound(coin_sound_path)
        coin_sound.set_volume(0.2)

        teleport_sound_path = os.path.join("sounds", "teleport.mp3")
        teleport_sound = pygame.mixer.Sound(teleport_sound_path)
        teleport_sound.set_volume(0.2)

        if not self.character.paused:  # If the game is not paused, update game state

            for platform in range(0, len(self.platforms[self.character.level-1][self.zone])):
                self.platforms[self.character.level-1][self.zone][platform].move()
            
            for platform in range(0, len(self.platforms[self.character.level-1][self.zone])):
                self.platforms[self.character.level-1][self.zone][platform].go_up_and_down()

            for platform in range(0, len(self.platforms[self.character.level-1][self.zone])):
                brick = self.platforms[self.character.level-1][self.zone][platform]
                if self.character.rect.colliderect(brick.rect) and self.character.velocity >= 0:
                    self.character.rect.y = brick.rect.top - self.character.rect.height
                    self.character.velocity = 0
                    self.character.on_ground = True


            # Coin collection
            for coin in range(0, len(self.coins[self.character.level-1][self.zone])):
                if self.character.rect.colliderect(self.coins[self.character.level-1][self.zone][coin].rect):
                    self.character.coin_count += 1
                    update_character_coins(self.character.name, self.character.coin_count)
                    coin_sound.play()
                    del self.coins[self.character.level-1][self.zone][coin]
                    break    
                    

            # Game Over condition
            for enemy in range(0, len(self.enemies[self.character.level-1][self.zone])):
                self.enemies[self.character.level-1][self.zone][enemy].move()

            for enemy in range(0, len(self.enemies[self.character.level-1][self.zone])):
                if self.character.rect.colliderect(self.enemies[self.character.level-1][self.zone][enemy].rect):
                    self.show_game_over_screen()     

            for plant in range(0, len(self.plants[self.character.level-1][self.zone])):
                if self.character.rect.colliderect(self.plants[self.character.level-1][self.zone][plant].rect):
                    self.show_game_over_screen() 

            if self.character.rect.colliderect(self.pipe.rect):
                # Resolve the collision based on the direction of movement
                if keys[pygame.K_LEFT]:
                    self.character.rect.left = self.pipe.rect.right  # Push the character right
                if keys[pygame.K_RIGHT]:
                    self.character.rect.right = self.pipe.rect.left  # Push the character left
                if keys[pygame.K_UP]:
                    self.character.rect.top = self.pipe.rect.bottom  # Push the character down
                if self.character.rect.bottom <= self.pipe.rect.top + 10:
                    # Teleport the character to a new position
                    teleport_sound.play()
                    self.character.rect.x = 100  # New X position (or any action you want)
                    self.character.rect.y = 600  # New Y position (or any action you want)
                    self.character.velocity = 0  # Reset vertical velocity
                    self.character.on_ground = True  # Character should land after teleporting
                    if (self.zone == 2):
                        update_character_level(self.character.name, self.character.level+1)
                        from main import main
                        main(self.character.name)
                    else:    
                        self.zone += 1
                    if (self.zone == 1  and self.character.level==3):
                        timer = threading.Timer(20, self.secret_finish)
                        timer.start()

    def secret_finish(self):
        self.zone += 1

    def render(self):
        self.screen.fill(SKY_BLUE)
        self.character.render(self.screen)

        for platform in range(0, len(self.platforms[self.character.level-1][self.zone])):
            self.platforms[self.character.level-1][self.zone][platform].render(self.screen)

        for coin in range(0, len(self.coins[self.character.level-1][self.zone])):
            self.coins[self.character.level-1][self.zone][coin].render(self.screen)

        for enemy in range(0, len(self.enemies[self.character.level-1][self.zone])):
            self.enemies[self.character.level-1][self.zone][enemy].render(self.screen)

        for plant in range(0, len(self.plants[self.character.level-1][self.zone])):
            self.plants[self.character.level-1][self.zone][plant].render(self.screen)

        self.pipe.render(self.screen)

    def show_game_over_screen(self):
        level_number, coin_count, death_count = get_character_data(self.character.name)
        death_count += 1
        update_character_deaths(self.character.name, death_count)
        game_over_sound = pygame.mixer.Sound("sounds/game_over.mp3")
        game_over_sound.set_volume(0.2)
        game_over_sound.play()
        font = pygame.font.SysFont(None, 48)
        
        # Render each line of text separately
        line1 = font.render("Game Over!", True, (255, 0, 0))
        line2 = font.render(f"Score: {self.character.coin_count}", True, (255, 0, 0))
        line3 = font.render("Press 'R' to Restart", True, (255, 0, 0))
        line4 = font.render("Press 'ESC' to MENU", True, (255, 0, 0))
        
        # Draw the text on the screen with adjusted Y positions for each line
        self.screen.blit(line1, (SCREEN_WIDTH // 2 - line1.get_width() // 2, SCREEN_HEIGHT // 2 - 100))  # Position for the first line
        self.screen.blit(line2, (SCREEN_WIDTH // 2 - line2.get_width() // 2, SCREEN_HEIGHT // 2 - 50))      # Position for the second line
        self.screen.blit(line3, (SCREEN_WIDTH // 2 - line3.get_width() // 2, SCREEN_HEIGHT // 2 + 0))  # Position for the third line
        self.screen.blit(line4, (SCREEN_WIDTH // 2 - line4.get_width() // 2, SCREEN_HEIGHT // 2 + + 50))

        pygame.display.update()

        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Restart the game
                        waiting_for_restart = False
                        from main import main
                        main(self.character.name)
                    if event.key == pygame.K_ESCAPE:  # Restart the game
                        waiting_for_restart = False
                        from main import main
                        main()
   
