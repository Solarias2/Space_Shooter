import pygame
import variable


class Explosion(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #Animation Loading
        self.explosion_spritsheet = pygame.image.load("../Assets/explosion.png").convert_alpha()
        self.explosion_H = 100
        self.explosion_W = 100
        self.explosion_animation = []
        self.explosion_Finish = False
        self.sprite_index = 0

        for y in range(0, self.explosion_spritsheet.get_height(), self.explosion_H):
            for x in range(0, self.explosion_spritsheet.get_width(), self.explosion_W):
                self.sprite = self.explosion_spritsheet.subsurface(pygame.Rect(x, y, self.explosion_W, self.explosion_H))
                self.explosion_animation.append(self.sprite)

    def update(self, x, y):
        if not self.explosion_Finish:
            current_sprite = self.explosion_animation[self.sprite_index]
            variable.screen.blit(current_sprite, (x, y))
            self.sprite_index += 1
            if self.sprite_index >= len(self.explosion_animation):
                self.explosion_Finish = True
                self.sprite_index = 0
            else:
               self.explosion_Finish = False