class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Load image of bullet
        self.image = pygame.image.load("bullet.png")

        # Setting the position of bullet
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speed = -10

        def update(self):
            # move bullets up
            self.rect.y += self.speed

            if self.rect_x < 0:
                self.kill() # need to check










