class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load image of player
        player_image = pygame.image.load("player.png")

        # Setting the position of player
        player_rect = self.image.get_rect()
        player_rect_x = SCREEN_WIDTH / 2
        player_rect_y = SCREEN_HEIGHT - 50

        # Moveing the player according to the key input
        def update(self):
            key = pygame.key.get_pressed()

            if key[K_LEFT]:
                player_rect_x -= 5

            if key[K_RIGHT]:
                player_rect_x += 5

            if key[K_UP]:
                player_rect_y -= 5

            if key[K_DOWN]:
                player_rect_y += 5
