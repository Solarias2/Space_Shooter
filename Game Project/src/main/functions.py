import pygame
from pygame import mixer
from variable import SCREEN_WIDTH, SCREEN_HEIGHT

def music_change(Music):
    mixer.music.stop()
    mixer.music.unload()
    mixer.music.load(Music)
    mixer.music.play(-1)
