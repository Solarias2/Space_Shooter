import pygame
import random
from variable import SCREEN_WIDTH, SCREEN_HEIGHT, active_Frame, enemy1_frame, ENEMY_1, enemy1_bullets, enemy2_frame, ENEMY_2, enemy2_bullets
from bullet import Enemy_Bullet

class Enemy1(pygame.sprite.Sprite):

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

        # Enemy1's HP
        self.hp = 3

        # Shoot flag. If it is 0, bullet is not be shot yet. If it is 1, bullet is already shot.
        self.shoot_flag = 0

    # Move enemy1
    def update(self):
        self.rect.y += self.speed

        # If enemy1 go out from screen, reapper on it
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -50)
            self.speed = random.randrange(8, 12)

            # Reset flag
            self.shoot_flag = False

        # Shoot bullets
        self.shoot(15)

    def shoot(self, speed):
        if self.rect.bottom > 300 and self.shoot_flag == False:
            bullet = Enemy_Bullet(self.rect.centerx, self.rect.centery, speed)
            enemy1_bullets.add(bullet)
            self.shoot_flag = True

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
        self.type = ENEMY_2

        # Setting the position of enemy2
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -50)

        # Setting speed
        self.speed = random.randrange(6, 9)

        # Enemy2's HP
        self.hp = 6

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
            self.speed = random.randrange(6, 9)

            # Reset flag
            self.shoot_flag = self.second_shoot_flag = False

        # Shoot bullets
        self.shoot(14)

    def shoot(self, speed):
        if self.rect.bottom > 100 and self.shoot_flag == False:
            bullet = Enemy_Bullet(self.rect.centerx, self.rect.centery, speed)
            enemy2_bullets.add(bullet)
            self.shoot_flag = True

        # if self.rect.bottom > 300 and self.second_shoot_flag == 0:
        #     bullet = Enemy_Bullet(self.rect.centerx, self.rect.centery, 18)
        #     enemy2_bullets.add(bullet)
        #     self.second_shoot_flag = 1

    def damage(self):
        self.hp -= 1
        if self.hp == 0:
            self.kill()
            return True