# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame, sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

pygame.init()
font = pygame.font.SysFont("Times New Roman", 24)

def main():
    asteroids_killed = 0
    lives_remaining = 1
    
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    Shot.containers = (shots, updatable, drawable)

    while pygame.get_init():
        score = font.render(f"Score: {asteroids_killed}", False, "white", "black")  
        lives = font.render(f"Lives: {lives_remaining}", False, "white", "black")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        updatable.update(dt)
        for asteroid in asteroids:
            for shot in shots:
                if shot.collision(asteroid):
                    shot.kill()
                    if asteroid.split():
                        asteroids_killed += 1
            if asteroid.collision(player):            
                player.kill()
                drawable.empty()
                asteroids.empty()
                shots.empty()
                lives_remaining -= 1

                if lives_remaining == -1:
                    game_over(asteroids_killed)

                player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        screen.fill("black")
        screen.blit(score, (0, 0))
        screen.blit(lives, (0, 24))
        for obj in drawable:
            obj.draw(screen)
        
        pygame.display.flip()
        dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

def game_over(score):
    print("broke out of loop")
    pygame.display.quit()
    screen = pygame.display.set_mode((300, 100))
    score_text = font.render(f"Final Score: {score}", False, "white", "black")
    score_text_width = score_text.get_width()
    score_text_height = score_text.get_height()
    center_x = 150 - score_text_width / 2
    center_y = 50 - score_text_height / 2
    screen.blit(score_text, (center_x, center_y))
    print(f"Game over!\nYou destroyed {score} asteroids!")
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


if __name__ == "__main__":
    main()