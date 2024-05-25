import pygame
import sys
import config
import auth
import selector
from styles import Styles

# Import styles
WHITE = Styles.WHITE
DARK_GRAY = Styles.DARK_GRAY
LIGHT_GRAY = Styles.LIGHT_GRAY
BLACK = Styles.BLACK
RED = Styles.RED
BLUE = Styles.BLUE  # New color for clickable text

DEFAULT_FONT = Styles.DEFAULT_FONT
BUTTON_FONT_SIZE = Styles.BUTTON_FONT_SIZE
TEXTBOX_FONT_SIZE = Styles.TEXTBOX_FONT_SIZE
PLACEHOLDER_FONT_SIZE = Styles.PLACEHOLDER_FONT_SIZE
TITLE_FONT_SIZE = Styles.TITLE_FONT_SIZE
PROMPT_FONT_SIZE = Styles.PROMPT_FONT_SIZE

BUTTON_WIDTH = Styles.BUTTON_WIDTH
BUTTON_HEIGHT = Styles.BUTTON_HEIGHT
TEXTBOX_WIDTH = Styles.TEXTBOX_WIDTH
TEXTBOX_WIDTH_LARGE = Styles.TEXTBOX_WIDTH_LARGE
TEXTBOX_HEIGHT = Styles.TEXTBOX_HEIGHT
TEXTBOX_HEIGHT_LARGE = Styles.TEXTBOX_HEIGHT_LARGE
TOGGLE_BUTTON_WIDTH = Styles.TOGGLE_BUTTON_WIDTH
TOGGLE_BUTTON_HEIGHT = Styles.TOGGLE_BUTTON_HEIGHT
BORDER_RADIUS = Styles.BORDER_RADIUS
TEXTBOX_PADDING = Styles.TEXTBOX_PADDING

# Initialize Pygame
pygame.init()

# Set up the display
screen = config.screen
pygame.display.set_caption("For You")

# Box configurations
box_width = 300
box_height = 100
box_margin = 20

# Define box positions
box1_rect = pygame.Rect(
    (config.SCREEN_WIDTH - box_width) // 2,
    config.SCREEN_HEIGHT // 2 - 150,
    box_width,
    box_height
)
box2_rect = pygame.Rect(
    (config.SCREEN_WIDTH - box_width) // 2,
    config.SCREEN_HEIGHT // 2 - 150 + box_height + box_margin,
    box_width,
    box_height
)
box3_rect = pygame.Rect(
    (config.SCREEN_WIDTH - box_width) // 2,
    config.SCREEN_HEIGHT // 2 - 150 + 2 * (box_height + box_margin),
    box_width,
    box_height
)

def draw_back_button(screen):
    pygame.draw.polygon(screen, BLACK, [(10, 20), (30, 10), (30, 30)])
    pygame.draw.line(screen, BLACK, (50, 20), (30, 20), 5)

def check_back_button_click(pos):
    return 10 <= pos[0] <= 30 and 10 <= pos[1] <= 30

def check_box_click(pos, box_rect):
    return box_rect.collidepoint(pos)

def main():
    # Load the background image
    background_image = pygame.image.load("img/For-You-background.jpg")  # Replace with your image path
    background_image = pygame.transform.scale(background_image, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    
    running = True
    font = pygame.font.Font(DEFAULT_FONT, BUTTON_FONT_SIZE)

    while running:
        screen.blit(background_image, (0, 0))
        draw_back_button(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if check_back_button_click(event.pos):
                    import next_screen
                    next_screen.main()
                    running = False
                if check_box_click(event.pos, box1_rect):
                    print("Save More for Emergencies clicked")
                    selector.main("Save More for Emergencies")
                    running = False
                elif check_box_click(event.pos, box2_rect):
                    print("Invest to Grow My Wealth clicked")
                    selector.main("Invest to Grow My Wealth")
                    running = False
                elif check_box_click(event.pos, box3_rect):
                    print("Plan My Retirement clicked")
                    selector.main("Plan My Retirement")
                    running = False

        # Draw the boxes and text
        pygame.draw.rect(screen, LIGHT_GRAY, box1_rect, border_radius=BORDER_RADIUS)
        pygame.draw.rect(screen, LIGHT_GRAY, box2_rect, border_radius=BORDER_RADIUS)
        pygame.draw.rect(screen, LIGHT_GRAY, box3_rect, border_radius=BORDER_RADIUS)
        
        text1 = font.render("Save More for Emergencies", True, BLACK)
        text2 = font.render("Invest to Grow My Wealth", True, BLACK)
        text3 = font.render("Plan My Retirement", True, BLACK)
        
        screen.blit(text1, text1.get_rect(center=box1_rect.center))
        screen.blit(text2, text2.get_rect(center=box2_rect.center))
        screen.blit(text3, text3.get_rect(center=box3_rect.center))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
