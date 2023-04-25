import pygame
import random
import sys
from pygame import mixer
import player



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

pre_bg_img = pygame.image.load("../Assets/bgimg.jpeg")
bg_img = pygame.transform.scale(pre_bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
bg_y = 0

# Starts up menu music
mixer.music.load('../Music/menu_music.wav')
mixer.music.play(-1)

# Object image
player_frame = ['../Assets/player_Frame1.png', '../Assets/player_Frame2.png',
                '../Assets/player_Frame3.png', '../Assets/player_Frame4.png']
enemy1_frame = ['../Assets/enemy1_Frame1.png', '../Assets/enemy1_Frame2.png',
                '../Assets/enemy1_Frame3.png', '../Assets/enemy1_Frame4.png']
enemy2_frame = ['../Assets/enemy2_Frame1.png', '../Assets/enemy2_Frame2.png',
                '../Assets/enemy2_Frame3.png', '../Assets/enemy2_Frame4.png']
boss_frame = ['../Assets/Boss.png']

active_Frame = 0

# Create a font of menu option
menu_font = pygame.font.Font(None, 36)

# Game States
STATE_MENU = 0
STATE_GAMEPLAY = 1

# Current state
game_state = STATE_MENU

# Define munu options
menu_options = [
    "Start Game",
    "Settings",
    "Help",
    "Quit"
]

# Loop through the menu options and create a menu item for each one
menu_items = []
for index, option in enumerate(menu_options):
    text = menu_font.render(option, True, (255, 255, 255))
    rect = text.get_rect()
    rect.centerx = screen.get_rect().centerx
    rect.centery = screen.get_rect().centery + index * 50
    menu_items.append((option, text, rect))

# Set the default menu option to the first one
menu_index = 0

# Create a font of score
score_font = pygame.font.Font(None, 36)

score = 0

BOSS_MOVE_INTERVAL = 1000


################################## Class definition of game object ##################################



class Player_Bullet(pygame.sprite.Sprite):
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


class Enemy1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load image of enemy1
        self.image = pygame.image.load(enemy1_frame[active_Frame])

        # Setting the position of enemy1
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -50)
        self.speed = random.randrange(8, 12)
        self.hp = 3

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
            return True


class Enemy2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load image of enemy2
        original_image = pygame.image.load(enemy2_frame[active_Frame])
        self.image = pygame.transform.scale(
            original_image, (original_image.get_width() * 2, original_image.get_height() * 2))

        # Setting the position of enemy2
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -50)
        self.speed = random.randrange(5, 15)
        self.hp = 6

    # Move enemy2
    def update(self):
        self.rect.y += self.speed

        # If enemy2 go out from screen, reapper on it
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -50)
            self.speed = random.randrange(11, 15)

    def damage(self):
        self.hp -= 1
        if self.hp == 0:
            self.kill()
            return True


class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load image of boss
        original_image = pygame.image.load(boss_frame[active_Frame])
        self.image = pygame.transform.scale(
            original_image, (original_image.get_width() * 2, original_image.get_height() * 2))

        self.last_move_time = pygame.time.get_ticks()

        # Setting the position of boss
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = 250
        self.hp = 50

    def update(self):
        self.delay = clock.tick(10000)

        # Check if it's time to move the boss
        now = pygame.time.get_ticks()
        if now - self.last_move_time >= BOSS_MOVE_INTERVAL:
            self.last_move_time = now

            # Move the boss in a random direction
            self.speedx = random.randint(-15, 15)
            self.speedy = random.randint(-10, 10)
        self.rect.move_ip(self.speedx, self.speedy)

        # Keep the boss on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > SCREEN_HEIGHT / 2 + 100:
            self.rect.bottom = SCREEN_HEIGHT / 2 + 100


