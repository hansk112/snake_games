import curses
from random import randint

# Setup window
screen = curses.initscr()
curses.curs_set(0)
win = curses.newwin(20, 60, 0, 0)  # height, width, start_y, start_x
win.keypad(1)
win.timeout(100)  # screen refresh rate in ms

# Initial snake and food
snake = [(4, 10), (4, 9), (4, 8)]
food = (10, 20)
win.addch(food[0], food[1], '🍎')

# Game logic
key = curses.KEY_RIGHT
score = 0

while True:
    next_key = win.getch()
    key = key if next_key == -1 else next_key

    # Calculate new head
    y = snake[0][0]
    x = snake[0][1]
    if key == curses.KEY_DOWN:
        y += 1
    elif key == curses.KEY_UP:
        y -= 1
    elif key == curses.KEY_LEFT:
        x -= 1
    elif key == curses.KEY_RIGHT:
        x += 1
    new_head = (y, x)

    # Game over conditions
    if (
        y in [0, 19] or x in [0, 59] or
        new_head in snake
    ):
        curses.endwin()
        print(f"Game Over! Final Score: {score}")
        break

    snake.insert(0, new_head)

    # Food eaten
    if new_head == food:
        score += 1
        food = (randint(1, 18), randint(1, 58))
        win.addch(food[0], food[1], '🍎')
    else:
        tail = snake.pop()
        win.addch(tail[0], tail[1], ' ')

    win.addch(snake[0][0], snake[0][1], '🟩')
