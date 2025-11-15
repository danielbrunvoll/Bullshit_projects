import random
import tkinter as tk
from tkinter import messagebox, Scale, HORIZONTAL

class Minesweeper:
    def __init__(self, width=10, height=10, mines=10):
        if mines >= width * height:
            mines = width * height - 1
            
        self.width = width
        self.height = height
        self.mines = mines
        self.board = [[' ' for _ in range(width)] for _ in range(height)]
        self.mask = [['?' for _ in range(width)] for _ in range(height)]
        self.game_over = False
        self.win = False
        self.first_click = True
        
    def _place_mines(self, first_y, first_x):
        mine_positions = set()
        safe_area = self._get_neighbors(first_y, first_x)
        safe_area.append((first_y, first_x))

        max_mines = self.width * self.height - len(safe_area)
        if self.mines > max_mines:
            self.mines = max_mines

        while len(mine_positions) < self.mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            
            if (y, x) not in safe_area and (y, x) not in mine_positions:
                mine_positions.add((y, x))
        
        for y_pos, x_pos in mine_positions:
            self.board[y_pos][x_pos] = '*'

    def _get_neighbors(self, y, x):
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                ny, nx = y + i, x + j
                if 0 <= ny < self.height and 0 <= nx < self.width:
                    neighbors.append((ny, nx))
        return neighbors

    def _calculate_adjacent_mines(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == '*':
                    continue
                mine_count = 0
                for ny, nx in self._get_neighbors(y, x):
                    if self.board[ny][nx] == '*':
                        mine_count += 1
                if mine_count > 0:
                    self.board[y][x] = str(mine_count)

    def reveal(self, y, x):
        if not (0 <= y < self.height and 0 <= x < self.width) or self.game_over:
            return

        if self.first_click:
            self._place_mines(y,x)
            self._calculate_adjacent_mines()
            self.first_click = False

        if self.mask[y][x] != '?':
            return

        self.mask[y][x] = self.board[y][x]

        if self.board[y][x] == '*':
            self.game_over = True
            return

        if self.board[y][x] == ' ':
            for ny, nx in self._get_neighbors(y, x):
                self.reveal(ny, nx)
        
        self._check_win()

    def flag(self, y, x):
        if not (0 <= y < self.height and 0 <= x < self.width) or self.game_over:
            return
        if self.mask[y][x] == '?':
            self.mask[y][x] = 'F'
        elif self.mask[y][x] == 'F':
            self.mask[y][x] = '?'

    def _check_win(self):
        revealed_count = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.mask[y][x] != '?' and self.mask[y][x] != 'F':
                    revealed_count += 1
        if revealed_count == (self.width * self.height) - self.mines:
            self.win = True
            self.game_over = True

class MinesweeperGUI:
    def __init__(self, master, settings):
        self.master = master
        self.settings = settings
        self.choice = None 

        self.master.title("Minesweeper")
        self.game = Minesweeper(**settings)
        self.buttons = [[None for _ in range(self.game.width)] for _ in range(self.game.height)]
        
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        self.create_widgets()
        self.update_board()

    def on_close(self):
        self.choice = 'exit'
        self.master.destroy()

    def create_widgets(self):
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        for y in range(self.game.height):
            for x in range(self.game.width):
                button = tk.Button(self.frame, width=2, height=1, text='',
                                   command=lambda y=y, x=x: self.on_click(y, x))
                button.bind("<Button-3>", lambda e, y=y, x=x: self.on_right_click(y, x))
                button.grid(row=y, column=x)
                self.buttons[y][x] = button

    def on_click(self, y, x):
        if self.game.game_over:
            return
        self.game.reveal(y, x)
        self.update_board()
        if self.game.game_over:
            self.show_game_over()

    def on_right_click(self, y, x):
        if self.game.game_over:
            return
        self.game.flag(y, x)
        self.update_board()

    def update_board(self):
        for y in range(self.game.height):
            for x in range(self.game.width):
                cell = self.game.mask[y][x]
                button = self.buttons[y][x]
                
                if cell == '?':
                    button.config(text='', state=tk.NORMAL, relief=tk.RAISED)
                elif cell == 'F':
                    button.config(text='F', state=tk.NORMAL, relief=tk.RAISED, fg='red')
                else:
                    button.config(text=cell, state=tk.DISABLED, relief=tk.SUNKEN)
                    if cell == '*':
                        button.config(text='*', bg='red')
                    elif cell != ' ':
                        colors = {
                            '1': 'blue', '2': 'green', '3': 'red',
                            '4': 'purple', '5': 'maroon', '6': 'turquoise',
                            '7': 'black', '8': 'gray'
                        }
                        button.config(disabledforeground=colors.get(cell, 'black'))

    def show_game_over(self):
        for y in range(self.game.height):
            for x in range(self.game.width):
                if self.game.board[y][x] == '*':
                    self.buttons[y][x].config(text='*', bg='red', state=tk.DISABLED)
        
        self.show_game_over_dialog()

    def show_game_over_dialog(self):
        dialog = tk.Toplevel(self.master)
        dialog.title("Game Over")
        
        message = "Congratulations! You won!" if self.game.win else "Game Over! You hit a mine."
        tk.Label(dialog, text=message, font=('Helvetica', 12)).pack(pady=10, padx=20)

        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=10)

        def on_retry():
            self.choice = 'retry'
            dialog.destroy()
            self.master.destroy()

        def on_menu():
            self.choice = 'menu'
            dialog.destroy()
            self.master.destroy()

        def on_exit():
            self.choice = 'exit'
            dialog.destroy()
            self.master.destroy()

        tk.Button(btn_frame, text="Retry", command=on_retry).pack(side='left', padx=10)
        tk.Button(btn_frame, text="Back to Menu", command=on_menu).pack(side='left', padx=10)
        tk.Button(btn_frame, text="Exit", command=on_exit).pack(side='left', padx=10)

        dialog.transient(self.master)
        dialog.grab_set()
        self.master.wait_window(dialog)


class StartMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("New Game")
        self.settings = None
        self.choice = None

        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        self.difficulty = tk.StringVar(value="Easy")
        
        tk.Label(master, text="Select Difficulty:").pack(pady=5)

        tk.Radiobutton(master, text="Easy (10x10, 10 mines)", variable=self.difficulty, value="Easy", command=self.toggle_sliders).pack(anchor='w', padx=20)
        tk.Radiobutton(master, text="Medium (16x16, 40 mines)", variable=self.difficulty, value="Medium", command=self.toggle_sliders).pack(anchor='w', padx=20)
        tk.Radiobutton(master, text="Hard (30x16, 99 mines)", variable=self.difficulty, value="Hard", command=self.toggle_sliders).pack(anchor='w', padx=20)
        tk.Radiobutton(master, text="Custom", variable=self.difficulty, value="Custom", command=self.toggle_sliders).pack(anchor='w', padx=20)

        self.slider_frame = tk.Frame(master)
        self.slider_frame.pack(pady=10, padx=20)

        self.rows_val = tk.IntVar(value=10)
        self.cols_val = tk.IntVar(value=10)
        self.mines_val = tk.IntVar(value=10)

        self.rows_slider = Scale(self.slider_frame, from_=5, to=30, orient=HORIZONTAL, label="Rows", variable=self.rows_val, command=self.update_mines_slider)
        self.rows_slider.pack(fill='x')
        self.cols_slider = Scale(self.slider_frame, from_=5, to=30, orient=HORIZONTAL, label="Columns", variable=self.cols_val, command=self.update_mines_slider)
        self.cols_slider.pack(fill='x')
        self.mines_slider = Scale(self.slider_frame, from_=1, to=99, orient=HORIZONTAL, label="Mines", variable=self.mines_val)
        self.mines_slider.pack(fill='x')

        self.toggle_sliders()

        tk.Button(master, text="Start Game", command=self.start_game).pack(pady=10)

    def on_close(self):
        self.choice = 'exit'
        self.master.destroy()

    def toggle_sliders(self):
        if self.difficulty.get() == "Custom":
            for widget in self.slider_frame.winfo_children():
                widget.config(state=tk.NORMAL)
        else:
            for widget in self.slider_frame.winfo_children():
                widget.config(state=tk.DISABLED)

    def update_mines_slider(self, _=None):
        if self.difficulty.get() == "Custom":
            rows = self.rows_val.get()
            cols = self.cols_val.get()
            max_mines = int(rows * cols * 0.9)
            if max_mines < 1:
                max_mines = 1
            self.mines_slider.config(to=max_mines)
            if self.mines_val.get() > max_mines:
                self.mines_val.set(max_mines)

    def start_game(self):
        diff = self.difficulty.get()
        if diff == "Easy":
            self.settings = {"width": 10, "height": 10, "mines": 10}
        elif diff == "Medium":
            self.settings = {"width": 16, "height": 16, "mines": 40}
        elif diff == "Hard":
            self.settings = {"width": 30, "height": 16, "mines": 99}
        elif diff == "Custom":
            self.settings = {
                "width": self.cols_val.get(),
                "height": self.rows_val.get(),
                "mines": self.mines_val.get()
            }
        self.choice = 'start'
        self.master.destroy()

def main():
    root = tk.Tk()
    root.withdraw()
    
    game_settings = None
    
    while True:
        start_menu_window = tk.Toplevel(root)
        start_menu = StartMenu(start_menu_window)
        start_menu_window.wait_window()

        if start_menu.choice == 'start':
            game_settings = start_menu.settings
        elif start_menu.choice == 'exit':
            break

        if game_settings:
            while True:
                game_window = tk.Toplevel(root)
                game_app = MinesweeperGUI(game_window, game_settings)
                game_window.wait_window()

                if game_app.choice == 'retry':
                    continue
                elif game_app.choice == 'menu':
                    break 
                elif game_app.choice == 'exit':
                    root.destroy()
                    return
        else:
            break

    root.destroy()

if __name__ == '__main__':
    main()
