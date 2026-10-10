from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_SHOOT_COOLDOWN_SECONDS, PLAYER_SHOOT_SPEED, PLAYER_SPEED, PLAYER_TURN_SPEED
import pygame
from shot import Shot

class Player(CircleShape):
    def __init__(self, x: float, y: float,) -> None:
        super().__init__(x,y,PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
        self.powerup_timer = 0

        
    def activate_powerup(self, duration=10):
        self.powerup_timer = duration
        
    def collides_with(self, other):
        return other.collides_with_triangle(self.triangle())
    

    # in the Player class
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
        # Calculates Turn Speed
    def rotate(self,dt):
        self.rotation += PLAYER_TURN_SPEED * dt
        

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        self.timer -= dt

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt/2)
        if keys[pygame.K_SPACE]:
            self.shoot()
        self.wrap_around()
        if self.powerup_timer > 0:
            self.powerup_timer -= dt
            
                
           
                

            
    def move(self,dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        if self.powerup_timer > 0:
            cooldown /= 2

        if self.timer > 0:
            return
        self.timer = cooldown

        # Single shot vs Triple spread shot
        if self.powerup_timer > 0:
            angles = [-35,-15, 0, 15, 35]
            for offset in angles:
                self._spawn_shot(self.rotation + offset)
        else:
            self._spawn_shot(self.rotation)
        
    def _spawn_shot(self, angle):
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(angle) * PLAYER_SHOOT_SPEED

    
        