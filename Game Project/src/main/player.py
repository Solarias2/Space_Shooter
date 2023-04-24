import pygame
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