class Enemy_Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.image.load("../Assets/Bullet_Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 6
        # self.direction = (math.cos(angle), math.sin(angle))

    def update(self):
        # Move the bullet based on its speed and direction
        dx = self.speed * self.direction[0]
        dy = self.speed * self.direction[1]
        self.rect.move_ip(dx, dy)

        # move bullets up
        self.rect.y += self.speed

        if self.rect.bottom < 0:
            self.kill()


################################## Basic parts of the game ##################################

# Make Player
player = player.Player()

# Make enemy1 group
enemies1 = pygame.sprite.Group()
for i in range(6):
    enemy1 = Enemy1()
    enemies1.add(enemy1)

# Make enemy2 group
enemies2 = pygame.sprite.Group()
for i in range(3):
    enemy2 = Enemy2()
    enemies2.add(enemy2)

# Make bullet group
bullets = pygame.sprite.Group()

# Hit ememies group
hit_enemies = []

# Boss
bosses = pygame.sprite.Group()
boss = Boss()
bosses.add(boss)

# Boss bullets

# Time setting of boss
waiting_time = 0
start_time = None
boss_delay = 3000

# Set the max FPS
clock = pygame.time.Clock()
FPS = 120

# Game_loop
running = True
while running:
    # Process the events
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if game_state == STATE_MENU:
                if event.key == pygame.K_UP:
                    # Move the menu index up
                    menu_index = (menu_index - 1) % len(menu_items)

                elif event.key == pygame.K_DOWN:
                    # Move the menu index down
                    menu_index = (menu_index + 1) % len(menu_items)

                elif event.key == pygame.K_RETURN:
                    # Check which menu option was selected
                    if menu_index == 0:
                        game_state = STATE_GAMEPLAY
                        mixer.music.stop()
                        pygame.mixer.Sound.play('../SFX/game_start.wav')
                        mixer.music.load('../Music/Stage_music.wav')
                        mixer.music.play(-1)

                    elif menu_index == 1:
                        pass

                    elif menu_index == 2:
                        pass

                    elif menu_index == 3:
                        pygame.quit()
                        sys.exit()

            if game_state == STATE_GAMEPLAY:
                # Shoot bullets
                if event.key == pygame.K_SPACE:
                    # while pygame.time.get_ticks():
                    bullet = Player_Bullet(
                        player.rect.centerx - 15, player.rect.top)
                    bullets.add(bullet)

    # Process according to the game state
    if game_state == STATE_MENU:
        # Draw menu screen
        for index, item in enumerate(menu_items):
            if index == menu_index:
                # Selected items are drawn in white
                screen.blit(item[1], item[2])
            else:
                # Unselected items are drawn in gray
                screen.blit(menu_font.render(
                    item[0], True, (128, 128, 128)), item[2])

    elif game_state == STATE_GAMEPLAY:
        # Draw score on surface object
        score_surface = score_font.render(
            "Score: " + str(score), True, (255, 255, 255))

        # Updata player
        player.update()

        # Updata enemy1
        enemies1.update()

        # Updata enemy2
        enemies2.update()

        # Updata bullet
        bullets.update()

        # Collision judgement
        for bullet in bullets:
            bullet_hits1 = pygame.sprite.spritecollide(bullet, enemies1, False)
            for enemy1 in bullet_hits1:
                bullet.kill()
                if enemy1.damage():
                    score += 10
                    new_enemy1 = Enemy1()
                    enemies1.add(new_enemy1)

            bullet_hits2 = pygame.sprite.spritecollide(bullet, enemies2, False)
            for enemy2 in bullet_hits2:
                bullet.kill()
                if enemy2.damage():
                    score += 50
                    new_enemy2 = Enemy2()
                    enemies2.add(new_enemy2)

        # Gameover
        player_hits1 = pygame.sprite.spritecollide(player, enemies1, True)
        if player_hits1:
            print("Game Over!!")
            running = False

        player_hits2 = pygame.sprite.spritecollide(player, enemies2, True)
        if player_hits2:
            print("Game Over!!")
            running = False

        # Draw background and scroll
        bg_y = (bg_y + 8) % 900
        screen.blit(bg_img, [0, bg_y])
        screen.blit(bg_img, [0, bg_y - 900])

        # Display Surface objects on screen
        screen.blit(score_surface, (10, 10))

        # Draw the player, enemies, and bullet
        screen.blit(player.image, player.rect)
        enemies1.draw(screen)
        enemies2.draw(screen)
        bullets.draw(screen)

        # Draw boss
        if score >= 10:
            if start_time is None:
                start_time = pygame.time.get_ticks()
                enemies1.empty()
                enemies2.empty()

            waiting_time = pygame.time.get_ticks() - start_time

            if waiting_time > boss_delay:
                bosses.draw(screen)

            bosses.update()  # Need to make

    # Update screen
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
