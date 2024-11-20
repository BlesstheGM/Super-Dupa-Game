import pygame
import os

from settings import SCREEN_HEIGHT, SCREEN_WIDTH

class Platform:
    def __init__(self, x, y, width, height, speed, jump):
        image_path = os.path.join("assets", "brick.png")
        
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.direction = 1
        self.jump = jump

    def move(self):
        self.rect.x += self.speed * self.direction
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH - self.rect.width:  # Screen edges
            self.direction *= -1

    def update(self, paused):
        if paused:
            return  # Skip updating if paused
    
    def go_up_and_down(self):
        self.rect.y += self.jump * self.direction  # Move vertically (up or down)
        if self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT - self.rect.height:  # Screen edges
            self.direction *= -1  # Reverse direction if touching screen edges

    def render(self, screen):
        screen.blit(self.image, self.rect)
