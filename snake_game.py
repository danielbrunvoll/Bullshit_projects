import tkinter as tk
import random

# --- constants ---
WIDTH = 500
HEIGHT = 500
SPEED = 100
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "#39FF14"
FOOD_COLOR = "#FF4136"
BACKGROUND_COLOR = "#222222"
TEXT_COLOR = "#FFFFFF"
FONT_NAME = "Segoe UI"


pending_directions = []


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake"
            )
            self.squares.append(square)


class Food:
    def __init__(self):
        x = random.randint(0, (WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food"
        )


def next_turn(snake, food):
    global direction

    if pending_directions:
        new_dir = pending_directions.pop(0)
        if new_dir == 'left':
            if direction != 'right':
                direction = new_dir
        elif new_dir == 'right':
            if direction != 'left':
                direction = new_dir
        elif new_dir == 'up':
            if direction != 'down':
                direction = new_dir
        elif new_dir == 'down':
            if direction != 'up':
                direction = new_dir
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR
    )

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global pending_directions
    if len(pending_directions) < 2:
        pending_directions.append(new_direction)


def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= WIDTH:
        return True
    if y < 0 or y >= HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    canvas.delete(tk.ALL)
    canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2 - 40,
        font=(FONT_NAME, 60, "bold"),
        text="GAME OVER",
        fill=FOOD_COLOR,
        tag="gameover",
    )

    button_style = {
        "font": (FONT_NAME, 14),
        "bg": "#444444",
        "fg": TEXT_COLOR,
        "activebackground": "#555555",
        "activeforeground": TEXT_COLOR,
        "borderwidth": 0,
        "relief": "flat",
        "padx": 10,
        "pady": 5
    }

    retry_button = tk.Button(window, text="Retry", command=restart_game, **button_style)
    canvas.create_window(canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 40, window=retry_button)

    exit_button = tk.Button(window, text="Exit", command=window.destroy, **button_style)
    canvas.create_window(canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 90, window=exit_button)

def restart_game():
    global snake, food, score, direction, pending_directions
    
    canvas.delete("all")
    
    score = 0
    direction = 'down'
    pending_directions = []
    label.config(text="Score:{}".format(score))
    
    snake = Snake()
    food = Food()
    
    next_turn(snake, food)


window = tk.Tk()
window.title("Snake game")
window.resizable(False, False)
window.config(bg=BACKGROUND_COLOR)

score = 0
direction = "down"

label = tk.Label(window, text="Score:{}".format(score), font=(FONT_NAME, 24), fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
label.pack(pady=10)

canvas = tk.Canvas(window, bg=BACKGROUND_COLOR, height=HEIGHT, width=WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()
