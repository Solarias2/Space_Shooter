import pygame
import random
import sys

# The width and height of Game
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800

# Initialize Pygame and make window
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the background color of the game screen
background_color = (0, 0, 0)
screen.fill(background_color)

player_frame = ['../Assets/player_Frame1.png', '../Assets/player_Frame2.png',
                '../Assets/player_Frame3.png', '../Assets/player_Frame4.png']
enemy1_frame = ['../Assets/enemy1_Frame1.png', '../Assets/enemy1_Frame2.png',
                '../Assets/enemy1_Frame3.png', '../Assets/enemy1_Frame4.png']
enemy2_frame = ['../Assets/enemy2_Frame1.png', '../Assets/enemy2_Frame2.png',
                '../Assets/enemy2_Frame3.png', '../Assets/enemy2_Frame4.png']
boss_frame = ['../Assets/boss_Frame1.png', '../Assets/boss_Frame2.png',
                '../Assets/boss_Frame3.png', '../Assets/boss_Frame4.png']

active_Frame = 0

#########################################################################

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load image of player
        self.image = pygame.image.load(player_frame[active_Frame])

        # Setting the position of player
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = SCREEN_HEIGHT - 50

    # Moveing the player according to the key input
    def update(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            self.rect.x -= 5

        if key[pygame.K_RIGHT]:
            self.rect.x += 5

        if key[pygame.K_UP]:
            self.rect.y -= 5

        if key[pygame.K_DOWN]:
            self.rect.y += 5


class Enemy1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load image of enemy1
        self.image = pygame.image.load(enemy1_frame[active_Frame])

        # Setting the position of enemy1
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -50)

    # Moveing enemy1
    def update(self):
        self.speed = random.randrange(2, 8)
        self.rect.y += self.speed


class Enemy2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load image of enemy2
        self.image = pygame.image.load(enemy2_frame[active_Frame])

        # Setting the position of enemy2
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -50)

    # Moveing enemy2
    def update(self):
        self.speed = random.randrange(5, 15)
        self.rect.y += self.speed


class Boss_Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Load image of bullet
        self.image = pygame.image.load("../Assets/Bullet_Player.png")

        # Setting the position of bullet
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = -10

    def update(self):
        # move bullets up
        self.rect.y += self.speed

        if self.rect.bottom < 0:
            self.kill()  # need to check

#########################################################################

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

clock = pygame.time.Clock()

# Game_loop starts
running = True
while running:
    # Process the events
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Shoot bullets
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # while pygame.time.get_ticks():
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    bullets.add(bullet)

    # Updata player
    player.update()

    # # Updata enemy1
    # enemy1.update()

    # # Updata enemy2
    # enemy2.update()

    # Updata bullet
    bullets.update()

    # Collision judgement
    for bullet in bullets:
        bullet_hits1 = pygame.sprite.spritecollide(bullet, enemies1, True)
        for bullet_hit1 in bullet_hits1:
            bullet.kill()

        bullet_hits2 = pygame.sprite.spritecollide(bullet, enemies2, True)
        for bullet_hit2 in bullet_hits2:
            bullet.kill()

    # Gameover
    player_hits1 = pygame.sprite.spritecollide(player, enemies1, True)
    if player_hits1:
        running = False
        print("Game Over!!")

    player_hits2 = pygame.sprite.spritecollide(player, enemies2, True)
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

    clock.tick(60)

pygame.quit()
