import pygame
from settings import GRAVITY, JUMP_STRENGTH, SCREEN_HEIGHT, SCREEN_WIDTH
import os 

class Character:
    def __init__(self, x, y, name, level, coin_count):
        image_path = os.path.join("assets", "character.png")
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = 0
        self.on_ground = True
        self.name = name
        self.level = level
        self.coin_count = coin_count
        self.paused = False  # Flag for pause state
        self.pause_key_pressed = False  # Flag to track if the 'P' key has been pressed

    def update(self, keys):
        pygame.mixer.init()
        
        jump_sound_path = os.path.join("sounds", "jump.mp3")
        jump_sound = pygame.mixer.Sound(jump_sound_path)
                
        jump_sound.set_volume(0.2)

        if keys[pygame.K_p] and not self.pause_key_pressed:
            self.paused = not self.paused
            self.pause_key_pressed = True  # Set the flag to avoid toggling multiple times

        if not keys[pygame.K_p]:  # Reset the flag when the key is released
            self.pause_key_pressed = False

        if not self.paused:  # If the game is not paused, update game state
        # Moving the character
            if keys[pygame.K_LEFT]:
                self.rect.x -= 5
            if keys[pygame.K_RIGHT]:
                self.rect.x += 5
            if keys[pygame.K_UP]:
                self.rect.y -= 2
            if keys[pygame.K_DOWN]:
                self.rect.y += 5
            if keys[pygame.K_SPACE] and self.on_ground:
                self.velocity = JUMP_STRENGTH
                self.on_ground = False
                jump_sound.play()

            # Apply gravity
            self.velocity += GRAVITY
            self.rect.y += self.velocity

            # Prevent character from falling through the ground (bottom of the screen)
            if self.rect.y >= SCREEN_HEIGHT - self.rect.height:
                self.rect.y = SCREEN_HEIGHT - self.rect.height
                self.velocity = 0
                self.on_ground = True

            # Make sure character stays within the window
            if self.rect.x < 0:
                self.rect.x = 0
            elif self.rect.x > SCREEN_WIDTH - self.rect.width:
                self.rect.x = SCREEN_WIDTH - self.rect.width
            if self.rect.y < 0:
                self.rect.y = 0
            elif self.rect.y > SCREEN_HEIGHT - self.rect.height:
                self.rect.y = SCREEN_HEIGHT - self.rect.height    


    def render(self, screen):
        screen.blit(self.image, self.rect)

    def render_paused(self, screen):
        # Draw the score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Coins: {self.coin_count}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))  # Draw score at the top-left corner

        # Draw the paused message if paused
        if self.paused:              
            font = pygame.font.SysFont(None, 48)
            paused_text = font.render("PAUSED", True, (255, 0, 0))
            screen.blit(paused_text, (SCREEN_WIDTH // 2 - paused_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
