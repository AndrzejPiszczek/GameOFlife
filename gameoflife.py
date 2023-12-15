import pygame
import numpy as np
import tkinter as tk
from tkinter import messagebox
import pickle
from tkinter import messagebox
from tkinter import filedialog
# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Grid dimensions
n_cells_x, n_cells_y = 40, 30
cell_width = width // n_cells_x
cell_height = height // n_cells_y

# Game state
game_state = np.random.choice([0, 1], size=(n_cells_x, n_cells_y), p=[0.8, 0.2])
paused = False

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Button dimensions and positions
button_width, button_height = 100, 50
pause_button_x, pause_button_y = 10, 10
save_button_x, save_button_y = 120, 10
load_button_x, load_button_y = 230, 10

def draw_button(x, y, text, color):
    pygame.draw.rect(screen, color, (x, y, button_width, button_height))
    font = pygame.font.Font(None, 36)
    text = font.render(text, True, black)
    text_rect = text.get_rect(center=(x + button_width // 2, y + button_height // 2))
    screen.blit(text, text_rect)

def draw_grid():
    for y in range(0, height, cell_height):
        for x in range(0, width, cell_width):
            cell = pygame.Rect(x, y, cell_width, cell_height)
            pygame.draw.rect(screen, gray, cell, 1)

def next_generation():
    global game_state
    new_state = np.copy(game_state)

    for y in range(n_cells_y):
        for x in range(n_cells_x):
            n_neighbors = sum([game_state[(x + dx) % n_cells_x, (y + dy) % n_cells_y]
                               for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx != 0 or dy != 0)])

            if game_state[x, y] == 1 and (n_neighbors < 2 or n_neighbors > 3):
                new_state[x, y] = 0
            elif game_state[x, y] == 0 and n_neighbors == 3:
                new_state[x, y] = 1

    game_state = new_state

def draw_cells():
    for y in range(n_cells_y):
        for x in range(n_cells_x):
            cell = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)
            if game_state[x, y] == 1:
                pygame.draw.rect(screen, black, cell)


def save_game(self):
    filepath = filedialog.asksaveasfilename(
        defaultextension=".gol",
        filetypes=[("Game of Life files", "*.gol"), ("All files", "*.*")],
    )
    if not filepath:
        return

    try:
        with open(filepath, "wb") as file:
            pickle.dump([[cell.is_alive for cell in row]
                         for row in self.game.grid], file)
        messagebox.showinfo(
            "Save Game", "The game was successfully saved!")
    except Exception as e:
        messagebox.showerror("Save Game", f"An error occurred: {e}")


def load_game(self):
    filepath = filedialog.askopenfilename(
        filetypes=[("Game of Life files", "*.gol"), ("All files", "*.*")]
    )
    if not filepath:
        return

    try:
        with open(filepath, "rb") as file:
            grid_state = pickle.load(file)

        for i in range(self.rows):
            for j in range(self.cols):
                self.game.grid[i][j].update(grid_state[i][j])
        self.update_canvas()
        messagebox.showinfo(
            "Load Game", "The game was successfully loaded!")
    except Exception as e:
        messagebox.showerror("Load Game", f"An error occurred: {e}")

running = True
clock = pygame.time.Clock()
while running:
    screen.fill(white)
    draw_grid()
    draw_cells()
    draw_button(pause_button_x, pause_button_y, "Pause" if not paused else "Resume", red)
    draw_button(save_button_x, save_button_y, "Save", green)
    draw_button(load_button_x, load_button_y, "Load", blue)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pause_button_x <= event.pos[0] <= pause_button_x + button_width and pause_button_y <= event.pos[1] <= pause_button_y + button_height:
                paused = not paused
            elif save_button_x <= event.pos[0] <= save_button_x + button_width and save_button_y <= event.pos[1] <= save_button_y + button_height:
                save_game()
            elif load_button_x <= event.pos[0] <= load_button_x + button_width and load_button_y <= event.pos[1] <= load_button_y + button_height:
                load_game()
            else:
                x, y = event.pos[0] // cell_width, event.pos[1] // cell_height
                game_state[x, y] = not game_state[x, y]

    if not paused:
        next_generation()

    clock.tick(10)  # Control the frame rate

pygame.quit()