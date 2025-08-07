import pygame
import random
import sys
import os

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (160, 32, 240)
WHITE = (255, 255, 255)

# Font
font = pygame.font.SysFont("Arial", 24)

# Clock
clock = pygame.time.Clock()
FPS = 10

# Snake and food
snake = [(100, 100), (80, 100), (60, 100)]
direction = (20, 0)
score = 0

# Food types
food_types = [
    {"color": RED, "points": 1},
    {"color": PURPLE, "points": 2}
]
food = {
    "pos": (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
            random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE),
    "type": random.choice(food_types)
}

# Score file
SCORE_FILE = "scores.txt"

def save_score(new_score):
    with open(SCORE_FILE, "a") as f:
        f.write(str(new_score) + "\n")

def load_top_scores(limit=5):
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as f:
            scores = [int(line.strip()) for line in f if line.strip().isdigit()]
            return sorted(scores, reverse=True)[:limit]
    return []

def draw_snake():
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

def draw_food():
    pygame.draw.rect(screen, food["type"]["color"], (*food["pos"], CELL_SIZE, CELL_SIZE))

def draw_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def move_snake():
    global food, score
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, new_head)

    if new_head == food["pos"]:
        score += food["type"]["points"]
        food = {
            "pos": (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                    random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE),
            "type": random.choice(food_types)
        }
    else:
        snake.pop()

def check_collision():
    head = snake[0]
    return (
        head[0] < 0 or head[0] >= WIDTH or
        head[1] < 0 or head[1] >= HEIGHT or
        head in snake[1:]
    )

def show_leaderboard():
    top_scores = load_top_scores()
    print("\n🏆 Leaderboard:")
    for i, s in enumerate(top_scores, 1):
        print(f"{i}. {s} points")

# Game loop
while True:
    screen.fill(BLACK)
    draw_snake()
    draw_food()
    draw_score()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 20):
                direction = (0, -20)
            elif event.key == pygame.K_DOWN and direction != (0, -20):
                direction = (0, 20)
            elif event.key == pygame.K_LEFT and direction != (20, 0):
                direction = (-20, 0)
            elif event.key == pygame.K_RIGHT and direction != (-20, 0):
                direction = (20, 0)

    move_snake()
    if check_collision():
        save_score(score)
        pygame.quit()
        print(f"\nGame Over! Final Score: {score}")
        show_leaderboard()
        sys.exit()

    clock.tick(FPS)
