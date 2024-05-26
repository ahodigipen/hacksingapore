import pygame
import sys
import math
import config
from styles import Styles

# Initialize Pygame
pygame.init()

# Set up the display
screen = config.screen
pygame.display.set_caption("Animated Pie Chart")

# Import styles
WHITE = Styles.WHITE
OFF_WHITE = [245, 243, 242]
DARK_GRAY = Styles.DARK_GRAY
LIGHT_GRAY = Styles.LIGHT_GRAY
BLACK = Styles.BLACK
RED = Styles.RED
BLUE = Styles.BLUE  # New color for clickable text
GREEN = Styles.GREEN
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

DEFAULT_FONT = Styles.DEFAULT_FONT
BUTTON_FONT_SIZE = Styles.BUTTON_FONT_SIZE
TEXTBOX_FONT_SIZE = Styles.TEXTBOX_FONT_SIZE
PLACEHOLDER_FONT_SIZE = Styles.PLACEHOLDER_FONT_SIZE
PROMPT_FONT_SIZE = Styles.PROMPT_FONT_SIZE

BUTTON_WIDTH = Styles.BUTTON_WIDTH
BUTTON_HEIGHT = Styles.BUTTON_HEIGHT
TEXTBOX_WIDTH = Styles.TEXTBOX_WIDTH
TEXTBOX_HEIGHT = Styles.TEXTBOX_HEIGHT
TOGGLE_BUTTON_WIDTH = Styles.TOGGLE_BUTTON_WIDTH
TOGGLE_BUTTON_HEIGHT = Styles.TOGGLE_BUTTON_HEIGHT
BORDER_RADIUS = Styles.BORDER_RADIUS
TEXTBOX_PADDING = Styles.TEXTBOX_PADDING

# Pie chart values for two accounts // hard coded values for now
account1_values = [69, 10, 90, 180]
account2_values = [100, 200, 50, 75]

# NAV account values put here @hidayat
account_balance = [6000, 3654]  # optimized and not optimized

values = account1_values

# Dropdown button state
dropdown_open = False

textbox1_rect = pygame.Rect(config.SCREEN_WIDTH / 2 - 35, config.SCREEN_HEIGHT / 2 - 180, TEXTBOX_WIDTH, TEXTBOX_HEIGHT)

# Calculate total amount // returns total amount (use as total = calculate_total(array))
def calculate_total(array):
    total = 0
    for elements in array:
        total += elements
    return total

# Function to draw the pie chart
def draw_pie_chart(values, screen, colors, center, radius, outline_color, outline_thickness, animation_progress=None):
    inner_circle_radius = int(0.9 * radius)
    total_value = sum(values)
    start_angle = 0

    # Draw outline
    pygame.draw.circle(screen, outline_color, center, radius + outline_thickness, outline_thickness)

    for i, value in enumerate(values):
        angle = (value / total_value) * 360
        end_angle = start_angle + angle

        if animation_progress is not None and animation_progress < end_angle:
            end_angle = animation_progress

        pygame.draw.arc(screen, colors[i], (center[0] - radius, center[1] - radius, radius * 2, radius * 2),
                        math.radians(start_angle), math.radians(end_angle), radius)

        start_angle = end_angle

    # Draw inner circle outline
    pygame.draw.circle(screen, outline_color, center, inner_circle_radius + outline_thickness, outline_thickness)
    # Draw inner circle to create the donut effect
    pygame.draw.circle(screen, WHITE, center, inner_circle_radius)

# Function to draw the balance circle with a donut effect
def draw_balance_circle(screen, center, radius, color, outline_color, outline_thickness, animation_progress=None):
    inner_circle_radius = int(0.9 * radius)
    # Draw outer circle
    pygame.draw.circle(screen, outline_color, center, radius + outline_thickness, outline_thickness)
    
    # If animating, draw only part of the circle
    if animation_progress is not None:
        pygame.draw.arc(screen, color, (center[0] - radius, center[1] - radius, radius * 2, radius * 2),
                        0, math.radians(animation_progress), radius)
    else:
        pygame.draw.circle(screen, color, center, radius)
    
    # Draw inner circle outline
    pygame.draw.circle(screen, outline_color, center, inner_circle_radius + outline_thickness, outline_thickness)
    # Draw inner circle to create the donut effect
    pygame.draw.circle(screen, WHITE, center, inner_circle_radius)

# Function to draw the "Your Plan"
def draw_boxes(screen):
    # Define box dimensions
    box_width = 200
    box_height = 100
    spacing = 50

    # Calculate positions
    box1_rect = pygame.Rect(config.SCREEN_WIDTH - box_width - spacing * 2 , config.SCREEN_HEIGHT - box_height - 100, box_width, box_height)

    # Draw boxes
    pygame.draw.rect(screen, LIGHT_GRAY, box1_rect)

    # Add labels
    font = pygame.font.Font(DEFAULT_FONT, TEXTBOX_FONT_SIZE)
    label1 = font.render("Your Plan", True, BLACK)
    screen.blit(label1, label1.get_rect(center=box1_rect.center))

    return box1_rect 

