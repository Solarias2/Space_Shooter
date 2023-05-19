import pygame
import variable
import os

# # In this class, split explosion.png to create an explosion animation.
# class Explosion(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__()
#         #Animation Loading
#         self.explosion_spritsheet = pygame.image.load('../Assets/explosion.png').convert_alpha()
#         self.explosion_H = 100
#         self.explosion_W = 80
#         self.explosion_animation = []
#         self.sprite_index = 0
#         self.explosion_flag = False

#         # Split explosion.png and store each image in self.explosion_animation
#         for y in range(0, self.explosion_H, self.explosion_spritsheet.get_height()):
#             for x in range(0, self.explosion_W, self.explosion_spritsheet.get_width()):
#                 self.sprite = self.explosion_spritsheet.subsurface(pygame.Rect(x, y, self.explosion_W, self.explosion_H))
#                 self.explosion_animation.append(self.sprite)

#         self.x = x
#         self.y = y

#     # Animation
#     def update(self):
#         # if self.explosion_flag:
#             current_sprite = self.explosion_animation[self.sprite_index]
#             # Render image at current index
#             variable.screen.blit(current_sprite, (self.x, self.y))
#             self.sprite_index += 1
#             if self.sprite_index >= len(self.explosion_animation):
#                 self.kill()


# Explosion effect
# explosion = pygame.sprite.Group()

# class Explosion(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__()
#         #Animation Loading
#         self.image = pygame.image.load("../Assets/player_Frame1.png").convert_alpha()
#         self.rect = self.image.get_rect()

#         self.rect.centerx = x
#         self.rect.centery = y

#     def update(self):
#         variable.screen.blit(self.image, [self.rect.centerx, self.rect.centery])

# In this class use each images originally divided

explosion_animation = [
    ('../Assets/explosions/explosion_Frame_1.png'),
    ('../Assets/explosions/explosion_Frame_2.png'),
    ('../Assets/explosions/explosion_Frame_3.png'),
    ('../Assets/explosions/explosion_Frame_4.png'),
    ('../Assets/explosions/explosion_Frame_5.png'),
    ('../Assets/explosions/explosion_Frame_6.png'),
    ('../Assets/explosions/explosion_Frame_7.png'),
    ('../Assets/explosions/explosion_Frame_8.png'),
    ('../Assets/explosions/explosion_Frame_9.png'),
    ('../Assets/explosions/explosion_Frame_10.png'),
    ('../Assets/explosions/explosion_Frame_11.png'),
    ('../Assets/explosions/explosion_Frame_12.png'),
    ('../Assets/explosions/explosion_Frame_13.png'),
    ('../Assets/explosions/explosion_Frame_14.png'),
    ('../Assets/explosions/explosion_Frame_15.png'),
    ('../Assets/explosions/explosion_Frame_16.png')
]

def make_explosion(x, y):
    sprite_index = 0
    frame_delay = 5
    frame_counter = 0
    frame_counter += 1
    if frame_counter >= frame_delay:
        frame_counter = 0
        sprite_index += 1

        if sprite_index >= len(explosion_animation):
            pass
        else:
            current_sprite = explosion_animation[sprite_index]
            variable.screen.blit(current_sprite,
                                 (x, y))

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.explosion_animation = []
        self.sprite_index = 0
        self.frame_delay = 1
        self.frame_counter = 0
        self.x = x
        self.y = y

        for img_path in explosion_animation:
            image = pygame.image.load(img_path).convert_alpha()
            self.explosion_animation.append(image)

        self.image = self.explosion_animation[self.sprite_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0
            self.sprite_index += 1

            if self.sprite_index >= len(self.explosion_animation):
                self.kill()
            else:
                self.image = self.explosion_animation[self.sprite_index]
                self.rect = self.image.get_rect(center=(self.x, self.y))
        
        variable.screen.blit(self.image, self.rect)