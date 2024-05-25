import pygame
import sys
import math
import config

# Initialize Pygame
pygame.init()

# Set up the display
screen = config.screen
pygame.display.set_caption("Animated Pie Chart")

# Define colors
WHITE = (240, 237, 229)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
LIGHT_GRAY = (211, 211, 211)
PINK = (255, 192, 203)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), PINK]

# Pie chart values for two accounts // hard coded values for now
account1_values = [69, 10, 90, 180, 30]
account2_values = [100, 200, 50, 75, 125]

#NAV account values put here @hidayat
acount_balance = [6000, 3654]  #optimized and not optimized

values = account1_values

# Dropdown button state
dropdown_open = False

#calculate total amount // returns total amount (use as total = calculate_total(array))
def calculate_total(array):
    for elements in array:
        total += elements
    return total

# Function to draw the pie chart
def draw_pie_chart(values, screen, colors, center, radius, outline_color, outline_thickness, scroll_offset=0, animation_progress=None):
    inner_circle_radius = int(0.7 * radius)
    total_value = sum(values)
    start_angle = 0

    # Draw outline
    pygame.draw.circle(screen, outline_color, center, radius + outline_thickness, outline_thickness)

    for i, value in enumerate(values):
        angle = (value / total_value) * 360
        end_angle = start_angle + angle

        if animation_progress is not None and animation_progress < end_angle:
            end_angle = animation_progress

        pygame.draw.arc(screen, colors[i], (center[0] - radius, center[1] - radius + scroll_offset, radius * 2, radius * 2),
                        math.radians(start_angle), math.radians(end_angle), radius)

        start_angle = end_angle


    #Draw inner circle outline
    pygame.draw.circle(screen, outline_color, center, inner_circle_radius + outline_thickness, outline_thickness)
    # Draw inner circle to create the donut effect
    pygame.draw.circle(screen, WHITE, (center[0], center[1] + scroll_offset), inner_circle_radius)

def draw_back_button(screen):
    pygame.draw.polygon(screen, GRAY, [(10, 20), (30, 10), (30, 30)])
    pygame.draw.line(screen, GRAY, (50, 20), (30, 20), 5)

def check_back_button_click(pos):
    return 10 <= pos[0] <= 30 and 10 <= pos[1] <= 30

def draw_dropdown(screen, dropdown_rect, dropdown_open, options, scroll_offset):
    # Adjust dropdown position based on scroll offset
    adjusted_rect = dropdown_rect.move(0, scroll_offset)

    # Draw the dropdown button
    pygame.draw.rect(screen, LIGHT_GRAY, adjusted_rect)
    text = pygame.font.SysFont(None, 36).render("Balances", True, BLACK)
    screen.blit(text, text.get_rect(center=adjusted_rect.center))

    # If the dropdown is open, draw the options
    if dropdown_open:
        for i, option in enumerate(options):
            option_rect = pygame.Rect(adjusted_rect.x, adjusted_rect.y + (i + 1) * adjusted_rect.height, adjusted_rect.width, adjusted_rect.height)
            pygame.draw.rect(screen, LIGHT_GRAY, option_rect)
            option_text = pygame.font.SysFont(None, 36).render(option, True, BLACK)
            screen.blit(option_text, option_text.get_rect(center=option_rect.center))

def check_dropdown_click(pos, dropdown_rect, dropdown_open, options, scroll_offset):
    # Adjust dropdown position based on scroll offset
    adjusted_rect = dropdown_rect.move(0, scroll_offset)

    # Check if the main dropdown button was clicked
    if adjusted_rect.collidepoint(pos):
        return "toggle"
    
    # Check if any of the options were clicked
    if dropdown_open:
        for i, option in enumerate(options):
            option_rect = pygame.Rect(adjusted_rect.x, adjusted_rect.y + (i + 1) * adjusted_rect.height, adjusted_rect.width, adjusted_rect.height)
            if option_rect.collidepoint(pos):
                return option

    return None

