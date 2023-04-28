import pygame
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


