from asteroid import Asteroid
from asteroidfield import AsteroidField
from player import Player
import pygame
from constants import PER_SECOND_SCORE, PLAYER_RADIUS, SCREEN_WIDTH,SCREEN_HEIGHT
from logger import log_state, log_event
import sys
from shot import Shot
from powerup import PowerUp
import random



def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0.0
    score = 0
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
    font = pygame.font.Font(None, 36)
    powerups = pygame.sprite.Group()
    PowerUp.containers = (powerups, updatable, drawable)
    POWERUP_RESPAWN_TIME = 30.0  # seconds between power-ups
    powerup_timer = 5.0          # wait 5 seconds before the very first one spawns

    def spawn_powerup():
        margin = 50
        x = random.randint(margin, SCREEN_WIDTH - margin)
        y = random.randint(margin, SCREEN_HEIGHT - margin)
        PowerUp(x, y)

    def reset_game():
        # Empty all sprite groups
        updatable.empty()
        drawable.empty()
        asteroids.empty()
        shots.empty()
        powerups.empty()

     

    
        # Recreate the player and field
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        asteroid_field = AsteroidField()
    
        return player, 0,5.0 # Returns fresh player and score = 0
    game_state = "PLAYING"
    player, score,powerup_timer = reset_game()
        
        # Define a restart button rect in the center
    button_rect = pygame.Rect(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 + 50, 200, 50)
                  

    while True:
        dt = clock.tick(60) / 1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
                # Check for button click when in GAME_OVER state
            if game_state == "GAME_OVER":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button_rect.collidepoint(event.pos):
                            player, score,powerup_timer = reset_game()
                            game_state = "PLAYING"
        
            # --- LOGIC & DRAWING ---
        screen.fill((0, 0, 0))
        
        if game_state == "PLAYING":
                # 1. Update entities
            updatable.update(dt)
            score += PER_SECOND_SCORE * dt
        
                # 2. Check collisions
            for asteroid in asteroids:
                if player.collides_with(asteroid):
                     game_state = "GAME_OVER"  # Instead of sys.exit()
                for shot in shots:
                    if asteroid.collides_with(shot):
                        shot.kill()
                        points = asteroid.split()
                        if points:
                            score += points
            if len(powerups) == 0:
                    powerup_timer -= dt
                    if powerup_timer <= 0:
                        spawn_powerup()
                        powerup_timer = POWERUP_RESPAWN_TIME
            for p_up in powerups:
                if player.collides_with(p_up):
                    player.activate_powerup(duration=10)
                    p_up.kill()
                    powerup_timer = POWERUP_RESPAWN_TIME 
                         
    
                # 3. Draw entities & active score
            for obj in drawable:
                obj.draw(screen)
        
            score_surface = font.render(f"Score: {int(score)}", True, (255, 255, 255))
            screen.blit(score_surface, (10, 10))
        
        elif game_state == "GAME_OVER":
                # Render Game Over text
            game_over_surface = font.render("GAME OVER", True, (255, 0, 0))
            final_score_surface = font.render(f"Final Score: {int(score)}", True, (255, 255, 255))
                
                # Center the text
            screen.blit(game_over_surface, (SCREEN_WIDTH / 2 - game_over_surface.get_width() / 2, SCREEN_HEIGHT / 2 - 60))
            screen.blit(final_score_surface, (SCREEN_WIDTH / 2 - final_score_surface.get_width() / 2, SCREEN_HEIGHT / 2 - 10))
        
                # Draw the button
            pygame.draw.rect(screen, (255, 255, 255), button_rect)
            btn_text = font.render("Restart", True, (0, 0, 0))
            screen.blit(btn_text, (button_rect.centerx - btn_text.get_width() / 2, button_rect.centery - btn_text.get_height() / 2))
        
        pygame.display.flip()


    
if __name__ == "__main__":
    main()