def draw_boxes(screen, scroll_offset):
    # Define box dimensions
    box_width = 200
    box_height = 100
    spacing = 50

    # Calculate positions
    box1_rect = pygame.Rect(config.SCREEN_WIDTH // 2 - box_width - spacing // 2, config.SCREEN_HEIGHT - box_height - 50 + scroll_offset, box_width, box_height)
    box2_rect = pygame.Rect(config.SCREEN_WIDTH // 2 + spacing // 2, config.SCREEN_HEIGHT - box_height - 50 + scroll_offset, box_width, box_height)

    # Draw boxes
    pygame.draw.rect(screen, LIGHT_GRAY, box1_rect)
    pygame.draw.rect(screen, LIGHT_GRAY, box2_rect)

    # Add labels
    font = pygame.font.SysFont(None, 36)
    label1 = font.render("For You", True, BLACK)
    label2 = font.render("Create", True, BLACK)
    screen.blit(label1, label1.get_rect(center=box1_rect.center))
    screen.blit(label2, label2.get_rect(center=box2_rect.center))

    return box1_rect, box2_rect

def main():
    global values

    center = (config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 3)
    radius = 100
    scroll_offset = 0  # Initial scroll offset
    scroll_speed = 10  # Scroll speed in pixels
    dropdown_rect = pygame.Rect(center[0] - 100, 10, 200, 50)  # Centered at the top middle
    options = ["Account 1", "Account 2"]

    running = True
    animated = True
    selected_index = None
    global dropdown_open
    animation_progress = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Input Handler
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reset animation
                    animated = True
                    animation_progress = 0
                if event.key == pygame.K_UP and selected_index is not None:
                    values[selected_index] += 10
                if event.key == pygame.K_DOWN and selected_index is not None:
                    values[selected_index] -= 10
                if event.key == pygame.K_TAB:
                    selected_index = (selected_index + 1) % len(values) if selected_index is not None else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if check_back_button_click(event.pos):
                    # Back button clicked, go back to main.py
                    import main  # Assuming main.py is your main script
                    main.main()
                    running = False

                action = check_dropdown_click(event.pos, dropdown_rect, dropdown_open, options, scroll_offset)
                if action == "toggle":
                    dropdown_open = not dropdown_open
                elif action == "Account 1":
                    if values != account1_values:
                        values = account1_values
                        animated = True
                        animation_progress = 0
                    dropdown_open = False
                elif action == "Account 2":
                    if values != account2_values:
                        animated = True
                        animation_progress = 0
                        values = account2_values
                    dropdown_open = False

                box1_rect, box2_rect = draw_boxes(screen, scroll_offset)
                if box1_rect.collidepoint(event.pos):
                    import for_you
                    for_you.main()
                    running = False
                elif box2_rect.collidepoint(event.pos):
                    import create
                    create.main()
                    running = False

            if event.type == pygame.MOUSEWHEEL:
                # Calculate the new scroll offset
                new_scroll_offset = scroll_offset + event.y * scroll_speed

                # Ensure the new scroll offset doesn't go above zero
                scroll_offset = min(new_scroll_offset, 0)

        screen.fill(WHITE)

        if animated:
            if animation_progress >= 360:
                animated = False
            else:
                animation_progress += 1.2
            draw_pie_chart(values, screen, COLORS, center, radius, BLACK, 2, scroll_offset, animation_progress)
        else:
            draw_pie_chart(values, screen, COLORS, center, radius, BLACK, 2, scroll_offset)

        # Draw value text 
        for i, value in enumerate(values):
            color = COLORS[i] if i != selected_index else BLACK
            text = pygame.font.SysFont(None, 36).render(str(value), True, color)
            text_rect = text.get_rect(center=(center[0], center[1] + radius + 20 * (i + 1) + scroll_offset))
            screen.blit(text, text_rect)

        # Draw back button
        draw_back_button(screen)

        # Draw dropdown (moves with scroll offset)
        draw_dropdown(screen, dropdown_rect, dropdown_open, options, scroll_offset)

        # Draw "For You" and "Create" boxes
        draw_boxes(screen, scroll_offset)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
