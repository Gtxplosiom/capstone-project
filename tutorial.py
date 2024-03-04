import pygame
import openThings
import time

## bool variables
main_next = False
activate_tsr = False

def Tutorial():
    pygame.init()

    screen_width = 800
    screen_height = 600

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Main Window")

    ## bool variables
    global main_next
    global activate_tsr

    tutorial_intro = True
    tutorial_mouse = False

    ## font stuff
    def Font(style: str, size: int):
        font = pygame.font.SysFont(style, size)
        return font
    
    def Font_Color(R, G, B) -> int:
        font_color = (R, G, B)
        return font_color

    def Put_Text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    ## loop
    
    ## tutorial_intro
    while tutorial_intro:

        screen.fill((52, 78, 91))

        if not main_next:
            Put_Text("Welcome to the Application!", Font("arial", 50), Font_Color(255, 255, 255), 160, 250)
            Put_Text("I am here to walk you through this app", Font("arial", 25), Font_Color(255, 255, 255), 235, 310)
            Put_Text("Say 'Next' to continue", Font("arial", 25), Font_Color(255, 255, 255), 310, 350)
        elif main_next:
            Put_Text("This app makes use of camera for mouse movements", Font("arial", 25), Font_Color(255, 255, 255), 200, 250)
            Put_Text("Make sure you are in a well lit room", Font("arial", 25), Font_Color(255, 255, 255), 225, 280)
            Put_Text("Also center your face in the camera, for better experience", Font("arial", 25), Font_Color(255, 255, 255), 190, 310)
            Put_Text("Enable mouse by saying 'Open mouse'", Font("arial", 25), Font_Color(255, 255, 255), 225, 340)
        if openThings.activate_mouse == True:
            tutorial_mouse = True
            tutorial_intro = False

        ## event handler (IMPORTANT!)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tutorial_intro = False

        pygame.display.update()

    while tutorial_mouse:

        screen.fill((52, 78, 91))

        Put_Text("Try moving your head around", Font("arial", 25), Font_Color(255, 255, 255), 225, 280)
        Put_Text("Say 'Next' to continue", Font("arial", 25), Font_Color(255, 255, 255), 310, 350)

        ## event handler (IMPORTANT!)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tutorial_mouse = False

        pygame.display.update()

    pygame.quit()