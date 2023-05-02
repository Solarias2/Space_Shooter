import pygame
import sys
import variable
import functions
from player import Player
from enemy import Enemy1, Enemy2
from boss import Boss


################################## Functions ##################################
def reset_game():
    variable.player_bullets.empty()
    variable.enemies.empty()
    bosses.empty()
    variable.enemy_bullets.empty()
    variable.boss_bullets.empty()
    player.rect.centerx = variable.SCREEN_WIDTH / 2
    player.rect.bottom = variable.SCREEN_HEIGHT - 10


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

# Time setting of boss

game_state = variable.game_state
menu_index = variable.menu_index
DIFF = variable.EASY_DIFF
setting_index = variable.setting_index
retry_index = variable.retry_index
bg_y = variable.bg_y

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
                        Start_Score = 50
                        multiplier = 2
                        score = 0
                        waiting_time = 0
                        start_time = None
                        boss_delay = 3000
                        player.hp = 5
                        player.damage_flag = False
                        player.invincible = 50
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
                    setting_index = (setting_index - 1) % len(variable.setting_items)

                elif event.key == pygame.K_DOWN:
                    # Move the setting index down
                   setting_index = (setting_index + 1) % len(variable.setting_items)

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

                    elif retry_index == 1:
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

        # Collision judgement for Player
        for bullet in variable.player_bullets:
            bullet_hits = pygame.sprite.spritecollide(bullet, variable.enemies, False)
            for enemy in bullet_hits:
                bullet.kill()
                pygame.mixer.Sound.play(variable.Hit_sound)
                if isinstance(enemy, Enemy1):
                    if enemy.damage():
                        score += 10
                        new_enemy1 = Enemy1(DIFF)
                        variable.enemies.add(new_enemy1)

                elif isinstance(enemy, Enemy2):
                    if enemy.damage():
                        score += 50
                        new_enemy2 = Enemy2(DIFF)
                        variable.enemies.add(new_enemy2)

        # Draw background and scroll
        bg_y = (bg_y + 8) % 900
        variable.screen.blit(variable.bg_img, [0, bg_y])
        variable.screen.blit(variable.bg_img, [0, bg_y - 900])

        # Display Surface objects on screen
        variable.screen.blit(score_surface, (10, 10))

        # Draw the player, enemies, and bullet
        if not player.damage_flag:
            variable.screen.blit(player.image, player.rect)

        else:
            if player.invincible % 2 == 0:
                variable.screen.blit(player.image, player.rect)

            if player.invincible == 0:
                player.invincible = 50
                player.damage_flag = False
            
            player.invincible -= 1

        variable.enemies.draw(variable.screen)
        variable.player_bullets.draw(variable.screen)
        variable.enemy_bullets.draw(variable.screen)

        # Draw boss
        if score >= Start_Score:
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
                bullet_hits = pygame.sprite.spritecollide(bullet, bosses, False)
                for boss in bullet_hits:
                    bullet.kill()
                    pygame.mixer.Sound.play(variable.Hit_sound)
                    if boss.damage():
                        score += 1000
                        game_state = variable.STATE_CLEAR


            # For player and boss
            for boss in bosses:
                if player.rect.colliderect(boss.rect):
                    if boss.type in variable.death_conditions["Colliding with an enemy ship"]:
                        if not player.damage_flag:
                            pygame.mixer.Sound.play(variable.death_sound)
                            if player.damage():
                                game_state = variable.STATE_DEAD
                                functions.music_change('../Music/menu_music.wav')

            # For player and boss bullets
            for bullet in variable.boss_bullets:
                if player.rect.colliderect(bullet.rect):
                    if bullet.type in variable.death_conditions["Colliding with an enemy bullet"]:
                        if not player.damage_flag:
                            pygame.mixer.Sound.play(variable.death_sound)
                            if player.damage():
                                game_state = variable.STATE_DEAD
                                functions.music_change('../Music/menu_music.wav')

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
                            game_state = variable.STATE_DEAD
                            functions.music_change('../Music/menu_music.wav')

        # For player and enemies bullets
        for bullet in variable.enemy_bullets:
            if player.rect.colliderect(bullet.rect):
                if bullet.type in variable.death_conditions["Colliding with an enemy bullet"]:
                    if not player.damage_flag:
                        bullet.kill()
                        pygame.mixer.Sound.play(variable.death_sound)
                        if player.damage():
                            game_state = variable.STATE_DEAD
                            functions.music_change('../Music/menu_music.wav')

    # For Setting
    if game_state == variable.STATE_SETTING:
        # Draw setting screen
        functions.blit_text(variable.screen, variable.SETTING_MENU_TEXT, (variable.SCREEN_WIDTH / 3, variable.SCREEN_HEIGHT / 5), pygame.font.Font(None, 50))
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
        functions.blit_text(variable.screen, variable.HELP_MENU_TEXT, (variable.SCREEN_WIDTH / 3 - 200, variable.SCREEN_HEIGHT / 5), pygame.font.Font('../Fonts/ipam.ttf', 36))
        for index, item in enumerate(variable.help_items):
            variable.screen.blit(item[1], item[2])

    if game_state == variable.STATE_CLEAR:
        functions.blit_text(variable.screen, variable.GAME_CLEAR_TEXT, (variable.SCREEN_WIDTH / 3, variable.SCREEN_HEIGHT / 5), pygame.font.Font('../Fonts/ipam.ttf', 36))
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
        functions.blit_text(variable.screen, variable.GAME_OVER_TEXT, (variable.SCREEN_WIDTH / 3, variable.SCREEN_HEIGHT / 5), pygame.font.Font('../Fonts/ipam.ttf', 36))
        for index, item in enumerate(variable.retry_items):
            if index == retry_index:
                # Selected items are drawn in white
                variable.screen.blit(item[1], item[2])
            else:
                # Unselected items are drawn in gray
                variable.screen.blit(variable.menu_font.render(
                    item[0], True, (128, 128, 128)), item[2])

    # Update screen
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
