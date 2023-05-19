import pygame
import random
import sys
import variable
import functions
from player import Player
from enemy import Enemy1, Enemy2
from boss import Boss
from item import Item1, Item2, Item3, Item4, Heart
from explosion import Explosion


################################## Functions ##################################
def reset_game():
    variable.player_bullets.empty()
    variable.enemies.empty()
    bosses.empty()
    variable.enemy_bullets.empty()
    variable.boss_bullets.empty()
    player.rect.centerx = variable.SCREEN_WIDTH / 2
    player.rect.bottom = variable.SCREEN_HEIGHT - 60


def Enemy_Drop(Difficulty_flag):
    items.draw(variable.screen)

    if Difficulty_flag == 2:
        check_prob = random.randint(0, 5000)
    else:
        check_prob = random.randint(0, 7000)

    # Multi Drop
    if check_prob <= 200:
        item1 = Item1()
        items.add(item1)

    # Wide Drop
    if check_prob > 200 and check_prob <= 400:
        item2 = Item2()
        items.add(item2)

    # Fast Drop
    if check_prob > 400 and check_prob <= 600:
        item3 = Item3()
        items.add(item3)

    # Berserk Drop
    if check_prob > 600 and check_prob <= 650:
        item4 = Item4()
        items.add(item4)

    # Heart Drop
    if check_prob > 650 and check_prob <= 750:
        heart = Heart()
        items.add(heart)


################################## Basic parts of the game ##################################

# Initialize Pygame and make window
pygame.init()

# Set the background color of the game screen
background_color = (0, 0, 0)
variable.screen.fill(background_color)

# Player
player = Player()

# Boss
bosses = pygame.sprite.Group()

# Items
items = pygame.sprite.Group()

# Powerup time limit
item1_timelimit = 7 * 1000
item2_timelimit = 7 * 1000
item3_timelimit = 7 * 1000
item4_timelimit = 4 * 1000

# Explosion
explosion = pygame.sprite.Group()
Explode_time = 1500

# Variable
game_state = variable.game_state
menu_index = variable.menu_index
DIFF = variable.EASY_DIFF
GAME_MODE = variable.STANDARD_MODE
setting_index = variable.setting_index
retry_index = variable.retry_index
bg_y = variable.bg_y
border_score = [3000, 1000, 5000]
clear_flag = False
clear_count = 100
game_over_flag = False
game_over_count = 100

# Set the max FPS
clock = pygame.time.Clock()
FPS = 40

