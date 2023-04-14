import random


class Enemy1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load image of enemy1
        enemy1_image = pygame.image.load("enemy1.png")

        # Setting the position of enemy1
        enemy1_rect = self.image.get_rect()
        enemy1_rect_x = random.randrange(SCREEN_WIDTH - enemy1_rect)
        enemy1_rect_y = random.randrange(-100, -50)

        # Moveing enemy1
        def update(self):
            enemy1_speed = random.randrange(2, 8)
            enemy1_rect_y += enemy1_speed


class Enemy2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load image of enemy2
        enemy2_image = pygame.image.load("enemy2.png")

        # Setting the position of enemy2
        enemy2_rect = self.image.get_rect()
        enemy2_rect_x = random.randrange(SCREEN_WIDTH - enemy2_rect)
        enemy2_rect_y = random.randrange(-100, -50)

        # Moveing enemy2
        def update(self):
            enemy2_speed = random.randrange(5, 15)
            enemy2_rect_y += enemy1_speed


class Boss_Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
