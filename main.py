# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main(): 
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    
    AsteroidField.containers = (updatable,)
    Asteroid.containers = (asteroids, updatable,drawable)
    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)


    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroidfield = AsteroidField()
    game_state = "menu"
    high_score = 0
    new_score = 0
    counter = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            if game_state == "menu":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:  # Start Game
                        player.reset()
                        for obj in asteroids:
                            obj.kill()
                        game_state = "game"
                    elif event.key == pygame.K_2:  # Quit Game
                        return
        
                    
        if game_state == "menu":
            screen.fill("black")
            font = pygame.font.Font(None, 70)
            font2 = pygame.font.Font(None, 30)
            start_text = font.render("1. Start game!", True, (255, 255, 255))
            quit_text = font.render("2. Quit game!", True, (255, 255, 255))
            high_score_text = font2.render(f"Highscore:{high_score}", True, "white")
            screen.blit(start_text, (450, 200))
            screen.blit(quit_text, (450,300))
            screen.blit(high_score_text, (30, 50))
            pygame.display.flip()
            continue

        if game_state == "game":
            screen.fill("black")
            font = pygame.font.Font(None, 30)
            new_score_text = font.render(f"Score:{new_score}", True, "white")
            high_score_text = font2.render(f"Highscore:{high_score}", True, "white")
            screen.blit(new_score_text, (30, 50))
            screen.blit(high_score_text, (30, 75))            
            updatable.update(dt)
            counter += 1
            if counter == 120:
                new_score += 1
                counter = 0
            
                      
            for asteroid in asteroids:
                if asteroid.collision(player) == True:
                    if new_score > high_score:
                        high_score = new_score
                    new_score = 0
                    game_state = "menu"
                    break
                for shot in shots:
                    if asteroid.collision(shot) == True:
                        asteroid.split()
                        shot.kill()
                        new_score += 1
        
            for object in drawable:
                object.draw(screen)
            pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()