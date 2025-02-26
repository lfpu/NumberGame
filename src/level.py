import numpy as np
import pygame
import random
import json
import base64  # Import base64 module
import tkinter as tk
from grid import Grid
from threading import Thread
from tkinter import messagebox
import MatrixGenerator as matrix

class Level:
    def __init__(self, level_number, screen_width, screen_height):
        self.level_number = level_number
        self.grid_size = self.calculate_grid_size(level_number)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.buttons = self.create_buttons()
        self.clicked_numbers = []
        self.Completed=False
        self.screen=None
        self.IsGenerated=False

    def calculate_grid_size(self, level_number):
        #return int(level_number ** 0.5) + (level_number % 2)
        return level_number 

    def create_buttons(self):
        buttons = []
        cell_size = 50
        grid_width = self.grid_size * cell_size
        grid_height = self.grid_size * cell_size
        offset_x = (self.screen_width - grid_width) // 2
        offset_y = (self.screen_height - grid_height) // 2

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                rect = pygame.Rect(offset_x + col * cell_size, offset_y + row * cell_size, cell_size, cell_size)
                buttons.append({'rect': rect, 'grid': Grid((row, col))})
        return buttons

    def generate_numbers(self,screen=None):
        if(screen!=None):
            self.screen=screen
        t= Thread(target=self.generate_numbersAsync)
        t.start()
        #t.join()
    def old_generate_numbers(self):
        
        numbers = list(range(1, max_number + 1))
        # Ensure numbers are placed in a sequence that guarantees they are adjacent to each other
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        done = False
        while not done:
            start_pos = (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1))
            start_button = next(button for button in self.buttons if button['grid'].get_position() == start_pos)
            start_button['grid'].generate_number(1)
            current_pos = start_pos
            for number in numbers[1:]:
                np.random.shuffle(directions)
                placed = False
                for direction in directions:
                    next_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1])
                    if 0 <= next_pos[0] < self.grid_size and 0 <= next_pos[1] < self.grid_size:
                        button = next(button for button in self.buttons if button['grid'].get_position() == next_pos)
                        if button['grid'].get_number() == 0:
                            button['grid'].generate_number(number)
                            current_pos = next_pos
                            placed = True
                            break
                if not placed:
                    break
            if all(button['grid'].get_number() > 0 for button in self.buttons):
                done = True
            else:
                for button in self.buttons:
                    button['grid'].reset()
    def generate_numbersAsync(self):
        self.IsGenerated=False
        max_number = self.level_number ** 2
        matrixs=matrix.generate_matrix(self.level_number)
        elements_with_coords = [(x, y, matrixs[y][x]) for y in range(len(matrixs)) for x in range(len(matrixs[y]))]
        for x, y, value in elements_with_coords:
            button = next(button for button in self.buttons if button['grid'].get_position() == (y,x))
            button['grid'].generate_number(value)

        # Randomly select n numbers to display, where n is equal to the current level
        display_numbers = random.sample(range(1, max_number + 1), self.level_number)
        for button in self.buttons:
            if button['grid'].get_number() not in display_numbers:
                #button['grid'].generate_number(0)
                button['grid'].clicked = False
            else:
                button['grid'].clicked = True
        min_number = min(button['grid'].get_number() for button in self.buttons if button['grid'].is_clicked()==False)
        self.clicked_numbers = list(range(1, min_number))
        self.save_level("saved_level.level")
        self.IsGenerated=True
    def click_button(self, pos):
        if(self.IsGenerated==False):
            return
        #min_number = min(button['grid'].get_number() for button in self.buttons if button['grid'].is_clicked()==False)
        min_number =(max(self.clicked_numbers))+1 if self.clicked_numbers else 1
        start_number = min_number
        level_square = self.level_number ** 2
        for button in self.buttons:
            if button['rect'].collidepoint(pos):
                if button['grid'].is_clicked():
                    return False
                number = button['grid'].click(start_number, level_square)
                if number is not None:
                    if number not in self.clicked_numbers: self.clicked_numbers.append(number)
                    button['grid'].number= number
                    button['grid'].clicked = True
                    button['grid'].IsUserInput = True
                    self.CheckNext(number)
                    if self.is_complete(button,start_number) == False:
                        self.reset_level()
                self.clicked_numbers.sort()
                return True
        return False
    def CheckNext(self,number):
        for button in self.buttons:
            if button['grid'].is_clicked() and button['grid'].get_number() == (number+1):
                self.clicked_numbers.append(button['grid'].get_number())
                number+=1
                self.CheckNext(number)
                break

    def find_maixnum(self):
        if not self.clicked_numbers:
            return None
        return max(self.clicked_numbers)
    def PromptNextNumber(self):
        if(self.IsGenerated==False):
            return
        next_number = 1 if not self.clicked_numbers else max(self.clicked_numbers)+1
        if next_number > self.level_number ** 2:
            return
        for button in self.buttons:
            if button['grid'].get_number() == next_number:
                button['grid'].clicked = True
                button['grid'].IsUserInput = True
                self.clicked_numbers.append(next_number)
                break
        
    def is_complete(self,btn,start):
        # if  btn['grid'].get_number() != start:
        #     return False
        # Check if all consecutive numbers are adjacent
        for i in range(1, len(self.clicked_numbers)):
            current_number = self.clicked_numbers[i - 1]
            next_number = self.clicked_numbers[i]
            current_position = next(button['grid'].get_position() for button in self.buttons if button['grid'].get_number() == current_number and button['grid'].is_clicked())
            next_position = next(button['grid'].get_position() for button in self.buttons if button['grid'].get_number() == next_number  and button['grid'].is_clicked())
            if not ((abs(current_position[0] - next_position[0]) == 1 and current_position[1] == next_position[1]) or
                    (abs(current_position[1] - next_position[1]) == 1 and current_position[0] == next_position[0])):
                return False
        self.Completed=True
        return True

    def reset_level(self):
        # Display "Game Over" comment
        font_size = min(self.screen.get_width() // 10, self.screen.get_height() // 10)
        font = pygame.font.Font(None, font_size)
        text = font.render("Game Over...", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)  # Wait for 2 seconds
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        root.attributes("-topmost", True)  # Set the root window as topmost
        save = messagebox.askyesno("Refresh", "Do you want challenge again?", icon='question')
        if save:
            self.load_level('saved_level.level')
            return
        root.destroy()

        self.clicked_numbers = list(range(1, self.level_number + 1))
        for button in self.buttons:
            button['grid'].reset()
        self.generate_numbers()

    def handle_mouse_hover(self, pos):
        for button in self.buttons:
            if(button['grid'].is_clicked()):
                continue
            if button['rect'].collidepoint(pos):
                button['grid'].set_hover(True)
            else:
                button['grid'].set_hover(False)

    def draw(self, screen):
        if self.IsGenerated==False:
            font = pygame.font.Font(None, 36)
            text = font.render("Generating...", True, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            screen.blit(text, text_rect)
            return
        self.screen = screen  # Store the screen reference for use in reset_level
        for button in self.buttons:
            if button['grid'].is_hover():
                color = (173, 216, 230)  # Light blue color for hover
            else:
                color = (211, 211, 211) if button['grid'].is_clicked() else (255, 255, 255)
                color=color if button['grid'].wrong==False else (255, 0, 0)  # Change color to red if the number is placed incorrectly
            pygame.draw.rect(screen, color, button['rect'])
            bordercolor=(59, 127, 78) if button['grid'].IsUserInput else (0, 0, 0)
            pygame.draw.rect(screen, bordercolor, button['rect'], 1)
            number = button['grid'].get_number()
            if button['grid'].is_clicked() and number > 0:
                font = pygame.font.Font(None, 36)
                text = font.render(str(number), True, (0, 0, 0))
                text_rect = text.get_rect(center=button['rect'].center)
                screen.blit(text, text_rect)

    def save_level(self, filename):
        level_data = {
            'level_number': self.level_number,
            'clicked_numbers': self.clicked_numbers,
            'buttons': [{'position': button['grid'].get_position(), 'number': button['grid'].get_number(), 'clicked': button['grid'].is_clicked(),"IsUserInput":button['grid'].IsUserInput,"OrignalNumber":button['grid'].OrignalNumber} for button in self.buttons]
        }
        json_data = json.dumps(level_data)
        base64_data = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')
        with open(filename, 'w') as f:
            f.write(base64_data)

    def load_level(self, filename,refresh=False):
        with open(filename, 'r') as f:
            base64_data = f.read()
        json_data = base64.b64decode(base64_data.encode('utf-8')).decode('utf-8')
        level_data = json.loads(json_data)
        self.level_number = level_data['level_number']
        self.clicked_numbers = level_data['clicked_numbers']
        for button_data in level_data['buttons']:
            position = tuple(button_data['position'])
            button = next((button for button in self.buttons if button['grid'].get_position() == position), None)
            if button:
                button['grid'].generate_number(button_data['number'])
                button['grid'].clicked = button_data['clicked']
                try:
                    if button_data['IsUserInput']==True and refresh:
                        button['grid'].clicked = False
                        button['grid'].IsUserInput=False
                        button['grid'].number=button_data['OrignalNumber']
                        button['grid'].OrignalNumber=button_data['OrignalNumber']
                except:
                    pass
        min_number = min(button['grid'].get_number() for button in self.buttons if button['grid'].is_clicked()==False)
        self.clicked_numbers = list(range(1,min_number))
        self.IsGenerated=True