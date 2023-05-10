import pygame
import random
import sys
from pygame import mixer


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
start_sound = pygame.mixer.Sound('../SFX/game_start.wav')
Hit_sound = pygame.mixer.Sound('../SFX/enemy_hit.wav')
death_sound = pygame.mixer.Sound('../SFX/player_death.wav')
bullet_sound = pygame.mixer.Sound('../SFX/bullet_fire.wav')
Boss_Incoming = pygame.mixer.Sound('../SFX/Boss_incoming.wav')

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
STATE_MENU = 4
STATE_GAMEPLAY = 0
STATE_SETTING = 1
STATE_HELP = 2
STATE_QUIT = 3

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

space = 0

BOSS_MOVE_INTERVAL = 1000

# ID for enemies and bullets. Meant to check death Conditions
ENEMY_1 = 1
ENEMY_2 = 2
BOSS = 3

ENEMY_BULLET = 1
BOSS_BULLET = 2

# Define the death conditions
death_conditions = {
    "Colliding with an enemy ship":(ENEMY_1, ENEMY_2, BOSS),
     "Colliding with an enemy bullet":(ENEMY_BULLET, BOSS_BULLET)
}


################################## Class definition of game object ##################################

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load image of player
        original_image = pygame.image.load(player_frame[active_Frame])
        self.image = pygame.transform.scale(
            original_image, (original_image.get_width() // 2, original_image.get_height() // 2))

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
    global enemy1_bullets
    def __init__(self):
        super().__init__()

        # Load image of enemy1
        self.image = pygame.image.load(enemy1_frame[active_Frame])
        self.type = ENEMY_1

        # Setting the position of enemy1
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -50)

        # Setting speed
        self.speed = random.randrange(8, 12)
        self.hp = 3
        self.shoot_delay = 2000
        self.last_shoot = 0

    # Move enemy1
    def update(self):
        self.rect.y += self.speed

        # If enemy1 go out from screen, reapper on it
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -50)
            self.speed = random.randrange(8, 12)

        # Shoot bullets
        if self.rect.bottom % 100 == 0:
            bullet = Enemy_Bullet(self.rect.centerx, self.rect.centery)
            enemy1_bullets.add(bullet)

    def damage(self):
        self.hp -= 1
        if self.hp == 0:
            self.kill()
            return True
        
    # def shoot(self):
        # current_time = pygame.time.get_ticks()
        # if current_time - self.last_shoot > self.shoot_delay:
        #     self.last_shoot = current_time
        #     bullet = Enemy_Bullet()
        #     enemy1_bullets.add(bullet)

        # if self.rect.bottom > 100:
        #     bullet = Enemy_Bullet(self.rect.centerx, self.rect.centery)
        #     enemy1_bullets.add(bullet)


class Enemy2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load image of enemy2
        original_image = pygame.image.load(enemy2_frame[active_Frame])
        self.image = pygame.transform.scale(
            original_image, (original_image.get_width() * 2, original_image.get_height() * 2))
        self.type = ENEMY_2

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


class Enemy_Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("../Assets/Bullet_Enemy.png")
        self.type = ENEMY_BULLET
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 20
        # self.direction = (math.cos(angle), math.sin(angle))

    def update(self):
        # Move the bullet based on its speed and direction
        # dx = self.speed * self.direction[0]
        # dy = self.speed * self.direction[1]
        # self.rect.move_ip(dx, dy)

        # move bullets up
        self.rect.y += self.speed
        if self.rect.bottom > SCREEN_HEIGHT:
            self.kill()
            

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load image of boss
        original_image = pygame.image.load(boss_frame[active_Frame])
        self.image = pygame.transform.scale(
        original_image, (original_image.get_width() * 2, original_image.get_height() * 2))
        self.type = BOSS

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

    # def shoot_bullet(x, y):


class Boss_bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("../Assets/Bullet_Boss.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        return True


################################## Basic parts of the game ##################################

# Player
player = Player()

# Player_bullet group
player_bullets = pygame.sprite.Group()

# Enemy1 group
enemies1 = pygame.sprite.Group()
for i in range(6):
    enemy1 = Enemy1()
    enemies1.add(enemy1)

# Enemy2 group
enemies2 = pygame.sprite.Group()
for i in range(3):
    enemy2 = Enemy2()
    enemies2.add(enemy2)

# Enemy1_bullet group
enemy1_bullets = pygame.sprite.Group()

# Enemy2_bullet group
enemy2_bullets = pygame.sprite.Group()

# Hit_ememies group
hit_enemies = []

# Boss
bosses = pygame.sprite.Group()
boss = Boss()
bosses.add(boss)

# Boss_bullets

# Time setting of boss
waiting_time = 0
start_time = None
boss_delay = 3000

# Set the max FPS
clock = pygame.time.Clock()
FPS = 40

# Key
# key = pygame.key.get_pressed()

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
                        mixer.music.unload()
                        pygame.mixer.Sound.play(start_sound)
                        mixer.music.load('../Music/stage_music.wav')
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
                    bullet = Player_Bullet(player.rect.centerx - 15, player.rect.top)
                    player_bullets.add(bullet)
                    pygame.mixer.Sound.play(bullet_sound)

                # key = pygame.key.get_pressed()
                # space = (space + 4) * key[pygame.K_SPACE]
                # if space % 1 == 0:
                #     bullet = Player_Bullet(player.rect.centerx - 15, player.rect.top)
                #     player_bullets.add(bullet)
                #     pygame.mixer.Sound.play(bullet_sound)

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
        enemy1_bullets.update()

        # Shoot enemy1's bullets
        # for enemy1 in enemies1:
        #     if enemy1.rect.bottom % 60 == 0:
        #         enemy1_bullet = Enemy_Bullet(enemy1.rect.centerx, enemy1.rect.centery)
        #         enemy1_bullets.add(enemy1_bullet)
        #     enemy1_bullets.update()

        # Updata enemy2
        enemies2.update()

        # Updata bullet
        player_bullets.update()

        # Collision judgement for Player
        for bullet in player_bullets:
            bullet_hits1 = pygame.sprite.spritecollide(bullet, enemies1, False)
            for enemy1 in bullet_hits1:
                bullet.kill()
                pygame.mixer.Sound.play(Hit_sound)
                if enemy1.damage():
                    score += 10
                    new_enemy1 = Enemy1()
                    enemies1.add(new_enemy1)

            bullet_hits2 = pygame.sprite.spritecollide(bullet, enemies2, False)
            for enemy2 in bullet_hits2:
                bullet.kill()
                pygame.mixer.Sound.play(Hit_sound)
                if enemy2.damage():
                    score += 50
                    new_enemy2 = Enemy2()
                    enemies2.add(new_enemy2)

        # Gameover
        for enemy1 in enemies1:
            if player.rect.colliderect(enemy1.rect):
                if enemy1.type in death_conditions["Colliding with an enemy ship"]:
                    pygame.mixer.Sound.play(death_sound)
                    print("Game Over!!")
                    running = False
                
        for bullet in enemy1_bullets:
            if player.rect.colliderect(bullet.rect):
                if bullet.type in death_conditions["Colliding with an enemy bullet"]:
                    pygame.mixer.Sound.play(death_sound)
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
        player_bullets.draw(screen)
        enemy1_bullets.draw(screen)

        # Draw boss
        if score >= 30:
            if start_time is None:
                pygame.mixer.Sound.play(Boss_Incoming)
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