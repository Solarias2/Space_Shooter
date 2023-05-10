import pygame
import random
import variable
from variable import SCREEN_WIDTH, SCREEN_HEIGHT, active_Frame, enemy1_frame, ENEMY_1, enemy2_frame, ENEMY_2,enemies, enemy_bullets
from bullet import Enemy_Bullet

class Enemy1(pygame.sprite.Sprite):
    def __init__(self, diff):
        super().__init__()

        # Load image of enemy1
        self.image = pygame.image.load(enemy1_frame[active_Frame])
        self.type = ENEMY_1
        self.diff = diff

        # Setting the position of enemy1
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -50)

        # Setting speed and HP
        hp = [2, 1, 4]
        if diff == variable.EASY_DIFF:
            self.speed = random.randrange(5, 9)
        if diff == variable.MED_DIFF:
            self.speed = random.randrange(8, 12)
        if diff == variable.HARD_DIFF:
            self.speed = random.randrange(12, 16)
        self.hp = hp[self.diff]

        # Shoot flag. If it is 0, bullet is not be shot yet. If it is 1, bullet is already shot.
        self.shoot_flag = 0

    # Move enemy1
    def update(self):
        self.rect.y += self.speed

        # If enemy1 go out from screen, reapper on it
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -50)
            if self.diff == variable.EASY_DIFF:
                self.speed = random.randrange(5, 9)
            if self.diff == variable.MED_DIFF:
                self.speed = random.randrange(8, 12)
            if self.diff == variable.HARD_DIFF:
                self.speed = random.randrange(12, 16)

            # Reset flag
            self.shoot_flag = False

        # Shoot bullets
        self.shoot()

    # Shoot bullets
    def shoot(self):
        speed = [15, 12, 19]
        if self.rect.bottom > 300 and self.shoot_flag == False:
            bullet = Enemy_Bullet(self.rect.centerx, self.rect.centery, speed[self.diff])
            enemy_bullets.add(bullet)
            self.shoot_flag = True

    # Decrease HP
    def damage(self):
        self.hp -= 1
        if self.hp == 0:
            self.kill()
            return True
        
    # Add a new Enemy1
    def new_add(self):
        new_enemy1 = Enemy1()
        enemies.add(new_enemy1)
        

class Enemy2(pygame.sprite.Sprite):
    def __init__(self, diff):
        super().__init__()

        # Load image of enemy2
        original_image = pygame.image.load(enemy2_frame[active_Frame])
        self.image = pygame.transform.scale(
            original_image, (original_image.get_width() * 2, original_image.get_height() * 2))
        self.type = ENEMY_2
        self.diff = diff

        # Setting the position of enemy2
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -50)

        # Setting speed and HP
        hp = [5, 3, 7]
        if diff == variable.EASY_DIFF:
            self.speed = random.randrange(5, 9)
        if diff == variable.MED_DIFF:
            self.speed = random.randrange(8, 12)
        if diff == variable.HARD_DIFF:
            self.speed = random.randrange(12, 16)

        self.hp = hp[self.diff]

        # Shoot flag. If it is 0, bullet is not be shot yet. If it is 1, bullet is already shot.
        self.shoot_flag = False
        self.second_shoot_flag = False

    # Move enemy2
    def update(self):
        self.rect.y += self.speed

        # If enemy2 go out from screen, reapper on it
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -50)
            if self.diff == variable.EASY_DIFF:
                self.speed = random.randrange(5, 9)
            if self.diff == variable.MED_DIFF:
                self.speed = random.randrange(8, 12)
            if self.diff == variable.HARD_DIFF:
                self.speed = random.randrange(12, 16)

            # Reset flag
            self.shoot_flag = self.second_shoot_flag = False

        # Shoot bullets
        self.shoot()

    # Shoot bullets
    def shoot(self):
        speed = [14, 11, 18]
        if self.rect.bottom > 100 and self.shoot_flag == False:
            bullet = Enemy_Bullet(self.rect.centerx, self.rect.centery, speed[self.diff])
            enemy_bullets.add(bullet)
            self.shoot_flag = True

    # Decrease HP
    def damage(self):
        self.hp -= 1
        if self.hp == 0:
            self.kill()
            return True
        
    # Add a new Enemy2
    def new_add(self):
        new_enemy2 = Enemy2()
        enemies.add(new_enemy2)