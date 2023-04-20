import pygame
import random
import sys


################################## Setting of game ##################################

# The width and height of Game
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

# Initialize Pygame and make window
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the background color of the game screen
background_color = (0, 0, 0)
screen.fill(background_color)

# Object image
player_frame = ['../Assets/player_Frame1.png', '../Assets/player_Frame2.png',
                '../Assets/player_Frame3.png', '../Assets/player_Frame4.png']
enemy1_frame = ['../Assets/enemy1_Frame1.png', '../Assets/enemy1_Frame2.png',
                '../Assets/enemy1_Frame3.png', '../Assets/enemy1_Frame4.png']
enemy2_frame = ['../Assets/enemy2_Frame1.png', '../Assets/enemy2_Frame2.png',
                '../Assets/enemy2_Frame3.png', '../Assets/enemy2_Frame4.png']
boss_frame = ['../Assets/boss_Frame1.png', '../Assets/boss_Frame2.png',
              '../Assets/boss_Frame3.png', '../Assets/boss_Frame4.png']

active_Frame = 0


################################## Class definition of game object ##################################

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load image of player
        # original_image = pygame.image.load(player_frame[active_Frame]) # need to check
        # self.image = pygame.transform.scale(original_image, (original_image.get_width//2, original_image.get_height//2)) # need to check
        self.image = pygame.image.load(player_frame[active_Frame])

        # Setting the position of player
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = SCREEN_HEIGHT - 10

        self.speed = 13

    # Moveing the player according to the key input
    def update(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if key[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if key[pygame.K_UP]:
            self.rect.y -= self.speed

        if key[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Stay on screen
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


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
            self.kill()

    # Collision judgement
    def hits_enemy(self, enemies):
        # if (self.rect.x > enemy.rect.x and self.rect.x < enemy.rect.x + enemy.rect.width) and (self.rect.y > enemy.rect.y and self.rect.y < enemy.rect.y + enemy.rect.height):
        #     return True
        
        # else:
        #     return False

        hit_enemies = pygame.sprite.spritecollide(bullet, enemies, True)
        for enemy in hit_enemies:
            enemy.damage()

class Enemy1(pygame.sprite.Sprite):
    def __init__(self, id):
        super().__init__()

        # Load image of enemy1
        self.image = pygame.image.load(enemy1_frame[active_Frame])

        # Setting the position of enemy1
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -50)
        self.speed = random.randrange(8, 12)
        self.hp = 2
        self.id = id

    # Move enemy1
    def update(self):
        self.rect.y += self.speed

        # If enemy1 go out from screen, reapper on it
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -50)
            self.speed = random.randrange(8, 12)

    def damage(self):
        self.hp -= 1
        if self.hp == 0:
            self.kill()

    def reset(self):
        self.hp = 2

class Enemy2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load image of enemy2
        self.image = pygame.image.load(enemy2_frame[active_Frame])

        # Setting the position of enemy2
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -50)
        self.speed = random.randrange(5, 15)

    # Move enemy2
    def update(self):
        self.rect.y += self.speed

        # If enemy1 go out from screen, reapper on it
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -50)
            self.speed = random.randrange(5, 15)


class Boss_Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()


################################## Basic parts of the game ##################################

# Make Player
player = Player()

# Make enemy1 group
enemies1 = pygame.sprite.Group()
enemy1_id = 0
for i in range(6):
    enemy1 = Enemy1(enemy1_id)
    enemies1.add(enemy1)
    enemy1_id += 1

enemy1_hp = {enemy1.id: enemy1.hp for enemy1 in enemies1}

# Make enemy2 group
enemies2 = pygame.sprite.Group()
for i in range(3):
    enemy2 = Enemy2()
    enemies2.add(enemy2)

# Make bullet group
bullets = pygame.sprite.Group()

# Hit ememies group
hit_enemies = []

clock = pygame.time.Clock()

# Game_loop
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
                bullet = Bullet(player.rect.centerx - 15, player.rect.top)
                bullets.add(bullet)

    # Updata player
    player.update()

    # Updata enemy1
    enemies1.update()

    # Updata enemy2
    # enemies2.update()

    # Updata bullet
    bullets.update()

    # Collision judgement
    for bullet in bullets:
        bullet_hits1 = pygame.sprite.spritecollide(bullet, enemies1, True)
        for enemy1 in bullet_hits1:
            bullet.kill()
            enemy1.damage()
            new_enemy1 = Enemy1()
            enemies1.add(new_enemy1)

        bullet_hits2 = pygame.sprite.spritecollide(bullet, enemies2, True)
        for bullet_hit2 in bullet_hits2:
            bullet.kill()
            new_enemy2 = Enemy2()
            enemies2.add(new_enemy2)

    # Collision judgement2
    # for bullet in bullets:
    #     for enemy1 in enemies1:
    #         if bullet.hits_enemy(enemy1):
    #             hit_enemies.append(enemy1)
    #             bullet.kill()
    #             break

    # # Treat hit enemies collectively
    # for enemy in hit_enemies:
    #     enemy.hp -= 1
    #     if enemy.hp == 0:
    #         enemy.kill()
    #         new_enemy1 = Enemy1()
    #         enemies1.add(new_enemy1)

    # Collision judgement3
    # for bullet in bullets:
    #         bullet.hits_enemy(enemies1)

    # Gameover
    player_hits1 = pygame.sprite.spritecollide(player, enemies1, True)
    if player_hits1:
        print("Game Over!!")
        running = False

    player_hits2 = pygame.sprite.spritecollide(player, enemies2, True)
    if player_hits2:
        print("Game Over!!")
        running = False

    # Draw the player, enemies, and bullet
    screen.blit(player.image, player.rect)
    enemies1.draw(screen)
    enemies2.draw(screen)
    bullets.draw(screen)

    # Update screen
    pygame.display.flip()

    clock.tick(40)

pygame.quit()
