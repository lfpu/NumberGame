from level import Level
import pygame
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.level = 2
        self.update_window_size()
        self.current_level = Level(self.level, self.level, self.screen.get_width(), self.screen.get_height())
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
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    pos = pygame.mouse.get_pos()
                    self.current_level.click_button(pos)
            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                self.current_level.handle_mouse_hover(pos)

    def update(self):
        if self.current_level.find_maixnum() == self.level ** 2:
            if self.current_level.is_complete():
                # Display "Level Upgrade" comment
                font_size = min(self.screen.get_width() // 10, self.screen.get_height() // 10)
                font = pygame.font.Font(None, font_size)
                text = font.render("Level Upgrade!", True, (0, 255, 100))
                text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
                self.screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.wait(2000)  # Wait for 2 seconds

                self.level += 1
                self.update_window_size()
                self.current_level = Level(self.level, self.level, self.screen.get_width(), self.screen.get_height())
                self.current_level.generate_numbers()
            else:
                self.current_level.reset_level()

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.current_level.draw(self.screen)
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()