import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Falling Objects")

# Player settings
player_width = 100
player_height = 20
player_x = (WIDTH - player_width) // 2
player_y = HEIGHT - player_height - 10
player_speed = 8
use_keyboard = True  # Default control method is keyboard

# Object settings
object_width = 40
object_height = 40
object_x = random.randint(0, WIDTH - object_width)
object_y = 0
object_speed_level1 = 6  # Speed in level 1
object_speed_level2 = 8  # Speed in level 2

# Score
score = 0
font = pygame.font.Font(None, 36)

# Timer
start_time = None  # Start time for level 1
level_duration = 30  # Level 1 duration in seconds (6 minutes)

# Timer for Level 2 notification
level2_notification_start_time = None
level2_notification_duration = 2  # 2 seconds

def draw_score():
    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))

def draw_level(level):
    level_text = font.render("Level " + str(level), True, BLACK)
    screen.blit(level_text, (WIDTH - 100, 10))

def draw_level_notification():
    if level == 2:
        level_notification_text = font.render("Level 2 - Faster Objects!", True, RED)
        screen.blit(level_notification_text, (WIDTH // 2 - 150, HEIGHT // 2 + 100))

def draw_game_over():
    game_over_text = font.render("Game Over", True, BLACK)
    restart_text = font.render("Press R to Restart", True, BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - 70, HEIGHT // 2 - 50))
    screen.blit(restart_text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
    pygame.display.flip()

def welcome_screen():
    screen.fill(WHITE)
    welcome_text = font.render("Welcome to Catch the Falling Objects!", True, BLACK)
    start_text = font.render("Press Enter to Start", True, BLACK)
    screen.blit(welcome_text, (WIDTH // 2 - 200, HEIGHT // 2 - 50))
    screen.blit(start_text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
    pygame.display.flip()

def restart_game():
    global score, object_x, object_y, use_keyboard, level, start_time
    score = 0
    object_x = random.randint(0, WIDTH - object_width)
    object_y = 0
    use_keyboard = True
    level = 1  # Start at level 1
    start_time = None

def game_over():
    global running
    screen.fill(WHITE)
    draw_game_over()
    waiting_for_restart = True
    while waiting_for_restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                restart_game()
                waiting_for_restart = False

# Display the welcome screen initially
welcome_screen()
waiting_for_start = True
level = 1  # Start at level 1

# Game loop
clock = pygame.time.Clock()
running = False  # The game loop is initially not running

while waiting_for_start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting_for_start = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            running = True
            waiting_for_start = False
            start_time = pygame.time.get_ticks()  # Start the timer

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if use_keyboard:
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed

        # Boundary checks for player
        if player_x < 0:
            player_x = 0
        elif player_x > WIDTH - player_width:
            player_x = WIDTH - player_width
    else:
        # Use the mouse for control
        player_x = pygame.mouse.get_pos()[0] - player_width / 2

    # Move the falling object
    if level == 1:
        object_y += object_speed_level1
    elif level == 2:
        object_y += object_speed_level2

    # Check if object missed
    if object_y > HEIGHT:
        game_over()

    # Check for collision
    if (
        player_x < object_x + object_width
        and player_x + player_width > object_x
        and player_y < object_y + object_height
        and player_y + player_height > object_y
    ):
        score += 1
        object_x = random.randint(0, WIDTH - object_width)
        object_y = 0

    # Level up condition: Updated to check the player's score
    if start_time is not None and score >= 20 and level == 1:
        level = 2
        object_speed_level2 = 10  # Increase speed in level 2

        # Set the Level 2 notification start time
        level2_notification_start_time = pygame.time.get_ticks()

    # Draw everything
    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, (player_x, player_y, player_width, player_height))
    pygame.draw.rect
    pygame.draw.rect(screen, BLACK, (object_x, object_y, object_width, object_height))
    draw_score()
    draw_level(level)

    # Show control method
    control_text = font.render("Control: Keyboard" if use_keyboard else "Control: Mouse", True, BLACK)
    screen.blit(control_text, (10, 40))

    # Draw Level 2 notification if applicable
    if level == 2 and level2_notification_start_time is not None:
        current_time = pygame.time.get_ticks()
        if current_time - level2_notification_start_time < (level2_notification_duration * 1000):
            draw_level_notification()
        else:
            level2_notification_start_time = None

    pygame.display.flip()

    # FPS control
    clock.tick(FPS)

# Quit the game
pygame.quit()

