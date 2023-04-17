class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load image of player
        self.image = pygame.image.load("player.png")

        # Setting the position of player
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = SCREEN_HEIGHT - 50

        # Moveing the player according to the key input
        def update(self):
            key = pygame.key.get_pressed()

            if key[K_LEFT]:
                self.rect.centerx -= 5

            if key[K_RIGHT]:
                self.rect.centerx += 5

            if key[K_UP]:
                self.rect.bottom -= 5

            if key[K_DOWN]:
                self.rect.bottom += 5
