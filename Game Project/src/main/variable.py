import pygame
from pygame import mixer

# The width and height of Game
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

# Initialize Pygame and make window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pre_bg_img = pygame.image.load("../Assets/bgimg.jpeg")
bg_img = pygame.transform.scale(pre_bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
bg_y = 0

# Object image
player_frame = ['../Assets/player_Frame1.png', '../Assets/player_Frame2.png',
                '../Assets/player_Frame3.png', '../Assets/player_Frame4.png']
enemy1_frame = ['../Assets/enemy1_Frame1.png', '../Assets/enemy1_Frame2.png',
                '../Assets/enemy1_Frame3.png', '../Assets/enemy1_Frame4.png']
enemy2_frame = ['../Assets/enemy2_Frame1.png', '../Assets/enemy2_Frame2.png',
                '../Assets/enemy2_Frame3.png', '../Assets/enemy2_Frame4.png']
boss_frame = ['../Assets/Boss.png']

active_Frame = 0

# Create a font of menu option
pygame.init()
menu_font = pygame.font.Font(None, 36)

# Game States
STATE_MENU = 4
STATE_GAMEPLAY = 0
STATE_SETTING = 1
STATE_HELP = 2
STATE_QUIT = 3
STATE_CLEAR = 5
STATE_DEAD = 6

# Current state
game_state = STATE_MENU

# Define munu options
menu_options = [
    "Start Game",
    "Settings",
    "Help",
    "Quit"
]

# Loop through the menu options and create a menu item for each one
menu_items = []
for index, option in enumerate(menu_options):
    text = menu_font.render(option, True, (255, 255, 255))
    rect = text.get_rect()
    rect.centerx = screen.get_rect().centerx
    rect.centery = screen.get_rect().centery + index * 50
    menu_items.append((option, text, rect))

# Set the default menu option to the first one
menu_index = 0

# Difficulty
MED_DIFF = 0
EASY_DIFF = 1
HARD_DIFF = 2

# Create a font of score and game clear
score_font = pygame.font.Font(None, 36)
score = 0

clear_font = pygame.font.Font(None, 70)

# Boss time setting
BOSS_MOVE_INTERVAL = 1000
BOSS_SHOOT_INTERVAL = 1000

# ID for enemies and bullets. Meant to check death Conditions
ENEMY_1 = 1
ENEMY_2 = 2
BOSS = 3

ENEMY_BULLET = 1
BOSS_BULLET = 2

# Define the death conditions
death_conditions = {
    "Colliding with an enemy ship": (ENEMY_1, ENEMY_2, BOSS),
    "Colliding with an enemy bullet": (ENEMY_BULLET, BOSS_BULLET)
}

# Starts up menu music
mixer.music.load('../Music/menu_music.wav')
mixer.music.play(-1)
start_sound = pygame.mixer.Sound('../SFX/game_start.wav')
Hit_sound = pygame.mixer.Sound('../SFX/enemy_hit.wav')
death_sound = pygame.mixer.Sound('../SFX/player_death.wav')
bullet_sound = pygame.mixer.Sound('../SFX/bullet_fire.wav')
Boss_Incoming = pygame.mixer.Sound('../SFX/Boss_incoming.wav')


# Player_bullet group
player_bullets = pygame.sprite.Group()

# Enemy group
enemies = pygame.sprite.Group()

# Enemy1_bullet group
enemy_bullets = pygame.sprite.Group()

# Hit_ememies group
hit_enemies = []

# Boss_bullets
boss_bullets = pygame.sprite.Group()

#Text being used in the Game
HELP_MENU_TEXT = '遊び方\n1. 矢印キーでプレイヤーを移動，スペースキーで弾を発射\n2. スコアが50を超えたら，ボスが出現\n3. 5回攻撃を受けると，ゲームオーバー\n4. 難易度は，イージー，ミディアム，ハードの3つ\n\nエネミーは3種類\nエネミー1を倒すと10点，エネミー2を倒すと50点'
GAME_OVER_TEXT = 'ゲームオーバー!!\nもう一度遊びますか？'
GAME_CLEAR_TEXT = 'クリアおめでとう!!!!!'