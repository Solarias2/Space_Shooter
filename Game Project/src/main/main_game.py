import pygame
import random

# The width and height of Game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

# Initialize Pygame and make window
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the background color of the game screen
background_color = (0, 0, 0)
screen.fill(background_color)

# Make Player
player = Player()

# Make Enemy1 Group
enemies1 = pygame.sprite.Group()
for i in range(10):
    enemy1 = Enemy1()
    enemies1.add(enemy1)

# Make Enemy2 Group
enemies2 = pygame.sprite.Group()
for i in range(10):
    enemy2 = Enemy2()
    enemies2.add(enemy2)

# Make Bullet Group
bullets = pygame.sprite.Group()


# Game_loop starts
running = True
while running:
    # Process the events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running == False

        # Shoot bullets
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.top)
                bullets.add(bullet)

    # Updata player
    player.update()

    # Updata enemy1
    enemy1.update()

    # Updata enemy2
    enemy2.update()

    # Updata bullet
    bullet.update()

    # Collision judgement
    for bullet in bullets:
        bullet_hits1 = pygame.sprite.spritecollide(bullet, enemies1, True)
        for bullet_hit1 in bullet_hits1:
            bullet.kill()

        bullet_hits2 = pygame.sprite.spritecollide(bullet, enemies2, True)
        for bullet_hit2 in bullet_hits2:
            bullet.kill()

    # Gameover
    player_hits1 = pygame.sprite.spritecollide(player, enemies1)
    if player_hits1:
        running = False
        print("Game Over!!")

    player_hits2 = pygame.sprite.spritecollide(player, enemies2)
    if player_hits2:
        running = False
        print("Game Over!!")

    # Draw the player, enemies, and bullet
    screen.blit(player.image, player.rect)
    enemies1.draw(screen)
    enemies2.draw(screen)
    bullets.draw(screen)

    # Update screen
    pygame.display.flip()

pygame.quit()