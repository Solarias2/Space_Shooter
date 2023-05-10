import pygame
import math
from pygame.sprite import Group
from variable import SCREEN_HEIGHT, ENEMY_BULLET, BOSS_BULLET

class Player_Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Load image of bullet
        self.image = pygame.image.load("../Assets/Bullet_Player.png")

        # Setting the position of bullet
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = -14

    def update(self):
        # move bullets up
        self.rect.y += self.speed

        if self.rect.bottom < 0:
            self.kill()


class Player_Wide_Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle1, angle2):
        super().__init__()
        # Load image of bullet
        original_img = pygame.image.load("../Assets/Bullet_Player.png")
        self.image = pygame.transform.rotate(original_img, angle1)

        # Setting the position of bullet
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = -14

        # Calculate the velocity components for the bullet
        self.velocity_x = math.cos(math.radians(angle2)) * self.speed
        self.velocity_y = math.sin(math.radians(angle2)) * self.speed

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        if self.rect.bottom < 0:
            self.kill()




class Enemy_Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.image.load("../Assets/Bullet_Enemy.png")
        self.type = ENEMY_BULLET
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed

    def update(self):
        # move bullets down
        self.rect.y += self.speed
        if self.rect.bottom > SCREEN_HEIGHT:
            self.kill()


class Boss_bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.image.load("../Assets/Bullet_Boss.png")
        self.type = BOSS_BULLET
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        # move bullets down
        self.rect.y += self.speed
        if self.rect.bottom > SCREEN_HEIGHT:
            self.kill()


