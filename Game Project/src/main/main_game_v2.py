import pygame
import random
import sys
from pygame import mixer
from variable import SCREEN_WIDTH, SCREEN_HEIGHT, screen, bg_img, bg_y, STATE_MENU, STATE_GAMEPLAY, STATE_SETTING, STATE_HELP, STATE_QUIT, menu_font, game_state, menu_items, menu_index, score_font, start_sound, Hit_sound, death_sound, bullet_sound, Boss_Incoming, death_conditions, player_bullets, enemies, enemy1_bullets, enemy2_bullets, hit_enemies, boss_bullets
from functions import music_change
from player import Player
from enemy import Enemy1, Enemy2
from boss import Boss


################################## Functions ##################################
def reset_game():
    player_bullets.empty()
    enemies.empty()
    bosses.empty()
    enemy1_bullets.empty()
    enemy2_bullets.empty()
    boss_bullets.empty()
    player.rect.centerx = SCREEN_WIDTH / 2
    player.rect.bottom = SCREEN_HEIGHT - 10


################################## Basic parts of the game ##################################

# Initialize Pygame and make window
pygame.init()

# Set the background color of the game screen
background_color = (0, 0, 0)
screen.fill(background_color)

# Player
player = Player()

# Boss
bosses = pygame.sprite.Group()
boss = Boss()

# Time setting of boss

# Set the max FPS
clock = pygame.time.Clock()
FPS = 40

# Key
# key = pygame.key.get_pressed()

# Game_loop
running = True
while running:
    # Process the events
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if game_state == STATE_MENU:

                if event.key == pygame.K_UP:
                    # Move the menu index up
                    menu_index = (menu_index - 1) % len(menu_items)

                elif event.key == pygame.K_DOWN:
                    # Move the menu index down
                    menu_index = (menu_index + 1) % len(menu_items)

                elif event.key == pygame.K_RETURN:
                    # Check which menu option was selected
                    if menu_index == 0:
                        game_state = STATE_GAMEPLAY
                        reset_game()
                        Start_Score = 50
                        multiplier = 2
                        score = 0
                        waiting_time = 0
                        start_time = None
                        boss_delay = 3000
                        player.hp = 20
                        boss.hp = 50
                        for i in range(6):
                            enemy1 = Enemy1()
                            enemies.add(enemy1)

                        for i in range(3):
                            enemy2 = Enemy2()
                            enemies.add(enemy2)

                        bosses.add(boss)

                        pygame.mixer.Sound.play(start_sound)
                        music_change('../Music/stage_music.wav')

                    elif menu_index == 1:
                        pass

                    elif menu_index == 2:
                        pass

                    elif menu_index == 3:
                        pygame.quit()
                        sys.exit()

            if game_state == STATE_GAMEPLAY:
                # Shoot bullets
                if event.key == pygame.K_SPACE:
                    player.shoot_flag = True
                    
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                player.shoot_flag = False

    # Process according to the game state
    if game_state == STATE_MENU:
        # Draw menu screen
        for index, item in enumerate(menu_items):
            if index == menu_index:
                # Selected items are drawn in white
                screen.blit(item[1], item[2])
            else:
                # Unselected items are drawn in gray
                screen.blit(menu_font.render(
                    item[0], True, (128, 128, 128)), item[2])

    elif game_state == STATE_GAMEPLAY:
        # Draw score on surface object
        score_surface = score_font.render(
            "Score: " + str(score), True, (255, 255, 255))

        # Updata player
        player.update()

        # Updata enemy1
        enemies.update()

        # Updata bullets
        player_bullets.update()
        enemy1_bullets.update()
        enemy2_bullets.update()

        # Collision judgement for Player
        for bullet in player_bullets:
            bullet_hits = pygame.sprite.spritecollide(bullet, enemies, False)
            for enemy in bullet_hits:
                bullet.kill()
                pygame.mixer.Sound.play(Hit_sound)
                if isinstance(enemy, Enemy1):
                    if enemy.damage():
                        score += 10
                        new_enemy1 = Enemy1()
                        enemies.add(new_enemy1)

                elif isinstance(enemy, Enemy2):
                    if enemy.damage():
                        score += 50
                        new_enemy2 = Enemy2()
                        enemies.add(new_enemy2)

        # Draw background and scroll
        bg_y = (bg_y + 8) % 900
        screen.blit(bg_img, [0, bg_y])
        screen.blit(bg_img, [0, bg_y - 900])

        # Display Surface objects on screen
        screen.blit(score_surface, (10, 10))

        # Draw the player, enemies, and bullet
        screen.blit(player.image, player.rect)
        enemies.draw(screen)
        player_bullets.draw(screen)
        enemy1_bullets.draw(screen)
        enemy2_bullets.draw(screen)

        # Draw boss
        if score >= Start_Score:
            boss_music = pygame.mixer.Sound(Boss_Incoming)
            boss_music.play()
            if start_time == None:
                enemies.empty()
                start_time = pygame.time.get_ticks()

            waiting_time = pygame.time.get_ticks() - start_time

            if waiting_time > boss_delay:
                boss_music.stop()
                bosses.draw(screen)
                boss_bullets.draw(screen)

                bosses.update()
                boss_bullets.update()

            # Collision judgement for Boss
            # For player bullets and boss
            for bullet in player_bullets:
                bullet_hits = pygame.sprite.spritecollide(bullet, bosses, False)
                for boss in bullet_hits:
                    bullet.kill()
                    pygame.mixer.Sound.play(Hit_sound)
                    if boss.damage():
                        score += 1000

            # For player and boss
            for boss in bosses:
                if player.rect.colliderect(boss.rect):
                    if boss.type in death_conditions["Colliding with an enemy ship"]:
                        pygame.mixer.Sound.play(death_sound)
                        game_state = STATE_MENU
                        music_change('../Music/menu_music.wav')

            # For player and boss bullets
            for bullet in boss_bullets:
                if player.rect.colliderect(bullet.rect):
                    if bullet.type in death_conditions["Colliding with an enemy bullet"]:
                        pygame.mixer.Sound.play(death_sound)
                        game_state = STATE_MENU
                        music_change('../Music/menu_music.wav')


        # Gameover
        # For player and enemies
        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                if enemy.type in death_conditions["Colliding with an enemy ship"]:
                    pygame.mixer.Sound.play(death_sound)
                    if player.damage():
                        pygame.mixer.Sound.play(death_sound)
                        game_state = STATE_MENU
                        music_change('../Music/menu_music.wav')

        # For player and enemies1 bullets
        for bullet in enemy1_bullets:
            if player.rect.colliderect(bullet.rect):
                if bullet.type in death_conditions["Colliding with an enemy bullet"]:
                    pygame.mixer.Sound.play(death_sound)
                    if player.damage():
                        pygame.mixer.Sound.play(death_sound)
                        game_state = STATE_MENU
                        music_change('../Music/menu_music.wav')

        # For player and enemies1 bullets
        for bullet in enemy2_bullets:
            if player.rect.colliderect(bullet.rect):
                if bullet.type in death_conditions["Colliding with an enemy bullet"]:
                    pygame.mixer.Sound.play(death_sound)
                    if player.damage():
                        pygame.mixer.Sound.play(death_sound)
                        game_state = STATE_MENU
                        music_change('../Music/menu_music.wav')

    # Update screen
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
