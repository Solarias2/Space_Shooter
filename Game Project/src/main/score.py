import pygame

# Game menu screen settings
menu_bg = pygame.image.load("../Assets/bgimg.jpeg")
menu_font = pygame.font.Font("font.ttf", 32)
menu_title = menu_font.render("Space shooter", True, (255, 255, 255))
menu_options = [
    "Start Game",
    "Settings",
    "Help",
    "Quit"
]
menu_selected = 0

# Function to draw menu items
def draw_menu():
    screen.blit(menu_bg, (0, 0))
    screen.blit(menu_title, (SCREEN_WIDTH / 2 - menu_title.get_width() / 2, 100))
    for i in range(len(menu_options)):
        color = (255, 255, 255)
        if i == menu_selected:
            color = (255, 0, 0)
        menu_option = menu_font.render(menu_options[i], True, color)
        screen.blit(menu_option, (SCREEN_WIDTH / 2 - menu_option.get_width() / 2, 300 + i * 50))
    pygame.display.update()

# Functions that handle user input in menus
def handle_menu_input():
    global menu_selected
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

            elif event.key == pygame.K_UP:
                menu_selected = (menu_selected - 1) % len(menu_options)

            elif event.key == pygame.K_DOWN:
                menu_selected = (menu_selected + 1) % len(menu_options)

            elif event.key == pygame.K_SPACE:
                if menu_selected == 0:
                    start_game()
                
                elif menu_selected == 1:
                    options_menu()
                
                elif menu_selected == 2:
                    pygame.quit()
                    quit()

