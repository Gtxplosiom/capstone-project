import pygame
import time
import sys

class Tutorial:

    game_state = 0

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Main Window")

        self.screen_width = 800
        self.screen_height = 600

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.running = True

    def set_font_style(self, style: str, size: int):
        self.font = pygame.font.SysFont(style, size)
        return self.font

    def set_font_color(self, R, G, B) -> int:
        self.font_color = (R, G, B)
        return self.font_color

    def put_text(self, text: str, font: object, text_col: object, x: int, y: int):
        self.img = font.render(text, True, text_col)
        self.screen.blit(self.img, (x, y))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        if self.game_state == 0:
            self.part_1()
        elif self.game_state == 1:
            self.part_2()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()

        # Quit Pygame when the game loop ends
        pygame.quit()

    ## game states
    def part_1(self):
        self.screen.fill((255, 255, 255))
        self.put_text("Welcome to the Tutorial! I am here to walk you through this app.", self.set_font_style("arial", 25), self.set_font_color(0, 0, 0), 200, 200)
        self.put_text("Say 'Next' to proceed.", self.set_font_style("arial", 20), self.set_font_color(0, 0, 0), 200, 225)
        pygame.display.update()

    def part_2(self):
        self.screen.fill((255, 255, 255))
        self.put_text("This app makes use of camera for mouse movements.", self.set_font_style("arial", 20), self.set_font_color(0, 0, 0), 200, 200)
        self.put_text("First let us open camera first to enable mouse control.", self.set_font_style("arial", 20), self.set_font_color(0, 0, 0), 200, 225)
        self.put_text("Make sure you are in a well lit room. and center you face in the camera.", self.set_font_style("arial", 20), self.set_font_color(0, 0, 0), 200, 250)
        self.put_text("Enable it by saying 'Open mouse'.", self.set_font_style("arial", 20), self.set_font_color(0, 0, 0), 200, 225)
        pygame.display.update()

if __name__ == "__main__":
    # Create an instance of the PygameExample class and run the game loop
    game = Tutorial()
    game.run()