import pygame
import random
import sys

# Constants
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
FPS = 5
SCORE_SPEED_INCREMENT = 50  # Number of points required to increase speed
SNAKE_SPEED = 8  # Initial speed

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Xenia")
        self.clock = pygame.time.Clock()
        self.running = False
        self.game_over = False
        self.snake = Snake(self)
        self.food = Food(self)
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.speed = SNAKE_SPEED

    def run(self):
        while not self.game_over:
            self.handle_events()
            if self.running:
                self.update()
                self.draw()
                self.clock.tick(self.speed)
            else:
                self.show_start_screen()
        
        # Show the "Game Over" screen and wait for a key press to continue
        self.show_game_over_screen()
        self.wait_for_key()
        pygame.quit()
        sys.exit()  # Ensure the application exits when the game ends

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            elif event.type == pygame.KEYDOWN:
                if not self.running:
                    self.running = True  # Start the game on any key press
                if event.key == pygame.K_UP:
                    self.snake.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction(RIGHT)

    def show_start_screen(self):
        self.screen.fill(BLACK)
        text = self.font.render("Tap any key to start", True, GREEN)
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

    def show_game_over_screen(self):
        self.screen.fill(BLACK)
        game_over_text = self.font.render("Game Over", True, RED)
        game_over_text_rect = game_over_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 20))
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        score_text_rect = score_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 20))
        self.screen.blit(game_over_text, game_over_text_rect)
        self.screen.blit(score_text, score_text_rect)
        pygame.display.flip()

    def wait_for_key(self):
        waiting_for_key = True
        while waiting_for_key:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    waiting_for_key = False

    def calculate_speed(self):
        if self.score >= SCORE_SPEED_INCREMENT:
            self.speed = SNAKE_SPEED + (self.score // SCORE_SPEED_INCREMENT)
        else:
            self.speed = SNAKE_SPEED
        return self.speed

    def update(self):
        self.snake.move()
        if self.snake.check_collision():
            self.game_over = True
        if self.snake.head == self.food.position:
            self.snake.grow()
            self.food.randomize_position()
            self.score += 1

    def draw(self):
        self.screen.fill(BLACK)
        self.snake.draw()
        self.food.draw()
        self.display_score()  # Display score on the screen
        pygame.display.flip()

    def display_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

class Snake:
    def __init__(self, game):
        self.game = game
        self.body = [(5, 5)]
        self.direction = RIGHT

    @property
    def head(self):
        return self.body[0]

    def change_direction(self, new_direction):
        if (
            (new_direction == UP and self.direction != DOWN) or
            (new_direction == DOWN and self.direction != UP) or
            (new_direction == LEFT and self.direction != RIGHT) or
            (new_direction == RIGHT and self.direction != LEFT)
        ):
            self.direction = new_direction

    def move(self):
        new_head = (self.head[0] + self.direction[0], self.head[1] + self.direction[1])
        self.body.insert(0, new_head)
        if self.head == self.game.food.position:
            return
        self.body.pop()

    def check_collision(self):
        if (
            self.head in self.body[1:] or
            self.head[0] < 0 or self.head[0] >= WIDTH // CELL_SIZE or
            self.head[1] < 0 or self.head[1] >= HEIGHT // CELL_SIZE
        ):
            return True
        return False

    def grow(self):
        self.body.append((0, 0))  # Dummy values; the new segment will be adjusted in the move function

    def draw(self):
        for segment in self.body:
            x, y = segment
            pygame.draw.rect(self.game.screen, GREEN, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

class Food:
    def __init__(self, game):
        self.game = game
        self.position = (random.randint(0, WIDTH // CELL_SIZE - 1), random.randint(0, HEIGHT // CELL_SIZE - 1))

    def randomize_position(self):
        self.position = (random.randint(0, WIDTH // CELL_SIZE - 1), random.randint(0, HEIGHT // CELL_SIZE - 1))

    def draw(self):
        x, y = self.position
        pygame.draw.rect(self.game.screen, RED, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
