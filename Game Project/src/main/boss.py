import pygame
import random
from variable import SCREEN_WIDTH, SCREEN_HEIGHT, boss_frame, active_Frame, BOSS, BOSS_MOVE_INTERVAL, boss_bullets
from bullet import Boss_bullet, Enemy_Bullet

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load image of boss
        original_image = pygame.image.load(boss_frame[active_Frame])
        self.image = pygame.transform.scale(
            original_image, (original_image.get_width() * 1.5, original_image.get_height() * 1.5))
        self.type = BOSS

        self.last_move_time = pygame.time.get_ticks()
        self.bullet_delay = 1500
        self.last_shot = pygame.time.get_ticks()

        # Setting the position of boss
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = 250

        # Boss's HP
        self.hp = 50

    def update(self):
        # Check if it's time to move the boss
        now = pygame.time.get_ticks()
        if now - self.last_move_time >= BOSS_MOVE_INTERVAL:
            self.last_move_time = now

            # Move the boss in a random direction
            self.speedx = random.randint(-18, 18)
            self.speedy = random.randint(-10, 10)

        self.rect.move_ip(self.speedx, self.speedy)

        # Keep the boss on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT / 2 + 100:
            self.rect.bottom = SCREEN_HEIGHT / 2 + 100

        # Shoot bullets
        self.shoot(15)

    def shoot(self, speed):
        now = pygame.time.get_ticks()
        if now - self.last_shot >= self.bullet_delay:
            self.last_shot = now
            Main_bullet = Boss_bullet(self.rect.centerx, self.rect.centery, speed)
            boss_bullets.add(Main_bullet)
            Right_bullet = Enemy_Bullet(self.rect.centerx + 70, self.rect.centery, speed)
            boss_bullets.add(Right_bullet)
            Left_bullet = Enemy_Bullet(self.rect.centerx - 50, self.rect.centery, speed)
            boss_bullets.add(Left_bullet)

    def damage(self):
        self.hp -= 1
        if self.hp == 0:
            self.kill()
            return True