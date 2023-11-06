# --------------------------------------------------------------------------------------------|
#                                                                                             |
# Thank you for your interest in my PacMan game! this was created in October 2023.            |
# My LinkedIn: https://www.linkedin.com/in/marcos-val%C3%A9rio-c-s-filho-688753113/           |
#                                                                                             |
# PacMan Marcos © 2023 by Marcos Valério Costa Silva Filho is licensed under CC BY-NC-SA 4.0  |
# Link for the license: https://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1     |
#                                                                                             |
# --------------------------------------------------------------------------------------------|



import pygame
import random
import webbrowser  # to be used on "about me" menu, to send user to my LinkedIn page

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CELL_SIZE = 40
SPEED = 1
WHITE = (255, 255, 255)
YELLOW = (255, 200, 10)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 140)
GREEN = (0, 220, 0)
PINK = (255, 0, 255)
TEAL = (0, 140, 255)
LIGHTBLUE = (30, 30, 255)

# Initialize game variables
player_pos = [360,480]
enemy_pos = [360,240]
enemy2_pos = [400, 240]
enemy3_pos = [440, 240]
enemy4_pos = [480, 240]
enemy_direction = 'UP'
enemy2_direction = 'RIGHT'
enemy3_direction = 'UP'
enemy4_direction = 'RIGHT'
score = 0
enemy_vulnerable_timer = 0

# Food positions (level 1), from bottom up, left to right. Total of 118 foods and 4 super-foods.
foods = [[40, 560], [80, 560], [120, 560], [160, 560], [200, 560], [240, 560], [280, 560], [320, 560], [360, 560], [400, 560], # bottom
         [440, 560], [480, 560], [520, 560], [560, 560], [600, 560], [640, 560], [680, 560], [720, 560], [0, 520],
         [280, 520], [480, 520], [760, 520], [0, 480], [40,480], [80,480], [120, 480], [200, 480], [240, 480], [280,480],
         [320, 480], [400, 480], [440, 480], [480, 480], [520, 480], [560, 480], [640, 480], [680, 480], [720, 480], [760, 480],
         [40, 440], [120, 440], [200, 440], [560, 440], [640, 440], [720, 440], [0, 400], [40, 400], [120, 400], [160, 400],
         [200, 400], [560, 400], [600, 400], [640, 400], [720, 400], [760, 400], [0, 360], [120, 360], [640, 360], [760, 360],
         [0, 320], [40, 320], [80, 320], [120, 320], [640, 320], [680, 320], [720, 320], [760, 320], [0, 240], [40, 240], [120,280], [640,280],
         [80, 240], [120, 240], [640, 240], [680, 240], [680, 240], [720, 240], [760, 240], [0, 200], [120, 200], [640, 200],
         [760, 200], [0, 160], [120, 160], [640, 160], [760, 160], [0, 120], [40, 120], [80, 120], [120, 120], [640, 120],
         [680, 120], [720, 120], [760, 120], [0, 80], [120, 80], [280, 80], [320, 80], [360, 80], [400, 80], [440, 80], [480, 80],
         [640, 80], [760, 80], [40, 40], [80, 40], [120, 40], [160, 40], [200, 40], [240, 40], [280, 40], [480, 40],
         [520, 40], [560, 40], [600, 40], [640, 40], [680, 40], [720, 40]]

# Super-food position
super_food_pos = [[0, 560], [760, 560], [0, 40], [760, 40]]

# Initial direction
player_direction = 'RIGHT'

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man Game (Marcos)")

# Set up the game clock
clock = pygame.time.Clock()
FPS = 60

# Rectangles
rectangles = [(520, 520, 240, 40), (320, 520, 160, 40), (40, 520, 240, 40),
                (600, 440, 40, 120), (160, 440, 40, 120), (760, 440, 40, 40),
                (0, 440, 40, 40), (680, 360, 40, 120), (720, 360, 40, 40),
                (80, 360, 40, 120), (40, 360, 40, 40), (480, 440, 80, 40),
                (360, 440, 80, 40), (240, 440, 80, 40), (520, 360, 120, 40),
                (320, 360, 160, 40), (160, 360, 120, 40), (600, 280, 40, 80),
                (160, 280, 40, 80), (680, 280, 120, 40), (0, 280, 120, 40),
                (240, 280, 320, 40), (320, 200, 40, 80), (400, 160, 40, 80), (480, 200, 40, 40),
                (40, 160, 80, 80), (160, 120, 40, 120), (240, 160, 40, 80),
                (320, 120, 160, 40), (520, 160, 40, 80), (600, 120, 40, 120),
                (680, 160, 80, 80), (0, 0, 800, 40), (40, 80, 80, 40), (160, 80, 120, 40),
                (320, 40, 160, 40), (520, 80, 120, 40), (680, 80, 80, 40)]

# Checking collisions with walls
def check_collision(player_pos, enemy_pos, rectangles):
    for rect in rectangles:
        if (player_pos[0] + CELL_SIZE > rect[0] and player_pos[0] < rect[0] + rect[2] and
            player_pos[1] + CELL_SIZE > rect[1] and player_pos[1] < rect[1] + rect[3]) or \
           (enemy_pos[0] + CELL_SIZE > rect[0] and enemy_pos[0] < rect[0] + rect[2] and
            enemy_pos[1] + CELL_SIZE > rect[1] and enemy_pos[1] < rect[1] + rect[3]):
            return True
    return False


# Defining middle area. To make enemy avoid turns here and start shaking because of random moves.
def is_in_middle_area(pos):
    return 200 < pos[1] < 240 and 320 < pos[0] < 440





