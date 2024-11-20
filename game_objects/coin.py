import pygame

class Coin:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)  # Coin is a small circle

    def render(self, screen):
        pygame.draw.circle(screen, (255, 223, 0), self.rect.center, 10)  # Yellow coin
