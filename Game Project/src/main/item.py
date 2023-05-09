import pygame
import random
import variable

# Item for multi bullet
class Item1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load image of item1
        self.image = pygame.image.load("../Assets/Multi_Shot.png")

        # Setting the position of item1
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(variable.SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -50)

        # Setting speed
        self.speed = 10

        # Delay
        self.delay = 8000
        self.last_appear = pygame.time.get_ticks()

        # Type
        self.type = variable.multi

        # Display flag. While player is powered up, not display item
        self.display_flag = True 

    # Move item1
    def update(self):
        self.rect.y += self.speed

        if self.rect.top > variable.SCREEN_HEIGHT:
            self.kill()


# Item for wide bullet
class Item2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load image of item2
        self.image = pygame.image.load("../Assets/Wide_Shot.png")

        # Setting the position of item2
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(variable.SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -50)

        # Setting speed
        self.speed = 13

        # Type
        self.type = variable.wide

    # Move item2
    def update(self):
        self.rect.y += self.speed

        if self.rect.top > variable.SCREEN_HEIGHT:
            self.kill()


# Item for fast bullet
class Item3(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load image of item1
        self.image = pygame.image.load("../Assets/Fast_Shot.png")

        # Setting the position of item3
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(variable.SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -50)

        # Setting speed
        self.speed = 12

        # Type
        self.type = variable.fast

    # Move item3
    def update(self):
        self.rect.y += self.speed

        if self.rect.top > variable.SCREEN_HEIGHT:
            self.kill()


# Item for berserk bullet
class Item4(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load image of item4
        self.image = pygame.image.load("../Assets/Berserk_Shot.png")

        # Setting the position of item4
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(variable.SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -50)

        # Setting speed
        self.speed = 9

        # Type
        self.type = variable.berserk

    # Move item4
    def update(self):
        self.rect.y += self.speed

        if self.rect.top > variable.SCREEN_HEIGHT:
            self.kill()


# Item for cure
class heart(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("../Assets/Heart.png")
        self.rect.x = random.randrange(variable.SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(variable.SCREEN_HEIGHT - self.rect.height)

        # Type
        self.type = variable.heart