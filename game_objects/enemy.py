import pygame
import os

class Enemy:
    def __init__(self, x, y, width, height, speed):
        self.image = pygame.image.load(os.path.join("assets", "enemy.png"))
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed
        self.direction = 1

    def move(self):
        self.rect.x += self.speed * self.direction
        if self.rect.x < 0 or self.rect.x > 800 - self.rect.width:  # Screen edges
            self.direction *= -1
            
    def update(self, paused):
        if paused:
            return  # Skip updating if paused

    def render(self, screen):
        screen.blit(self.image, self.rect)
