from shlex import split
from logger import log_event
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH, PER_SMALL_KILL
import pygame
import random

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen,"white",self.position,self.radius,LINE_WIDTH)

    def update(self,dt)-> None:
        self.position += self.velocity * dt
        self.wrap_around()

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return PER_SMALL_KILL
        log_event("asteroid_split")
        angle = random.uniform(20,50)
        positive = self.velocity.rotate(angle)
        negative = self.velocity.rotate(-angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid_positive = Asteroid(self.position.x,self.position.y,new_radius)
        asteroid_negative = Asteroid(self.position.x,self.position.y,new_radius)
        asteroid_positive.velocity = positive*1.2
        asteroid_negative.velocity = negative*1.2
    
        
                