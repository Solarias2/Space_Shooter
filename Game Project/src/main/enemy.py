import random


class Enemy1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load image of enemy1
        self.image = pygame.image.load("enemy1.png")

        # Setting the position of enemy1
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect)
        self.rect.y = random.randrange(-100, -50)

        # Moveing enemy1
        def update(self):
            self.speed = random.randrange(2, 8)
            self.rect.y += self.speed


class Enemy2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load image of enemy2
        self.image = pygame.image.load("enemy2.png")

        # Setting the position of enemy2
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect)
        self.rect.y = random.randrange(-100, -50)

        # Moveing enemy2
        def update(self):
            self.speed = random.randrange(5, 15)
            self.rect.y += self.speed


class Boss_Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
