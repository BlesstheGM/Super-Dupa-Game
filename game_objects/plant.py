import pygame
import os

class Plant:
    def __init__(self, x, y, width, height):
        image_path = os.path.join("assets", "plant.png")
        
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = pygame.Rect(x, y, width, height)

    def render(self, screen):
        screen.blit(self.image, self.rect)
