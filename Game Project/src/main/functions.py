import pygame
from pygame import mixer
from variable import SCREEN_WIDTH, SCREEN_HEIGHT

def music_change(Music):
    mixer.music.stop()
    mixer.music.unload()
    mixer.music.load(Music)
    mixer.music.play(-1)

def blit_text(surface, text, pos, font, color=pygame.Color('white')):
    words = [word.split(' ')for word in text.splitlines()]
    space = font.size(' ')[0]
    max_width, max_height = surface.get_size()
    x,y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]
                y += word_height
            surface.blit(word_surface, (x,y))
            x += word_width + space 
        x= pos[0]
        y += word_height
