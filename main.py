from asteroid import Asteroid
from asteroidfield import AsteroidField
from player import Player
import pygame
from constants import PLAYER_RADIUS, SCREEN_WIDTH,SCREEN_HEIGHT
from logger import log_state, log_event
import sys
from shot import Shot




def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0.0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids,updatable,drawable)
    AsteroidField.containers = (updatable)
    asteroid_field = AsteroidField()
    shots = pygame.sprite.Group()
    Shot.containers = (shots,updatable,drawable)
    player = Player(SCREEN_WIDTH / 2,SCREEN_HEIGHT / 2)
    

    
    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
       
        screen.fill("black")
        updatable.update(dt)
        for asteroid in asteroids:
             if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
             for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()
                
                
        for sprite in drawable:
            sprite.draw(screen)
        pygame.display.flip()

        # limit framrate to 60
        dt = clock.tick(60) / 1000

    
if __name__ == "__main__":
    main()
