
import pygame
import sys

img_bg = pygame.image.load("bgimage.png")
img_player = pygame.image.load("player1.png")
img_weapon = pygame.image.load("bullet.png")
bg_y = 0
px = 320 #プレイヤーのX座標
py = 240 #プレイヤーのY座標
bx = 0 #弾のX座標
by = 0 #弾のY座標
space = 0
BULLET_MAX = 100 #弾の最大値
bull_n = 0
bull_x =[0]*BULLET_MAX
bull_y =[0]*BULLET_MAX
bull_f =[False]*BULLET_MAX

def set_bullet():#弾のスタンバイ
    global bull_n
    bull_f[bull_n] = True
    bull_x[bull_n] = px-16
    bull_y[bull_n] = py-32
    bull_n = (bull_n+1)%BULLET_MAX

def move_bullet(screen):#弾を飛ばす
    for i in range(BULLET_MAX):
        if bull_f[i] == True:
            bull_y[i] = bull_y[i] - 32
            screen.blit(img_weapon,[bull_x[i],bull_y[i]])
            if bull_y[i] < 0:
                bull_f[i] = False

def move_player(screen,key):
    global px,py,space
    if key[pygame.K_UP] == 1:
        py = py - 10
        if py < 20:
            py = 20
    if key[pygame.K_DOWN] == 1:
        py = py + 10
        if py > 460:
            py = 460
    if key[pygame.K_LEFT] == 1:
        px = px - 10
        if px < 20:
            px = 20
    if key[pygame.K_RIGHT] == 1:
        px = px + 10
        if px > 620:
            px = 620
    space = (space+1)*key[pygame.K_SPACE]
    if space%5 == 1: #5フレーム毎に弾を飛ばす
        set_bullet()

    screen.blit(img_player,[px-16,py-16])

def main():
    global bg_y
    pygame.init()
    pygame.display.set_caption("シューティングゲーム")
    screen = pygame.display.set_mode((640,480))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        bg_y = (bg_y+16)%480
        screen.blit(img_bg,[0,bg_y-480])
        screen.blit(img_bg,[0,bg_y])
        key = pygame.key.get_pressed()
        move_player(screen,key)
        move_bullet(screen)
        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()