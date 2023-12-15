import pygame
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
import pickle

# Initialize both Pygame and Tkinter
pygame.init()
tk_root = tk.Tk()
tk_root.withdraw()  # Hide the main Tkinter window

class GameOfLife:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.n_cells_x, self.n_cells_y = 40, 30
        self.cell_width = self.width // self.n_cells_x
        self.cell_height = (self.height - 100) // self.n_cells_y  # Adjust for button area
        self.game_state = np.random.choice([0, 1], size=(self.n_cells_x, self.n_cells_y), p=[0.8, 0.2])
        self.paused = False
        self.font = pygame.font.Font(None, 36)

        # Define button positions and sizes
        button_y = self.height - 80
        self.pause_button = pygame.Rect(10, button_y, 120, 50)
        self.save_button = pygame.Rect(140, button_y, 100, 50)
        self.load_button = pygame.Rect(260, button_y, 100, 50)

    def draw_grid(self):
        for y in range(0, self.height - 100, self.cell_height):  # Adjust the grid height
            for x in range(0, self.width, self.cell_width):
                cell = pygame.Rect(x, y, self.cell_width, self.cell_height)
                pygame.draw.rect(self.screen, (128, 128, 128), cell, 1)

    def draw_cells(self):
        for y in range(self.n_cells_y):
            for x in range(self.n_cells_x):
                cell = pygame.Rect(x * self.cell_width, y * self.cell_height, self.cell_width, self.cell_height)
                if self.game_state[x, y] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 0), cell)

    def draw_buttons(self):
        pygame.draw.rect(self.screen, (255, 165, 0), self.pause_button)  # Orange button
        pause_text = self.font.render('Pause' if not self.paused else 'Resume', True, (255, 255, 255))
        self.screen.blit(pause_text, (self.pause_button.x + 10, self.pause_button.y + 10))

        pygame.draw.rect(self.screen, (0, 191, 255), self.save_button)  # Deep Sky Blue button
        save_text = self.font.render('Save', True, (255, 255, 255))
        self.screen.blit(save_text, (self.save_button.x + 20, self.save_button.y + 10))

        pygame.draw.rect(self.screen, (34, 139, 34), self.load_button)  # Forest Green button
        load_text = self.font.render('Load', True, (255, 255, 255))
        self.screen.blit(load_text, (self.load_button.x + 20, self.load_button.y + 10))

    def handle_button_click(self, pos):
        if self.pause_button.collidepoint(pos):
            self.paused = not self.paused
        elif self.save_button.collidepoint(pos):
            self.save_game()
        elif self.load_button.collidepoint(pos):
            self.load_game()

    def next_generation(self):
        new_state = np.copy(self.game_state)
        for y in range(self.n_cells_y):
            for x in range(self.n_cells_x):
                n_neighbors = sum([self.game_state[(x + dx) % self.n_cells_x, (y + dy) % self.n_cells_y]
                                   for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx != 0 or dy != 0)])
                if self.game_state[x, y] == 1 and (n_neighbors < 2 or n_neighbors > 3):
                    new_state[x, y] = 0
                elif self.game_state[x, y] == 0 and n_neighbors == 3:
                    new_state[x, y] = 1
        self.game_state = new_state

    def save_game(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".gol",
            filetypes=[("Game of Life files", "*.gol"), ("All files", "*.*")],
        )
        if not filepath:
            return
        try:
            with open(filepath, "wb") as file:
                pickle.dump(self.game_state, file)
            messagebox.showinfo("Save Game", "The game was successfully saved!")
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
                self.game_state = pickle.load(file)
            messagebox.showinfo("Load Game", "The game was successfully loaded!")
        except Exception as e:
            messagebox.showerror("Load Game", f"An error occurred: {e}")

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            self.screen.fill((255, 255, 255))
            self.draw_grid()
            self.draw_cells()
            self.draw_buttons()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.pause_button.collidepoint(event.pos) or \
                       self.save_button.collidepoint(event.pos) or \
                       self.load_button.collidepoint(event.pos):
                        self.handle_button_click(event.pos)
                    else:
                        x, y = event.pos
                        cell_x, cell_y = x // self.cell_width, y // self.cell_height
                        self.game_state[cell_x, cell_y] = not self.game_state[cell_x, cell_y]

            if not self.paused:
                self.next_generation()

            clock.tick(10)

# Run the game
game = GameOfLife()
game.run()

pygame.quit()