# Game_loop
running = True
while running:
    # Process the events
    variable.screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            # For Game menu
            if game_state == variable.STATE_MENU:
                if event.key == pygame.K_UP:
                    # Move the menu index up
                    menu_index = (menu_index - 1) % len(variable.menu_items)

                elif event.key == pygame.K_DOWN:
                    # Move the menu index down
                    menu_index = (menu_index + 1) % len(variable.menu_items)

                elif event.key == pygame.K_RETURN:
                    # Check which menu option was selected
                    if menu_index == 0:
                        game_state = variable.STATE_GAMEPLAY
                        reset_game()
                        Start_Score = border_score[DIFF]
                        multiplier = 2
                        score = 0
                        waiting_time = 0
                        start_time = None
                        boss_delay = 3000
                        player.hp = 5
                        player.damage_flag = False
                        player.invincible = 50
                        clear_flag = game_over_flag = False
                        clear_count = game_over_count = 100
                        items.empty()
                        for i in range(6):
                            enemy1 = Enemy1(DIFF)
                            variable.enemies.add(enemy1)

                        for i in range(3):
                            enemy2 = Enemy2(DIFF)
                            variable.enemies.add(enemy2)

                        boss = Boss(DIFF)
                        bosses.add(boss)

                        pygame.mixer.Sound.play(variable.start_sound)
                        functions.music_change('../Music/stage_music.wav')

                    elif menu_index == 1:
                        game_state = variable.STATE_SETTING
                        pygame.mixer.Sound.play(variable.Menu_Select)

                    elif menu_index == 2:
                        game_state = variable.STATE_HELP
                        pygame.mixer.Sound.play(variable.Menu_Select)

                    elif menu_index == 3:
                        pygame.mixer.Sound.play(variable.Menu_Select)
                        pygame.quit()
                        sys.exit()

            # For Setting
            elif game_state == variable.STATE_SETTING:
                if event.key == pygame.K_UP:
                    # Move the setting index up
                    setting_index = (
                        setting_index - 1) % len(variable.setting_items)

                elif event.key == pygame.K_DOWN:
                    # Move the setting index down
                    setting_index = (
                        setting_index + 1) % len(variable.setting_items)

                elif event.key == pygame.K_RETURN:
                    # Check which menu option was selected
                    if setting_index == 0:
                        DIFF = variable.EASY_DIFF
                        pygame.mixer.Sound.play(variable.Menu_Select)

                    elif setting_index == 1:
                        DIFF = variable.MED_DIFF
                        pygame.mixer.Sound.play(variable.Menu_Select)

                    elif setting_index == 2:
                        DIFF = variable.HARD_DIFF
                        pygame.mixer.Sound.play(variable.Menu_Select)

                    elif setting_index == 3:
                        GAME_MODE = variable.STANDARD_MODE
                        pygame.mixer.Sound.play(variable.Menu_Select)

                    elif setting_index == 4:
                        GAME_MODE = variable.FREEPLAY_MODE
                        pygame.mixer.Sound.play(variable.Menu_Select)

                    elif setting_index == 5:
                        game_state = variable.STATE_MENU
                        pygame.mixer.Sound.play(variable.Menu_Select)

            # For Help
            elif game_state == variable.STATE_HELP:
                if event.key == pygame.K_RETURN:
                    game_state = variable.STATE_MENU
                    pygame.mixer.Sound.play(variable.Menu_Select)

             # For Game Clear and Game Over
            elif game_state == variable.STATE_CLEAR or game_state == variable.STATE_DEAD:
                if event.key == pygame.K_UP:
                    # Move the setting index up
                    retry_index = (retry_index - 1) % len(variable.retry_items)

                elif event.key == pygame.K_DOWN:
                    # Move the setting index down
                    retry_index = (retry_index + 1) % len(variable.retry_items)

                elif event.key == pygame.K_RETURN:
                    # Check which menu option was selected
                    if retry_index == 0:
                        game_state = variable.STATE_MENU
                        pygame.mixer.Sound.play(variable.Menu_Select)
                        functions.music_change('../Music/menu_music.wav')

                    elif retry_index == 1:
                        game_state = variable.STATE_LEADERBOARD
                        pygame.mixer.Sound.play(variable.Menu_Select)

                    elif retry_index == 2:
                        pygame.mixer.Sound.play(variable.Menu_Select)
                        pygame.quit()
                        sys.exit()

            # For Player bullet
            elif game_state == variable.STATE_GAMEPLAY:
                # Shoot bullets
                if event.key == pygame.K_SPACE:
                    player.shoot_flag = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                player.shoot_flag = False

    # Process according to the game state
     # For Game menu
    if game_state == variable.STATE_MENU:
        # Draw menu screen
        for index, item in enumerate(variable.menu_items):
            if index == menu_index:
                # Selected items are drawn in white
                variable.screen.blit(item[1], item[2])
            else:
                # Unselected items are drawn in gray
                variable.screen.blit(variable.menu_font.render(
                    item[0], True, (128, 128, 128)), item[2])

    # For Game
    if game_state == variable.STATE_GAMEPLAY:
        # Draw score on surface object
        score_surface = variable.score_font.render(
            "Score: " + str(score), True, (255, 255, 255))

        # Updata player
        player.update()

        # Updata enemy1
        variable.enemies.update()

        # Updata bullets
        variable.player_bullets.update()
        variable.enemy_bullets.update()

        explosion.update()

        # Collision judgement for Player_bullet
        for bullet in variable.player_bullets:
            bullet_hits = pygame.sprite.spritecollide(
                bullet, variable.enemies, False)
            for enemy in bullet_hits:
                bullet.kill()
                pygame.mixer.Sound.play(variable.Hit_sound)
                if isinstance(enemy, Enemy1):
                    if enemy.damage():
                        # When the enemy is defeated, the explosion animation should activate upon each enemy defeat
                        explo = Explosion(enemy.rect.centerx,
                                          enemy.rect.centery)
                        explosion.add(explo)
                        enemy.kill()
                        Enemy_Drop(DIFF)
                        score += 10
                        new_enemy1 = Enemy1(DIFF)
                        variable.enemies.add(new_enemy1)

                elif isinstance(enemy, Enemy2):
                    if enemy.damage():
                        # When the enemy is defeated, the explosion animation should activate upon each enemy defeat
                        explo = Explosion(enemy.rect.centerx,
                                          enemy.rect.centery)
                        explosion.add(explo)
                        enemy.kill()
                        Enemy_Drop(DIFF)
                        score += 50
                        new_enemy2 = Enemy2(DIFF)
                        variable.enemies.add(new_enemy2)

        # if explo.explosion_flag:
        #     explosion.update()

        items.update()

        # Draw background and scroll
        bg_y = (bg_y + 8) % 900
        variable.screen.blit(variable.bg_img, [0, bg_y])
        variable.screen.blit(variable.bg_img, [0, bg_y - 900])

        # Display Surface objects on screen
        variable.screen.blit(score_surface, (10, 10))

        # Draw the player, enemies, and bullet
        if not player.damage_flag:
            if player.hp != 0:
                variable.screen.blit(player.image, player.rect)

        else:
            if player.hp != 0:
                if player.invincible % 2 == 0:
                    variable.screen.blit(player.image, player.rect)

                if player.invincible == 0:
                    player.invincible = 50
                    player.damage_flag = False

                player.invincible -= 1

        variable.enemies.draw(variable.screen)
        variable.player_bullets.draw(variable.screen)
        variable.enemy_bullets.draw(variable.screen)

        items.draw(variable.screen)
        explosion.draw(variable.screen)

        # Display player hp
        for i in range(player.hp):
            variable.screen.blit(variable.player_hp,
                                 (10 + i * 50, variable.SCREEN_HEIGHT - 50))

        # Draw boss
        if score >= Start_Score and GAME_MODE == variable.STANDARD_MODE:
            boss_music = pygame.mixer.Sound(variable.Boss_Incoming)
            boss_music.play()
            if start_time == None:
                variable.enemies.empty()
                start_time = pygame.time.get_ticks()

            waiting_time = pygame.time.get_ticks() - start_time

            if waiting_time > boss_delay:
                boss_music.stop()
                bosses.draw(variable.screen)
                variable.boss_bullets.draw(variable.screen)

                bosses.update()
                variable.boss_bullets.update()

            # Collision judgement for Boss
             # For player bullets and boss
            for bullet in variable.player_bullets:
                bullet_hits = pygame.sprite.spritecollide(
                    bullet, bosses, False)
                for boss in bullet_hits:
                    bullet.kill()
                    pygame.mixer.Sound.play(variable.Hit_sound)
                    if boss.damage():
                        score += 1000
                        explo = Explosion(boss.rect.centerx, boss.rect.centery)
                        explosion.add(explo)
                        bosses.empty()
                        clear_flag = True

             # For player and boss
            for boss in bosses:
                if player.rect.colliderect(boss.rect):
                    if boss.type in variable.death_conditions["Colliding with an enemy ship"]:
                        if not player.damage_flag:
                            pygame.mixer.Sound.play(variable.death_sound)
                            if player.damage():
                                explo = Explosion(
                                    player.rect.centerx - 11, player.rect.centery)
                                explosion.add(explo)
                                game_over_flag = True

             # For player and boss bullets
            for bullet in variable.boss_bullets:
                if player.rect.colliderect(bullet.rect):
                    if bullet.type in variable.death_conditions["Colliding with an enemy bullet"]:
                        if not player.damage_flag:
                            pygame.mixer.Sound.play(variable.death_sound)
                            if player.damage():
                                explo = Explosion(
                                    player.rect.centerx - 11, player.rect.centery)
                                explosion.add(explo)
                                game_over_flag = True

        # Make delay until the game is finished
        if clear_flag:
            clear_count -= 1
            if clear_count == 0:
                game_state = variable.STATE_CLEAR
                functions.music_change('../Music/clear.ogg')

        # Gameover
         # For player and enemies
        for enemy in variable.enemies:
            if player.rect.colliderect(enemy.rect):
                if enemy.type in variable.death_conditions["Colliding with an enemy ship"]:
                    if not player.damage_flag:
                        pygame.mixer.Sound.play(variable.death_sound)
                        if isinstance(enemy, Enemy1):
                            enemy.kill()
                            new_enemy1 = Enemy1(DIFF)
                            variable.enemies.add(new_enemy1)

                        elif isinstance(enemy, Enemy2):
                            enemy.kill()
                            new_enemy2 = Enemy2(DIFF)
                            variable.enemies.add(new_enemy2)

                        if player.damage():
                            # Explosion of player
                            explo = Explosion(
                                player.rect.centerx - 11, player.rect.centery)
                            explosion.add(explo)
                            game_over_flag = True

         # For player and enemies bullets
        for bullet in variable.enemy_bullets:
            if player.rect.colliderect(bullet.rect):
                # current_hit_time = pygame.time.get_ticks()
                if bullet.type in variable.death_conditions["Colliding with an enemy bullet"]:
                    if not player.damage_flag:
                        bullet.kill()
                        pygame.mixer.Sound.play(variable.death_sound)
                        if player.damage():
                            explo = Explosion(
                                player.rect.centerx - 11, player.rect.centery)
                            explosion.add(explo)
                            game_over_flag = True

        # Make delay until the game is finished
        if game_over_flag:
            game_over_count -= 1
            if game_over_count == 0:
                game_state = variable.STATE_DEAD
                functions.music_change('../Music/menu_music.wav')

        # Collision judgement for Item
         # For player and items
        for item in items:
            if player.rect.colliderect(item.rect):
                if item.type in variable.item_types["get an item type"]:
                    item_get_time = pygame.time.get_ticks()
                    # Item1
                    if item.type == variable.multi:
                        if not player.multi:
                            player.multi = True
                        # When player get item1 while being powered up, add addtional power up time.
                        elif player.multi:
                            item1_timelimit = 7 * 1000

                    # Item2
                    if item.type == variable.wide:
                        if not player.wide:
                            player.wide = True
                        # When player get item2 while being powered up, add addtional power up time.
                        elif player.wide:
                            item2_timelimit = 7 * 1000

                    # Item3
                    if item.type == variable.fast:
                        if not player.fast:
                            player.fast = True
                        # When player get item3 while being powered up, add addtional power up time.
                        elif player.fast:
                            item3_timelimit = 7 * 1000

                    # Item4
                    if item.type == variable.berserk:
                        if not player.berserk:
                            player.berserk = True
                        # When player get item4 while being powered up, add addtional power up time.
                        elif player.berserk:
                            item4_timelimit = 4 * 1000

                    # Heart
                    if item.type == variable.heart:
                        player.hp += 1

                    item.kill()

        # Item1's time limit
        if player.multi:
            powerup1_now = pygame.time.get_ticks()
            if powerup1_now - item_get_time >= item1_timelimit:
                player.multi = False
                item_get_time = powerup1_now

        # Item2's time limit
        if player.wide:
            powerup2_now = pygame.time.get_ticks()
            if powerup2_now - item_get_time >= item2_timelimit:
                player.wide = False
                item_get_time = powerup2_now

        # Item3's time limit
        if player.fast:
            powerup3_now = pygame.time.get_ticks()
            if powerup3_now - item_get_time >= item3_timelimit:
                player.fast = False
                item_get_time = powerup3_now

        # Item4's time limit
        if player.berserk:
            powerup4_now = pygame.time.get_ticks()
            if powerup4_now - item_get_time >= item4_timelimit:
                player.berserk = False
                item_get_time = powerup4_now

    # For Setting
    if game_state == variable.STATE_SETTING:
        # Draw setting screen
        functions.blit_text(variable.screen, variable.SETTING_MENU_TEXT1, (variable.SCREEN_WIDTH /
                            3, variable.SCREEN_HEIGHT / 12), pygame.font.Font('../Fonts/ipam.ttf', 50))
        functions.blit_text(variable.screen, variable.SETTING_MENU_TEXT2, (variable.SCREEN_WIDTH /
                            3, variable.SCREEN_HEIGHT / 2), pygame.font.Font('../Fonts/ipam.ttf', 50))
        for index, item in enumerate(variable.setting_items):
            if index == setting_index:
                # Selected items are drawn in white
                variable.screen.blit(item[1], item[2])
            else:
                # Unselected items are drawn in gray
                variable.screen.blit(variable.menu_font.render(
                    item[0], True, (128, 128, 128)), item[2])

    # For Help
    if game_state == variable.STATE_HELP:
        # Draw help screen
        functions.blit_text(variable.screen, variable.HELP_MENU_TEXT, (variable.SCREEN_WIDTH /
                            3 - 200, variable.SCREEN_HEIGHT / 10), pygame.font.Font('../Fonts/ipam.ttf', 36))
        for index, item in enumerate(variable.help_items):
            variable.screen.blit(item[1], item[2])

    if game_state == variable.STATE_CLEAR:
        functions.blit_text(variable.screen, variable.GAME_CLEAR_TEXT, (variable.SCREEN_WIDTH / 3,
                            variable.SCREEN_HEIGHT / 5), pygame.font.Font('../Fonts/ipam.ttf', 36))
        for index, item in enumerate(variable.retry_items):
            if index == retry_index:
                # Selected items are drawn in white
                variable.screen.blit(item[1], item[2])
            else:
                # Unselected items are drawn in gray
                variable.screen.blit(variable.menu_font.render(
                    item[0], True, (128, 128, 128)), item[2])

    # For Game Over
    if game_state == variable.STATE_DEAD:
        functions.blit_text(variable.screen, variable.GAME_OVER_TEXT, (variable.SCREEN_WIDTH / 3,
                            variable.SCREEN_HEIGHT / 5), pygame.font.Font('../Fonts/ipam.ttf', 36))
        for index, item in enumerate(variable.retry_items):
            if index == retry_index:
                # Selected items are drawn in white
                variable.screen.blit(item[1], item[2])
            else:
                # Unselected items are drawn in gray
                variable.screen.blit(variable.menu_font.render(
                    item[0], True, (128, 128, 128)), item[2])
                
    if game_state == variable.STATE_LEADERBOARD:
        pass

    # Update screen
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
