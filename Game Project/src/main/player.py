import pygame
from variable import SCREEN_WIDTH, SCREEN_HEIGHT, active_Frame, player_frame, bullet_sound, player_bullets
from bullet import Player_Bullet

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

        self.bullet_delay = 150
        self.last_shot = pygame.time.get_ticks()

        # Player's HP
        self.hp = 5

        # Setting speed
        self.speed = 15

        # Shoot_flag
        self.shoot_flag = False

        # Damage_flag
        self.damage_flag = False

        # Invincible time
        self.invincible = 50

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

        self.shoot()

    def shoot(self):
        now = pygame.time.get_ticks()
        if self.shoot_flag and now - self.last_shot >= self.bullet_delay:
            self.last_shot = now
            bullet = Player_Bullet(self.rect.centerx - 15, self.rect.top)
            player_bullets.add(bullet)
            pygame.mixer.Sound.play(bullet_sound)

    def damage(self):
        self.hp -= 1
        self.damage_flag = True
        if self.hp == 0:
            return True