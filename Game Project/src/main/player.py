import pygame
from variable import SCREEN_WIDTH, SCREEN_HEIGHT, active_Frame, player_frame, bullet_sound, player_bullets
from bullet import Player_Bullet, Player_Wide_Bullet

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
        self.rect.bottom = SCREEN_HEIGHT

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

        # Powerup flag
         # For item1
        self.multi = False

         # For item2
        self.wide = False

         # For item3
        self.fast = False

         # For item4
        self.berserk = False

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

        if self.rect.bottom > SCREEN_HEIGHT - 60:
            self.rect.bottom = SCREEN_HEIGHT - 60

        self.shoot()

    def shoot(self):
        # Continue to shoot bullets while holding space bar.
        now = pygame.time.get_ticks()
        bullet_delay = [150, 100]

        if self.fast == True or self.berserk == True:
            self.bullet_delay = bullet_delay[1]
        elif not self.fast and not self.berserk:
            self.bullet_delay = bullet_delay[0]

        if self.shoot_flag and now - self.last_shot >= self.bullet_delay:
            self.last_shot = now
            bullet = Player_Bullet(self.rect.centerx - 11, self.rect.top)
            player_bullets.add(bullet)
            pygame.mixer.Sound.play(bullet_sound)

            # While being powered up woth item1, player can shoot 3 bullet3.
            if self.multi or self.berserk:
                right_bullet = Player_Bullet(self.rect.centerx + 10, self.rect.top)
                left_bullet = Player_Bullet(self.rect.centerx - 30, self.rect.top)
                player_bullets.add(right_bullet)
                player_bullets.add(left_bullet)

            if self.wide or self.berserk:
                right_bullet = Player_Wide_Bullet(self.rect.left + 40, self.rect.centery - 25, 125, 150)
                left_bullet = Player_Wide_Bullet(self.rect.right - 83, self.rect.centery - 25, 55, 30)
                player_bullets.add(right_bullet)
                player_bullets.add(left_bullet)

            

    # 
    def damage(self):
        self.hp -= 1
        self.damage_flag = True
        if self.hp == 0:
            return True
        
    def game_over(self):
        self.kill()