# Function to display the main menu /////////////////////////
def main_menu():
    menu_running = True
    while menu_running:
        screen.fill(BLACK)
        font = pygame.font.Font(None, 36)
        title1 = pygame.font.Font(None, 50)
        title2 = pygame.font.Font(None, 20)
        title3 = pygame.font.Font(None, 15)
        
        title1_text = title1.render("PacMan", True, WHITE)
        title2_text = title2.render("Made in Python, by Marcos V C S Filho", True, WHITE)
        title3_text = title3.render("October 2023", True, WHITE)
        play_text = font.render("Play", True, WHITE)
        about_me_text = font.render("About Me", True, WHITE)
        quit_text = font.render("Quit", True, WHITE)

        title1_rect = title1_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200))
        title2_rect = title2_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 170))
        title3_rect = title3_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        play_rect = play_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        about_me_rect = about_me_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

        screen.blit(title1_text, title1_rect)
        screen.blit(title2_text, title2_rect)
        screen.blit(title3_text, title3_rect)
        screen.blit(play_text, play_rect)
        screen.blit(about_me_text, about_me_rect)
        screen.blit(quit_text, quit_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_rect.collidepoint(mouse_pos):
                    menu_running = False  # Start the game
                elif about_me_rect.collidepoint(mouse_pos):
                    about_me()
                elif quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    quit()




def display_text(screen, text, font, color, position):  # used on the text on "about me" page
    rendered_text = font.render(text, True, color)
    text_rect = rendered_text.get_rect(topleft=position)  # Use topleft instead of center
    screen.blit(rendered_text, text_rect)

def about_me():
    about_me_running = True
    title_font = pygame.font.Font(None, 36)
    content_font = pygame.font.Font(None, 21)
    back_font = pygame.font.Font(None, 26)

    while about_me_running:
        screen.fill(BLACK)

        # Use topleft alignment for content text
        # display_text(screen, "<-  Press ESC to go back", back_font, WHITE, (SCREEN_WIDTH // 2 - 380, SCREEN_HEIGHT // 2 - 285)) # go back
        display_text(screen, "Thanks for playing my game!", title_font, WHITE, (SCREEN_WIDTH // 2 - 170, SCREEN_HEIGHT // 2 - 210)) # Thanks text
        display_text(screen, "Who am I?", title_font, WHITE, (SCREEN_WIDTH // 2 - 270, SCREEN_HEIGHT // 2 - 130))
        display_text(screen, "Hello, nice to meet you! My name is Marcos.", content_font, WHITE, (50, SCREEN_HEIGHT // 2 - 80))
        display_text(screen, "When I'm not working, I like to spend time", content_font, WHITE, (50, SCREEN_HEIGHT // 2 - 60))
        display_text(screen, "with my family, and to create videogames. I", content_font, WHITE, (50, SCREEN_HEIGHT // 2 - 40))
        display_text(screen, "also like everything that has to do with", content_font, WHITE, (50, SCREEN_HEIGHT // 2 - 20))
        display_text(screen, "technology and innovation. That's why I", content_font, WHITE, (50, SCREEN_HEIGHT // 2))
        display_text(screen, "also have a diploma in electronics and", content_font, WHITE, (50, SCREEN_HEIGHT // 2 + 20))
        display_text(screen, "computer graphic's design.", content_font, WHITE, (50, SCREEN_HEIGHT // 2 + 40))

        display_text(screen, "If you'd like to know more about me, please", content_font, WHITE, (50, SCREEN_HEIGHT // 2 + 70))
        display_text(screen, "visit my LinkedIn page by clicking", content_font, WHITE, (50, SCREEN_HEIGHT // 2 + 90))
        display_text(screen, " here", content_font, GREEN, (290, SCREEN_HEIGHT // 2 + 90))

        # drawings
        # PACMAN drawing - Original positions
        player_center = (550, 280)
        x, y = (550, 280)

        # Increase size by 20 units
        size_increase = 20

        # Draw shapes with updated positions and sizes
        pygame.draw.circle(screen, YELLOW, player_center, 50 + size_increase)  # Increased circle radius and position
        pygame.draw.polygon(screen, BLACK, [(x, y),
                                            (x + 50 + size_increase, y + 50 + size_increase),
                                            (x + 50 + size_increase, y - 50 - size_increase)])  # Adjusted polygon points
        pygame.draw.circle(screen, WHITE, (x + 1 + size_increase, y - 13 - size_increase), 8)  # Adjusted circle position
        pygame.draw.circle(screen, BLACK, (x + 2 + size_increase, y - 13 - size_increase), 4)  # Adjusted circle position


        # ENEMY drawing
        # starting position
        a, b = (650, 260)

       
        pygame.draw.ellipse(screen, RED, (a, b, 40, 20))   #(a, b, 40, 20)
        pygame.draw.rect(screen, RED, (a, b + 9, 40, 20)) 
        pygame.draw.ellipse(screen, RED, (a, b + 20, 10, 20)) 
        pygame.draw.ellipse(screen, RED, (a + 10, b + 20, 10, 20)) 
        pygame.draw.ellipse(screen, RED, (a + 20, b + 20, 10, 20)) 
        pygame.draw.ellipse(screen, RED, (a + 30, b + 20, 10, 20)) 
        pygame.draw.ellipse(screen, WHITE, (a + 6, b + 5, 10, 12)) 
        pygame.draw.ellipse(screen, WHITE, (a + 24, b + 5, 10, 12))
        # Eyes looking right
        pygame.draw.ellipse(screen, BLACK, (a + 11, b + 9, 5, 5))
        pygame.draw.ellipse(screen, BLACK, (a + 29, b + 9, 5, 5))
        # Sweat drop
        pygame.draw.ellipse(screen, TEAL, (a, b, 5, 12))
        


        pygame.display.flip()



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    about_me_running = False  # exit the about me page.

            # Check for mouse button click events
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Get the mouse position
                mouse_pos = pygame.mouse.get_pos()
                # Define the bounds of the "here" text
                here_text_rect = pygame.Rect(272, SCREEN_HEIGHT // 2 + 60, 60, 50)  # Adjust text_width and text_height accordingly
                # Check if the mouse click is within the bounds of the "here" text
                if here_text_rect.collidepoint(mouse_pos):
                    # Open the web page when clicked
                    webbrowser.open("https://www.linkedin.com/in/marcos-val%C3%A9rio-c-s-filho-688753113/")


# Call the main menu function before the main game loop
main_menu()




# Main game loop /////////////////////////////////////////
running = True
while running:

    clock.tick(FPS)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                main_menu()  # Go back to the main menu


    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_direction != 'RIGHT':
        if not check_collision([player_pos[0] - SPEED, player_pos[1]], enemy_pos, rectangles):
            player_direction = 'LEFT'
    if keys[pygame.K_RIGHT] and player_direction != 'LEFT':
        if not check_collision([player_pos[0] + SPEED, player_pos[1]], enemy_pos, rectangles):
            player_direction = 'RIGHT'
    if keys[pygame.K_UP] and player_direction != 'DOWN':
        if not check_collision([player_pos[0], player_pos[1] - SPEED], enemy_pos, rectangles):
            player_direction = 'UP'
    if keys[pygame.K_DOWN] and player_direction != 'UP':
        if not check_collision([player_pos[0], player_pos[1] + SPEED], enemy_pos, rectangles):
            player_direction = 'DOWN'

    # Store the next position based on the current direction
    next_pos = player_pos.copy()

    # Move the player
    if player_direction == 'LEFT' and player_pos[0] > 0:
        next_pos[0] -= SPEED
    elif player_direction == 'RIGHT' and player_pos[0] < SCREEN_WIDTH - CELL_SIZE:
        next_pos[0] += SPEED
    elif player_direction == 'UP' and player_pos[1] > 0:
        next_pos[1] -= SPEED
    elif player_direction == 'DOWN' and player_pos[1] < SCREEN_HEIGHT - CELL_SIZE:
        next_pos[1] += SPEED

    # Check if the next position collides with any wall
    collides_with_wall = check_collision(next_pos, enemy_pos, rectangles)

    # Only update player position if the next position does not collide with a wall
    if not collides_with_wall:
        player_pos = next_pos






    # Enemy 1 -------------------------------------------------------------
    # Move enemy 1 in a deterministic way
    next_enemy_pos = enemy_pos.copy()
    valid_directions = []

    # Check valid directions (not opposite to the current direction, and no wall collision, and not in the middle)
    if (enemy_direction != 'RIGHT' and enemy_pos[0] > 0 and not check_collision(player_pos, [enemy_pos[0] - SPEED, enemy_pos[1]], rectangles) and not is_in_middle_area(next_enemy_pos)):
        valid_directions.append('LEFT')
    if (enemy_direction != 'LEFT' and enemy_pos[0] < SCREEN_WIDTH - CELL_SIZE and not check_collision(player_pos, [enemy_pos[0] + SPEED, enemy_pos[1]], rectangles) and not is_in_middle_area(next_enemy_pos)):
        valid_directions.append('RIGHT')
    if (enemy_direction != 'DOWN' and enemy_pos[1] > 0 and not check_collision(player_pos, [enemy_pos[0], enemy_pos[1] - SPEED], rectangles) and not is_in_middle_area(next_enemy_pos)):
        valid_directions.append('UP')
    if (enemy_direction != 'UP' and enemy_pos[1] < SCREEN_HEIGHT - CELL_SIZE and not check_collision(player_pos, [enemy_pos[0], enemy_pos[1] + SPEED], rectangles) and not is_in_middle_area(next_enemy_pos)):
        valid_directions.append('DOWN')

    # Change direction if a valid turn is available
    if valid_directions:
        enemy_direction = random.choice(valid_directions)

    # Move the enemy based on the selected direction
    if enemy_direction == 'LEFT':
        next_enemy_pos[0] -= SPEED
    elif enemy_direction == 'RIGHT':
        next_enemy_pos[0] += SPEED
    elif enemy_direction == 'UP':
        next_enemy_pos[1] -= SPEED
    elif enemy_direction == 'DOWN':
        next_enemy_pos[1] += SPEED

    # Update enemy 1 position
    enemy_pos = next_enemy_pos


    # Enemy 2 --------------------------------------------------------------
    # Move enemy 2 in a deterministic way
    next_enemy2_pos = enemy2_pos.copy()
    valid_directions2 = []
    if (enemy2_direction != 'RIGHT' and enemy2_pos[0] > 0 and not check_collision(player_pos, [enemy2_pos[0] - SPEED, enemy2_pos[1]], rectangles) and not is_in_middle_area(next_enemy2_pos)):
        valid_directions2.append('LEFT')
    if (enemy2_direction != 'LEFT' and enemy2_pos[0] < SCREEN_WIDTH - CELL_SIZE and not check_collision(player_pos, [enemy2_pos[0] + SPEED, enemy2_pos[1]], rectangles) and not is_in_middle_area(next_enemy2_pos)):
        valid_directions2.append('RIGHT')
    if (enemy2_direction != 'DOWN' and enemy2_pos[1] > 0 and not check_collision(player_pos, [enemy2_pos[0], enemy2_pos[1] - SPEED], rectangles) and not is_in_middle_area(next_enemy2_pos)):
        valid_directions2.append('UP')
    if (enemy2_direction != 'UP' and enemy2_pos[1] < SCREEN_HEIGHT - CELL_SIZE and not check_collision(player_pos, [enemy2_pos[0], enemy2_pos[1] + SPEED], rectangles) and not is_in_middle_area(next_enemy2_pos)):
        valid_directions2.append('DOWN')

    # Change direction if a valid turn is available
    if valid_directions2:
        enemy2_direction = random.choice(valid_directions2)

    # Move enemy 2 based on the selected direction
    if enemy2_direction == 'LEFT':
        next_enemy2_pos[0] -= SPEED
    elif enemy2_direction == 'RIGHT':
        next_enemy2_pos[0] += SPEED
    elif enemy2_direction == 'UP':
        next_enemy2_pos[1] -= SPEED
    elif enemy2_direction == 'DOWN':
        next_enemy2_pos[1] += SPEED

    # Update enemy2 position
    enemy2_pos = next_enemy2_pos


    # Enemy 3 ----------------------------------------------------------------
    # Move enemy 3 in a deterministic way
    next_enemy3_pos = enemy3_pos.copy()
    valid_directions3 = []
    if (enemy3_direction != 'RIGHT' and enemy3_pos[0] > 0 and not check_collision(player_pos, [enemy3_pos[0] - SPEED, enemy3_pos[1]], rectangles) and not is_in_middle_area(next_enemy3_pos)):
        valid_directions3.append('LEFT')
    if (enemy3_direction != 'LEFT' and enemy3_pos[0] < SCREEN_WIDTH - CELL_SIZE and not check_collision(player_pos, [enemy3_pos[0] + SPEED, enemy3_pos[1]], rectangles) and not is_in_middle_area(next_enemy3_pos)):
        valid_directions3.append('RIGHT')
    if (enemy3_direction != 'DOWN' and enemy3_pos[1] > 0 and not check_collision(player_pos, [enemy3_pos[0], enemy3_pos[1] - SPEED], rectangles) and not is_in_middle_area(next_enemy3_pos)):
        valid_directions3.append('UP')
    if (enemy3_direction != 'UP' and enemy3_pos[1] < SCREEN_HEIGHT - CELL_SIZE and not check_collision(player_pos, [enemy3_pos[0], enemy3_pos[1] + SPEED], rectangles) and not is_in_middle_area(next_enemy3_pos)):
        valid_directions3.append('DOWN')

    # Change direction if a valid turn is available
    if valid_directions3:
        enemy3_direction = random.choice(valid_directions3)

    # Move enemy 3 based on the selected direction
    if enemy3_direction == 'LEFT':
        next_enemy3_pos[0] -= SPEED
    elif enemy3_direction == 'RIGHT':
        next_enemy3_pos[0] += SPEED
    elif enemy3_direction == 'UP':
        next_enemy3_pos[1] -= SPEED
    elif enemy3_direction == 'DOWN':
        next_enemy3_pos[1] += SPEED

    # Update enemy3 position
    enemy3_pos = next_enemy3_pos

    # Enemy 4 --------------------------------------------------------------
    # Move enemy 4 in a deterministic way
    next_enemy4_pos = enemy4_pos.copy()
    valid_directions4 = []
    if (enemy4_direction != 'RIGHT' and enemy4_pos[0] > 0 and not check_collision(player_pos, [enemy4_pos[0] - SPEED, enemy4_pos[1]], rectangles) and not is_in_middle_area(next_enemy4_pos)):
        valid_directions4.append('LEFT')
    if (enemy4_direction != 'LEFT' and enemy4_pos[0] < SCREEN_WIDTH - CELL_SIZE and not check_collision(player_pos, [enemy4_pos[0] + SPEED, enemy4_pos[1]], rectangles) and not is_in_middle_area(next_enemy4_pos)):
        valid_directions4.append('RIGHT')
    if (enemy4_direction != 'DOWN' and enemy4_pos[1] > 0 and not check_collision(player_pos, [enemy4_pos[0], enemy4_pos[1] - SPEED], rectangles) and not is_in_middle_area(next_enemy4_pos)):
        valid_directions4.append('UP')
    if (enemy4_direction != 'UP' and enemy4_pos[1] < SCREEN_HEIGHT - CELL_SIZE and not check_collision(player_pos, [enemy4_pos[0], enemy4_pos[1] + SPEED], rectangles) and not is_in_middle_area(next_enemy4_pos)):
        valid_directions4.append('DOWN')

    # Change direction if a valid turn is available
    if valid_directions4:
        enemy4_direction = random.choice(valid_directions4)

    # Move enemy 4 based on the selected direction
    if enemy4_direction == 'LEFT':
        next_enemy4_pos[0] -= SPEED
    elif enemy4_direction == 'RIGHT':
        next_enemy4_pos[0] += SPEED
    elif enemy4_direction == 'UP':
        next_enemy4_pos[1] -= SPEED
    elif enemy4_direction == 'DOWN':
        next_enemy4_pos[1] += SPEED

    # Update enemy4 position
    enemy4_pos = next_enemy4_pos




    # Check if the next position collides with any wall or the player
    collides_with_wall_or_player = check_collision(player_pos, next_enemy_pos, rectangles)

    # Only update enemy position if the next position does not collide with a wall or the player
    if not collides_with_wall_or_player:
        enemy_pos = next_enemy_pos

    # Check for collisions with food
    for food in foods:
        if (player_pos[0] + 20) // CELL_SIZE == food[0] // CELL_SIZE and (player_pos[1] + 20) // CELL_SIZE == food[1] // CELL_SIZE:
            score += 1
            foods.remove(food)
            break


    # Check for collisions between player and Enemy 1 (dies while not vulnerable, and kills when they are vulnerable)
    if (player_pos[0] == enemy_pos[0]) and (player_pos[1] == enemy_pos[1]):
        player_enemy_colliding = True
        if not pygame.time.get_ticks() < enemy_vulnerable_timer:
            about_me()
        if pygame.time.get_ticks() < enemy_vulnerable_timer:
            enemy_pos = [360,240]
    if (player_pos[1] >= enemy_pos[1] and player_pos[1] <= enemy_pos[1] + 20):
        if (player_pos[0] + 20 >= enemy_pos[0] and player_pos[0] + 20 <= enemy_pos[0] + 20):  # collision from left to right
            if not pygame.time.get_ticks() < enemy_vulnerable_timer:
                about_me()
            if pygame.time.get_ticks() < enemy_vulnerable_timer:
                enemy_pos = [360,240]
        if (player_pos[0] <= enemy_pos[0] + 20 and player_pos[0] >= enemy_pos[0]):  # collision from right to left
            if not pygame.time.get_ticks() < enemy_vulnerable_timer:
                about_me()
            if pygame.time.get_ticks() < enemy_vulnerable_timer:
                enemy_pos = [360,240]
    if (player_pos[0] >= enemy_pos[0] and player_pos[0] + 20 <= enemy_pos[0] + 20):
        if (player_pos[1] <= enemy_pos[1] + 20 and player_pos[1] >= enemy_pos[1]):  # collision from bellow the enemy
            if not pygame.time.get_ticks() < enemy_vulnerable_timer:
                about_me()
            if pygame.time.get_ticks() < enemy_vulnerable_timer:
                enemy_pos = [360,240]
        if (player_pos[1] + 20 >= enemy_pos[1] and player_pos[1] + 20 <= enemy_pos[1] + 20):
            if not pygame.time.get_ticks() < enemy_vulnerable_timer:
                about_me()
            if pygame.time.get_ticks() < enemy_vulnerable_timer:
                enemy_pos = [360,240]
    

    # Check for collisions between player and Enemy 2 (dies while not vulnerable, and kills when they are vulnerable)
    if (player_pos[0] == enemy2_pos[0]) and (player_pos[1] == enemy2_pos[1]):
        player_enemy_colliding = True
        if not pygame.time.get_ticks() < enemy_vulnerable_timer:
            about_me()
        if pygame.time.get_ticks() < enemy_vulnerable_timer:
            enemy2_pos = [360,240]
    if (player_pos[1] >= enemy2_pos[1] and player_pos[1] <= enemy2_pos[1] + 20):
        if (player_pos[0] + 20 >= enemy2_pos[0] and player_pos[0] + 20 <= enemy2_pos[0] + 20):  # collision from left to right
            if not pygame.time.get_ticks() < enemy_vulnerable_timer:
                about_me()
            if pygame.time.get_ticks() < enemy_vulnerable_timer:
                enemy2_pos = [360,240]
        if (player_pos[0] <= enemy2_pos[0] + 20 and player_pos[0] >= enemy2_pos[0]):  # collision from right to left
            if not pygame.time.get_ticks() < enemy_vulnerable_timer:
                about_me()
            if pygame.time.get_ticks() < enemy_vulnerable_timer:
                enemy2_pos = [360,240]
    if (player_pos[0] >= enemy2_pos[0] and player_pos[0] + 20 <= enemy2_pos[0] + 20):
        if (player_pos[1] <= enemy2_pos[1] + 20 and player_pos[1] >= enemy2_pos[1]):  # collision from bellow the enemy
            if not pygame.time.get_ticks() < enemy_vulnerable_timer:
                about_me()
            if pygame.time.get_ticks() < enemy_vulnerable_timer:
                enemy2_pos = [360,240]
        if (player_pos[1] + 20 >= enemy2_pos[1] and player_pos[1] + 20 <= enemy2_pos[1] + 20):
            if not pygame.time.get_ticks() < enemy_vulnerable_timer:
                about_me()
            if pygame.time.get_ticks() < enemy_vulnerable_timer:
                enemy2_pos = [360,240]


    # Check for collisions between player and Enemy 3 (dies while not vulnerable, and kills when they are vulnerable)
    if (player_pos[0] == enemy3_pos[0]) and (player_pos[1] == enemy3_pos[1]):
        player_enemy_colliding = True
        if not pygame.time.get_ticks() < enemy_vulnerable_timer:
            about_me()
        if pygame.time.get_ticks() < enemy_vulnerable_timer:
            enemy3_pos = [360,240]
    if (player_pos[1] >= enemy3_pos[1] and player_pos[1] <= enemy3_pos[1] + 20):
        if (player_pos[0] + 20 >= enemy3_pos[0] and player_pos[0] + 20 <= enemy3_pos[0] + 20):  # collision from left to right
            if not pygame.time.get_ticks() < enemy_vulnerable_timer:
                about_me()
            if pygame.time.get_ticks() < enemy_vulnerable_timer:
                enemy3_pos = [360,240]
        if (player_pos[0] <= enemy3_pos[0] + 20 and player_pos[0] >= enemy3_pos[0]):  # collision from right to left
            if not pygame.time.get_ticks() < enemy_vulnerable_timer:
                about_me()
            if pygame.time.get_ticks() < enemy_vulnerable_timer:
                enemy3_pos = [360,240]
    if (player_pos[0] >= enemy3_pos[0] and player_pos[0] + 20 <= enemy3_pos[0] + 20):
        if (player_pos[1] <= enemy3_pos[1] + 20 and player_pos[1] >= enemy3_pos[1]):  # collision from bellow the enemy
            if not pygame.time.get_ticks() < enemy_vulnerable_timer:
                about_me()
            if pygame.time.get_ticks() < enemy_vulnerable_timer:
                enemy3_pos = [360,240]
        if (player_pos[1] + 20 >= enemy3_pos[1] and player_pos[1] + 20 <= enemy3_pos[1] + 20):
            if not pygame.time.get_ticks() < enemy_vulnerable_timer:
                about_me()
            if pygame.time.get_ticks() < enemy_vulnerable_timer:
                enemy3_pos = [360,240]


    # Check for collisions between player and Enemy 4 (dies while not vulnerable, and kills when they are vulnerable)
    if (player_pos[0] == enemy4_pos[0]) and (player_pos[1] == enemy4_pos[1]):
        player_enemy_colliding = True
        if not pygame.time.get_ticks() < enemy_vulnerable_timer:
            about_me()
        if pygame.time.get_ticks() < enemy_vulnerable_timer:
            enemy4_pos = [360,240]
    if (player_pos[1] >= enemy4_pos[1] and player_pos[1] <= enemy4_pos[1] + 20):
        if (player_pos[0] + 20 >= enemy4_pos[0] and player_pos[0] + 20 <= enemy4_pos[0] + 20):  # collision from left to right
            if not pygame.time.get_ticks() < enemy_vulnerable_timer:
                about_me()
            if pygame.time.get_ticks() < enemy_vulnerable_timer:
                enemy4_pos = [360,240]
        if (player_pos[0] <= enemy4_pos[0] + 20 and player_pos[0] >= enemy4_pos[0]):  # collision from right to left
            if not pygame.time.get_ticks() < enemy_vulnerable_timer:
                about_me()
            if pygame.time.get_ticks() < enemy_vulnerable_timer:
                enemy4_pos = [360,240]
    if (player_pos[0] >= enemy4_pos[0] and player_pos[0] + 20 <= enemy4_pos[0] + 20):
        if (player_pos[1] <= enemy4_pos[1] + 20 and player_pos[1] >= enemy4_pos[1]):  # collision from bellow the enemy
            if not pygame.time.get_ticks() < enemy_vulnerable_timer:
                about_me()
            if pygame.time.get_ticks() < enemy_vulnerable_timer:
                enemy4_pos = [360,240]
        if (player_pos[1] + 20 >= enemy4_pos[1] and player_pos[1] + 20 <= enemy4_pos[1] + 20):
            if not pygame.time.get_ticks() < enemy_vulnerable_timer:
                about_me()
            if pygame.time.get_ticks() < enemy_vulnerable_timer:
                enemy4_pos = [360,240]



    # Check for collisions with super-food
    for food_pos in super_food_pos:
        if (player_pos[0] + 20) // CELL_SIZE == food_pos[0] // CELL_SIZE and (player_pos[1] + 20) // CELL_SIZE == food_pos[1] // CELL_SIZE:
            # Make enemies vulnerable for 10 seconds
            enemy_vulnerable_timer = pygame.time.get_ticks() + 10000
            super_food_pos.remove(food_pos)
            score = score + 1
            break

    # Draw everything
    screen.fill(BLACK)

    

    # Draw Pac-Man
    player_center = (player_pos[0] + CELL_SIZE // 2, player_pos[1] + CELL_SIZE // 2)
    pygame.draw.circle(screen, YELLOW, player_center, CELL_SIZE // 2)
    if player_direction == 'RIGHT':
        pygame.draw.polygon(screen, BLACK, [(player_center[0], player_center[1]),
                                            (player_center[0] + 20, player_center[1] + 20),
                                            (player_center[0] + 20, player_center[1] - 20)])
        pygame.draw.circle(screen, WHITE, (player_center[0] + 1, player_center[1] - CELL_SIZE // 3), 4)
        pygame.draw.circle(screen, BLACK, (player_center[0] + 2, player_center[1] - CELL_SIZE // 3), 2)
    elif player_direction == 'LEFT':
        pygame.draw.polygon(screen, BLACK, [(player_center[0], player_center[1]),
                                            (player_center[0] - CELL_SIZE // 2, player_center[1] + CELL_SIZE // 2),
                                            (player_center[0] - CELL_SIZE // 2, player_center[1] - CELL_SIZE // 2)])
        pygame.draw.circle(screen, WHITE, (player_center[0] - 1, player_center[1] - CELL_SIZE // 3), 4)
        pygame.draw.circle(screen, BLACK, (player_center[0] - 2, player_center[1] - CELL_SIZE // 3), 2)
    elif player_direction == 'UP':
        pygame.draw.polygon(screen, BLACK, [(player_center[0], player_center[1]),
                                            (player_center[0] - CELL_SIZE // 2, player_center[1] - CELL_SIZE // 2),
                                            (player_center[0] + CELL_SIZE // 2, player_center[1] - CELL_SIZE // 2)])
        pygame.draw.circle(screen, WHITE, (player_center[0] - CELL_SIZE // 3, player_center[1] - 1), 4)
        pygame.draw.circle(screen, BLACK, (player_center[0] - CELL_SIZE // 3, player_center[1] - 2), 2)
    elif player_direction == 'DOWN':
        pygame.draw.polygon(screen, BLACK, [(player_center[0], player_center[1]),
                                            (player_center[0] + CELL_SIZE // 2, player_center[1] + CELL_SIZE // 2),
                                            (player_center[0] - CELL_SIZE // 2, player_center[1] + CELL_SIZE // 2)])
        pygame.draw.circle(screen, WHITE, (player_center[0] + CELL_SIZE // 3, player_center[1] + 1), 4)
        pygame.draw.circle(screen, BLACK, (player_center[0] + CELL_SIZE // 3, player_center[1] + 2), 2)

    # Draw food
    for food_pos in foods:
        pygame.draw.rect(screen, WHITE, ((food_pos[0] + 4) + CELL_SIZE // 3, (food_pos[1] + 3) + CELL_SIZE // 3, 5, 5))

    # Draw super-food
    for food_pos in super_food_pos:
        pygame.draw.rect(screen, WHITE, ((food_pos[0] - 1) + CELL_SIZE // 3, (food_pos[1] - 2) + CELL_SIZE // 3, 15, 15))



    # Draw enemies -------------------------------------------------------------------
    enemy_center = (enemy_pos[0] - CELL_SIZE // 2, enemy_pos[1] - CELL_SIZE // 2)
    # Check if enemies are vulnerable
    if pygame.time.get_ticks() < enemy_vulnerable_timer:
        # Draw enemies in a vulnerable state
        # Draw enemy 1 (RED)
        pygame.draw.ellipse(screen, LIGHTBLUE, (enemy_pos[0], enemy_pos[1], 40, 20))  
        pygame.draw.rect(screen, LIGHTBLUE, (enemy_pos[0], enemy_pos[1] + 9, 40, 20)) 
        pygame.draw.ellipse(screen, LIGHTBLUE, (enemy_pos[0], enemy_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, LIGHTBLUE, (enemy_pos[0] + 10, enemy_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, LIGHTBLUE, (enemy_pos[0] + 20, enemy_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, LIGHTBLUE, (enemy_pos[0] + 30, enemy_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, WHITE, (enemy_pos[0] + 6, enemy_pos[1] + 5, 10, 12)) 
        pygame.draw.ellipse(screen, WHITE, (enemy_pos[0] + 24, enemy_pos[1] + 5, 10, 12))
        pygame.draw.circle(screen, WHITE, (enemy_pos[0] + 20, enemy_pos[1] + 29), 10, 2, True, True, False, False)
        # Draw enemy 2 (GREEN)
        pygame.draw.ellipse(screen, LIGHTBLUE, (enemy2_pos[0], enemy2_pos[1], 40, 20))  
        pygame.draw.rect(screen, LIGHTBLUE, (enemy2_pos[0], enemy2_pos[1] + 9, 40, 20)) 
        pygame.draw.ellipse(screen, LIGHTBLUE, (enemy2_pos[0], enemy2_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, LIGHTBLUE, (enemy2_pos[0] + 10, enemy2_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, LIGHTBLUE, (enemy2_pos[0] + 20, enemy2_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, LIGHTBLUE, (enemy2_pos[0] + 30, enemy2_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, WHITE, (enemy2_pos[0] + 6, enemy2_pos[1] + 5, 10, 12)) 
        pygame.draw.ellipse(screen, WHITE, (enemy2_pos[0] + 24, enemy2_pos[1] + 5, 10, 12))
        pygame.draw.circle(screen, WHITE, (enemy2_pos[0] + 20, enemy2_pos[1] + 29), 10, 2, True, True, False, False)
        # Draw enemy 3 (PINK)
        pygame.draw.ellipse(screen, LIGHTBLUE, (enemy3_pos[0], enemy3_pos[1], 40, 20))  
        pygame.draw.rect(screen, LIGHTBLUE, (enemy3_pos[0], enemy3_pos[1] + 9, 40, 20)) 
        pygame.draw.ellipse(screen, LIGHTBLUE, (enemy3_pos[0], enemy3_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, LIGHTBLUE, (enemy3_pos[0] + 10, enemy3_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, LIGHTBLUE, (enemy3_pos[0] + 20, enemy3_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, LIGHTBLUE, (enemy3_pos[0] + 30, enemy3_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, WHITE, (enemy3_pos[0] + 6, enemy3_pos[1] + 5, 10, 12)) 
        pygame.draw.ellipse(screen, WHITE, (enemy3_pos[0] + 24, enemy3_pos[1] + 5, 10, 12))
        pygame.draw.circle(screen, WHITE, (enemy3_pos[0] + 20, enemy3_pos[1] + 29), 10, 2, True, True, False, False)
        # Draw enemy 4 (TEAL)
        pygame.draw.ellipse(screen, LIGHTBLUE, (enemy4_pos[0], enemy4_pos[1], 40, 20))  
        pygame.draw.rect(screen, LIGHTBLUE, (enemy4_pos[0], enemy4_pos[1] + 9, 40, 20)) 
        pygame.draw.ellipse(screen, LIGHTBLUE, (enemy4_pos[0], enemy4_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, LIGHTBLUE, (enemy4_pos[0] + 10, enemy4_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, LIGHTBLUE, (enemy4_pos[0] + 20, enemy4_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, LIGHTBLUE, (enemy4_pos[0] + 30, enemy4_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, WHITE, (enemy4_pos[0] + 6, enemy4_pos[1] + 5, 10, 12)) 
        pygame.draw.ellipse(screen, WHITE, (enemy4_pos[0] + 24, enemy4_pos[1] + 5, 10, 12))
        pygame.draw.circle(screen, WHITE, (enemy4_pos[0] + 20, enemy4_pos[1] + 29), 10, 2, True, True, False, False)

       



    else:
        # Draw enemy 1 ----------------------------------------------------------------------------
        pygame.draw.ellipse(screen, RED, (enemy_pos[0], enemy_pos[1], 40, 20))  
        pygame.draw.rect(screen, RED, (enemy_pos[0], enemy_pos[1] + 9, 40, 20)) 
        pygame.draw.ellipse(screen, RED, (enemy_pos[0], enemy_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, RED, (enemy_pos[0] + 10, enemy_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, RED, (enemy_pos[0] + 20, enemy_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, RED, (enemy_pos[0] + 30, enemy_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, WHITE, (enemy_pos[0] + 6, enemy_pos[1] + 5, 10, 12)) 
        pygame.draw.ellipse(screen, WHITE, (enemy_pos[0] + 24, enemy_pos[1] + 5, 10, 12))
        # looking right
        if enemy_direction == 'RIGHT':
            pygame.draw.ellipse(screen, BLACK, (enemy_pos[0] + 11, enemy_pos[1] + 9, 5, 5))
            pygame.draw.ellipse(screen, BLACK, (enemy_pos[0] + 29, enemy_pos[1] + 9, 5, 5))
        # Looking left
        if enemy_direction == 'LEFT':
            pygame.draw.ellipse(screen, BLACK, (enemy_pos[0] + 6, enemy_pos[1] + 9, 5, 5))
            pygame.draw.ellipse(screen, BLACK, (enemy_pos[0] + 24, enemy_pos[1] + 9, 5, 5))
        # Looking down
        if enemy_direction == 'DOWN':
            pygame.draw.ellipse(screen, BLACK, (enemy_pos[0] + 8.5, enemy_pos[1] + 12, 5, 5))
            pygame.draw.ellipse(screen, BLACK, (enemy_pos[0] + 26.5, enemy_pos[1] + 12, 5, 5))
        if enemy_direction == 'UP':
            pygame.draw.ellipse(screen, BLACK, (enemy_pos[0] + 8.5, enemy_pos[1] + 5, 5, 5))
            pygame.draw.ellipse(screen, BLACK, (enemy_pos[0] + 26.5, enemy_pos[1] + 5, 5, 5))
        

        # Draw enemy 2 -------------------------------------------------------------------
        enemy2_center = (enemy2_pos[0] - CELL_SIZE // 2, enemy2_pos[1] - CELL_SIZE // 2)
        pygame.draw.ellipse(screen, GREEN, (enemy2_pos[0], enemy2_pos[1], 40, 20))
        pygame.draw.rect(screen, GREEN, (enemy2_pos[0], enemy2_pos[1] + 9, 40, 20)) 
        pygame.draw.ellipse(screen, GREEN, (enemy2_pos[0], enemy2_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, GREEN, (enemy2_pos[0] + 10, enemy2_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, GREEN, (enemy2_pos[0] + 20, enemy2_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, GREEN, (enemy2_pos[0] + 30, enemy2_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, WHITE, (enemy2_pos[0] + 6, enemy2_pos[1] + 5, 10, 12)) 
        pygame.draw.ellipse(screen, WHITE, (enemy2_pos[0] + 24, enemy2_pos[1] + 5, 10, 12))
        # looking right
        if enemy2_direction == 'RIGHT':
            pygame.draw.ellipse(screen, BLACK, (enemy2_pos[0] + 11, enemy2_pos[1] + 9, 5, 5))
            pygame.draw.ellipse(screen, BLACK, (enemy2_pos[0] + 29, enemy2_pos[1] + 9, 5, 5))
        # Looking left
        if enemy2_direction == 'LEFT':
            pygame.draw.ellipse(screen, BLACK, (enemy2_pos[0] + 6, enemy2_pos[1] + 9, 5, 5))
            pygame.draw.ellipse(screen, BLACK, (enemy2_pos[0] + 24, enemy2_pos[1] + 9, 5, 5))
        # Looking down
        if enemy2_direction == 'DOWN':
            pygame.draw.ellipse(screen, BLACK, (enemy2_pos[0] + 8.5, enemy2_pos[1] + 12, 5, 5))
            pygame.draw.ellipse(screen, BLACK, (enemy2_pos[0] + 26.5, enemy2_pos[1] + 12, 5, 5))
        if enemy2_direction == 'UP':
            pygame.draw.ellipse(screen, BLACK, (enemy2_pos[0] + 8.5, enemy2_pos[1] + 5, 5, 5))
            pygame.draw.ellipse(screen, BLACK, (enemy2_pos[0] + 26.5, enemy2_pos[1] + 5, 5, 5))

        # Draw enemy 3 -------------------------------------------------------------------
        enemy3_center = (enemy3_pos[0] - CELL_SIZE // 2, enemy3_pos[1] - CELL_SIZE // 2)
        pygame.draw.ellipse(screen, PINK, (enemy3_pos[0], enemy3_pos[1], 40, 20))
        pygame.draw.rect(screen, PINK, (enemy3_pos[0], enemy3_pos[1] + 9, 40, 20)) 
        pygame.draw.ellipse(screen, PINK, (enemy3_pos[0], enemy3_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, PINK, (enemy3_pos[0] + 10, enemy3_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, PINK, (enemy3_pos[0] + 20, enemy3_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, PINK, (enemy3_pos[0] + 30, enemy3_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, WHITE, (enemy3_pos[0] + 6, enemy3_pos[1] + 5, 10, 12)) 
        pygame.draw.ellipse(screen, WHITE, (enemy3_pos[0] + 24, enemy3_pos[1] + 5, 10, 12))
        # looking right
        if enemy3_direction == 'RIGHT':
            pygame.draw.ellipse(screen, BLACK, (enemy3_pos[0] + 11, enemy3_pos[1] + 9, 5, 5))
            pygame.draw.ellipse(screen, BLACK, (enemy3_pos[0] + 29, enemy3_pos[1] + 9, 5, 5))
        # Looking left
        if enemy3_direction == 'LEFT':
            pygame.draw.ellipse(screen, BLACK, (enemy3_pos[0] + 6, enemy3_pos[1] + 9, 5, 5))
            pygame.draw.ellipse(screen, BLACK, (enemy3_pos[0] + 24, enemy3_pos[1] + 9, 5, 5))
        # Looking down
        if enemy3_direction == 'DOWN':
            pygame.draw.ellipse(screen, BLACK, (enemy3_pos[0] + 8.5, enemy3_pos[1] + 12, 5, 5))
            pygame.draw.ellipse(screen, BLACK, (enemy3_pos[0] + 26.5, enemy3_pos[1] + 12, 5, 5))
        if enemy3_direction == 'UP':
            pygame.draw.ellipse(screen, BLACK, (enemy3_pos[0] + 8.5, enemy3_pos[1] + 5, 5, 5))
            pygame.draw.ellipse(screen, BLACK, (enemy3_pos[0] + 26.5, enemy3_pos[1] + 5, 5, 5))
        
        # Draw enemy 4 -------------------------------------------------------------------
        enemy4_center = (enemy4_pos[0] - CELL_SIZE // 2, enemy4_pos[1] - CELL_SIZE // 2)
        pygame.draw.ellipse(screen, TEAL, (enemy4_pos[0], enemy4_pos[1], 40, 20))
        pygame.draw.rect(screen, TEAL, (enemy4_pos[0], enemy4_pos[1] + 9, 40, 20)) 
        pygame.draw.ellipse(screen, TEAL, (enemy4_pos[0], enemy4_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, TEAL, (enemy4_pos[0] + 10, enemy4_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, TEAL, (enemy4_pos[0] + 20, enemy4_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, TEAL, (enemy4_pos[0] + 30, enemy4_pos[1] + 20, 10, 20)) 
        pygame.draw.ellipse(screen, WHITE, (enemy4_pos[0] + 6, enemy4_pos[1] + 5, 10, 12)) 
        pygame.draw.ellipse(screen, WHITE, (enemy4_pos[0] + 24, enemy4_pos[1] + 5, 10, 12))
        # looking right
        if enemy4_direction == 'RIGHT':
            pygame.draw.ellipse(screen, BLACK, (enemy4_pos[0] + 11, enemy4_pos[1] + 9, 5, 5))
            pygame.draw.ellipse(screen, BLACK, (enemy4_pos[0] + 29, enemy4_pos[1] + 9, 5, 5))
        # Looking left
        if enemy4_direction == 'LEFT':
            pygame.draw.ellipse(screen, BLACK, (enemy4_pos[0] + 6, enemy4_pos[1] + 9, 5, 5))
            pygame.draw.ellipse(screen, BLACK, (enemy4_pos[0] + 24, enemy4_pos[1] + 9, 5, 5))
        # Looking down
        if enemy4_direction == 'DOWN':
            pygame.draw.ellipse(screen, BLACK, (enemy4_pos[0] + 8.5, enemy4_pos[1] + 12, 5, 5))
            pygame.draw.ellipse(screen, BLACK, (enemy4_pos[0] + 26.5, enemy4_pos[1] + 12, 5, 5))
        if enemy4_direction == 'UP':
            pygame.draw.ellipse(screen, BLACK, (enemy4_pos[0] + 8.5, enemy4_pos[1] + 5, 5, 5))
            pygame.draw.ellipse(screen, BLACK, (enemy4_pos[0] + 26.5, enemy4_pos[1] + 5, 5, 5))



    # Draw map
    for rect in rectangles:
        pygame.draw.rect(screen, BLUE, rect, 3)

    
    font = pygame.font.SysFont(None, 24)

    # Draw Debug info (comment every line after testing)
    #pos = str(player_pos)
    #img = font.render(pos, True, YELLOW)
    #screen.blit(img, (20, 20))
    #pos2 = str(enemy_pos)
    #img2 = font.render(pos2, True, YELLOW)
    #screen.blit(img2, (150, 20))


    # Draw Score
    score_str = "Score: " + str(score)
    score_img = font.render(score_str, True, YELLOW)
    screen.blit(score_img, (710, 15))

    # Win condition  (total of 121 foods, including the super-foods.)
    if (score >= 121):
        about_me()

    pygame.display.flip()

# Quit Pygame
pygame.quit()
