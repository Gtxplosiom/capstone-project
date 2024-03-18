import pygame
import speechRecognition

pygame.init()

dots = [".", "..", "..."]

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Main Window")

# Font setup
def Font(style: str, size: int):
    font = pygame.font.SysFont(style, size)
    return font

def Font_Color(R, G, B) -> int:
    font_color = (R, G, B)
    return font_color

def Put_Text(text: str, font: object, text_col: object, x: int, y: int):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def center_window():
    screen_rect = screen.get_rect()
    screen_width = screen_rect.width
    screen_height = screen_rect.height

    window_width = screen_width
    window_height = screen_height

    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    screen_rect.topleft = (x, y)

# Function to draw loading animation
def Loading():
    loading_text = "Loading modules"
    dot_index = 0
    while not speechRecognition.asr_active:  # Repeat until test is True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        center_window()

        screen.fill((52, 78, 91))
        Put_Text("Welcome to Application!", Font("arial", 25), Font_Color(255, 255, 255), 100, 200)
        Put_Text(loading_text + dots[dot_index], Font("arial", 25), Font_Color(255, 255, 255), 100, 250)
        pygame.display.update()

        dot_index = (dot_index + 1) % len(dots)
        pygame.time.delay(500)  # Adjust the delay as needed
    pygame.quit()

Loading()