# Function to draw the warning text
def draw_warning_text(screen):
    font = pygame.font.Font(DEFAULT_FONT, TEXTBOX_FONT_SIZE)
    warning_text1 = font.render("Your money is losing value!", True, BLACK)
    warning_text2 = font.render("Protect your future now", True, BLACK)

    warning_text1_rect = warning_text1.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 100))
    warning_text2_rect = warning_text2.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 150))

    screen.blit(warning_text1, warning_text1_rect)
    screen.blit(warning_text2, warning_text2_rect)

def draw_navigation_bar(screen, tab_rects, tab_texts, active_tab):
    # Define navigation bar properties
    nav_bar_height = 50
    tab_width = config.SCREEN_WIDTH // 2  # Equal width for both tabs
    tab_color_inactive = LIGHT_GRAY
    tab_color_active = WHITE
    font = pygame.font.SysFont(None, 24)
    outline_color = BLACK
    outline_thickness = 2

    # Draw navigation bar background
    pygame.draw.rect(screen, BLACK, (0, 0, config.SCREEN_WIDTH, nav_bar_height))

    # Draw tabs
    for i, rect in enumerate(tab_rects):
        color = tab_color_active if i == active_tab else tab_color_inactive
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, outline_color, rect, outline_thickness)  # Add outline
        text = font.render(tab_texts[i], True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

# Function to draw the red line separator
def draw_red_line_separator(screen):
    line_width = 4
    line_length = int(config.SCREEN_WIDTH * 0.8)  # 80% of the screen width
    line_start_pos = (config.SCREEN_WIDTH // 2 - line_length // 2, config.SCREEN_HEIGHT // 2 + 45)
    line_end_pos = (config.SCREEN_WIDTH // 2 + line_length // 2, config.SCREEN_HEIGHT // 2 + 45)
    pygame.draw.line(screen, RED, line_start_pos, line_end_pos, line_width)

def main():
    global values, show_expenditure

     # Load the background image
    # background_image = pygame.image.load("img/background-1.jpg")  # Replace "background_image.jpg" with the path to your image
    # Set background image
    screen.fill(OFF_WHITE)


    center = (config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 3)
    radius = 100
    dropdown_rect = pygame.Rect(center[0] - 100, 10, 200, 50)  # Centered at the top middle
    options = ["Account 1", "Account 2"]

    running = True
    animated = True
    selected_index = None
    global dropdown_open
    animation_progress = 0
    show_expenditure = False  # Flag to toggle between expenditure and balance
    expenditure_animation_played = True  # Flag to check if the animation has already played
    balance_animation_played = False  # Flag to check if the balance animation has already played

    # Define tab properties
    tab_height = 50
    tab_spacing = 0  # No spacing between tabs

    # Define navigation tabs
    nav_bar_height = 50
    tab_rects = [
        pygame.Rect(0, 0, config.SCREEN_WIDTH // 2, nav_bar_height),
        pygame.Rect(config.SCREEN_WIDTH // 2, 0, config.SCREEN_WIDTH // 2, nav_bar_height)
    ]
    tab_texts = ["Savings", "Expenditure"]
    active_tab = 0

    # Define box dimensions and positions
    box_width = 200
    box_height = 100
    spacing = 50
    box1_rect = pygame.Rect(config.SCREEN_WIDTH // 2 - box_width - spacing // 2, config.SCREEN_HEIGHT - box_height - 100, box_width, box_height)
    box2_rect = pygame.Rect(config.SCREEN_WIDTH // 2 + spacing // 2, config.SCREEN_HEIGHT - box_height - 100, box_width, box_height)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle tab clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(tab_rects):
                    if rect.collidepoint(event.pos):
                        if active_tab != i:
                            active_tab = i
                            show_expenditure = (active_tab == 1)
                            expenditure_animation_played = False  # Reset animation flag when switching tabs
                            balance_animation_played = False  # Reset balance animation flag when switching tabs
                            animation_progress = 0  # Reset animation progress when switching tabs
                            animated = True  # Start animation when switching tabs
                # Handle box clicks
                if box1_rect.collidepoint(event.pos):
                    import for_you
                    for_you.main()

        # Draw navigation bar
        draw_navigation_bar(screen, tab_rects, tab_texts, active_tab)

        if show_expenditure:
            # Draw expenditure section
            if animated and not expenditure_animation_played:
                if animation_progress >= 360:
                    animated = False
                    expenditure_animation_played = True  # Mark the animation as played
                else:
                    animation_progress += 1.2
                draw_pie_chart(values, screen, COLORS, center, radius, BLACK, 2, animation_progress)
            else:
                draw_pie_chart(values, screen, COLORS, center, radius, BLACK, 2)
        else:
            # Draw savings section
            if animated and not balance_animation_played:
                if animation_progress >= 360:
                    animated = False
                    balance_animation_played = True  # Mark the balance animation as played
                else:
                    animation_progress += 1.2
                draw_balance_circle(screen, center, radius, GREEN, BLACK, 2, animation_progress)
            else:
                draw_balance_circle(screen, center, radius, GREEN, BLACK, 2)

        textbox1_surface = pygame.font.Font(DEFAULT_FONT, TEXTBOX_FONT_SIZE).render("Total", True, DARK_GRAY)
        screen.blit(textbox1_surface, (textbox1_rect.x + TEXTBOX_PADDING, textbox1_rect.y + TEXTBOX_HEIGHT // 2 - TEXTBOX_FONT_SIZE // 2))
        draw_warning_text(screen)
        draw_boxes(screen)
        draw_red_line_separator(screen)  # Draw the red line separator

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
