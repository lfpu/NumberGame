import numpy as np
import pygame
import random
import json
from grid import Grid

class Level:
    def __init__(self, level_number, screen_width, screen_height):
        self.level_number = level_number
        self.grid_size = self.calculate_grid_size(level_number)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.buttons = self.create_buttons()
        self.clicked_numbers = []
        self.Completed=False

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

    def generate_numbers(self):
        max_number = self.level_number ** 2
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

    def click_button(self, pos):
        #min_number = min(button['grid'].get_number() for button in self.buttons if button['grid'].is_clicked()==False)
        min_number =max(self.clicked_numbers)+1 if self.clicked_numbers else 1
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
                    for button in self.buttons:
                        if button['grid'].is_clicked() and button['grid'].get_number() == start_number+1:
                            self.clicked_numbers.append(button['grid'].get_number())
                            start_number+=1
                    if self.is_complete(button,start_number) == False:
                        self.reset_level()
                self.clicked_numbers.sort()
                return True
        return False

    def find_maixnum(self):
        if not self.clicked_numbers:
            return None
        return max(self.clicked_numbers)

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
        self.screen = screen  # Store the screen reference for use in reset_level
        for button in self.buttons:
            if button['grid'].is_hover():
                color = (173, 216, 230)  # Light blue color for hover
            else:
                color = (211, 211, 211) if button['grid'].is_clicked() else (255, 255, 255)
                color=color if button['grid'].wrong==False else (255, 0, 0)  # Change color to red if the number is placed incorrectly
            pygame.draw.rect(screen, color, button['rect'])
            pygame.draw.rect(screen, (0, 0, 0), button['rect'], 1)
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
            'buttons': [{'position': button['grid'].get_position(), 'number': button['grid'].get_number(), 'clicked': button['grid'].is_clicked()} for button in self.buttons]
        }
        with open(filename, 'w') as f:
            json.dump(level_data, f)

    def load_level(self, filename):
        with open(filename, 'r') as f:
            level_data = json.load(f)
        self.level_number = level_data['level_number']
        self.clicked_numbers = level_data['clicked_numbers']
        for button_data in level_data['buttons']:
            position = tuple(button_data['position'])
            button = next((button for button in self.buttons if button['grid'].get_position() == position), None)
            if button:
                button['grid'].generate_number(button_data['number'])
                button['grid'].clicked = button_data['clicked']