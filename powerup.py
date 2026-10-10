# powerup.py
import pygame
from circleshape import CircleShape

class PowerUp(CircleShape):
    def __init__(self, x, y):
        # A radius of ~15 gives it a good collision boundary matching a 30x30 square
        super().__init__(x, y, 15)
        self.width = 30
        self.height = 30

    def draw(self, screen):
        # Draw a filled green rectangle centered on the position
        rect = pygame.Rect(
            self.position.x - self.width / 2,
            self.position.y - self.height / 2,
            self.width,
            self.height
        )
        pygame.draw.rect(screen, (0, 255, 0), rect)

    def update(self, dt):
        # Static powerup, does not move (or add wrap_around if desired)
        pass