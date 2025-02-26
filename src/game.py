from level import Level
import pygame
import sys
import os
import tkinter as tk
from tkinter import messagebox

class Game:
    def __init__(self):
        pygame.init()
        self.level = 15
        self.update_window_size()
        self.current_level = Level(self.level, self.screen.get_width(), self.screen.get_height())
        if os.path.exists('saved_level.level'):
            self.current_level.load_level('saved_level.level')
            self.level = self.current_level.level_number
            self.update_window_size()
            self.current_level.__init__(self.level, self.screen.get_width(), self.screen.get_height())
            self.current_level.load_level('saved_level.level')
        else:
            self.current_level.generate_numbers()
        self.clock = pygame.time.Clock()  # Initialize the clock

    def update_window_size(self):
        cell_size = 50
        grid_size = self.level
        width = max(100, grid_size * cell_size + 100)
        height = max(100, grid_size * cell_size + 100)
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Number Connection Game")

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.prompt_save_level()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    pos = pygame.mouse.get_pos()
                    self.current_level.click_button(pos)
            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                self.current_level.handle_mouse_hover(pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F5:
                    self.prompt_rechallenge_level()
                elif event.key == pygame.K_F1:
                    self.prompt_save_level()
                elif event.key == pygame.K_F2:
                    self.PromptNextNumber()
                    

    def update(self):
        if self.current_level.find_maixnum() == self.level ** 2:
            if self.current_level.Completed:
                # Display "Level Upgrade" comment
                font_size = min(self.screen.get_width() // 10, self.screen.get_height() // 10)
                font = pygame.font.Font(None, font_size)
                text = font.render("Level Upgrade!", True, (0, 255, 100))
                text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
                self.screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.wait(1000)  # Wait for 2 seconds

                self.level += 1
                self.update_window_size()
                self.current_level = Level(self.level, self.screen.get_width(), self.screen.get_height())
                self.current_level.generate_numbers(self.screen)
            else:
                self.current_level.reset_level()

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.current_level.draw(self.screen)
        pygame.display.flip()

    def prompt_save_level(self):
        # Use a GUI prompt to ask the user to save the current level
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        root.attributes("-topmost", True)  # Set the root window as topmost
        save = messagebox.askyesno("Save Level", "Do you want to save the current level?")
        if save:
            self.current_level.save_level('saved_level.level')
        root.destroy()

    def prompt_rechallenge_level(self):
        # Use a GUI prompt to ask the user to rechallenge the current level
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        root.attributes("-topmost", True)  # Set the root window as topmost
        rechallenge = messagebox.askyesno("Rechallenge Level", "Do you want to rechallenge the current level?")
        if rechallenge:
            self.update_window_size()
            self.current_level.__init__(self.level, self.screen.get_width(), self.screen.get_height())
            self.current_level.load_level('saved_level.level',True)
            self.current_level.save_level('saved_level.level')
        root.destroy()
    def PromptNextNumber(self):
        self.current_level.PromptNextNumber()
if __name__ == "__main__":
    game = Game()
    game.run()