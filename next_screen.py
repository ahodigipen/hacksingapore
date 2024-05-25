import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 450
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Animated Pie Chart")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

# Pie chart values
values = [30, 60, 90, 180]

# Function to draw the pie chart
def draw_pie_chart(values, screen, colors, center, radius, animated=False):
    total_value = sum(values)
    start_angle = 0
    for i, value in enumerate(values):
        angle = (value / total_value) * 360
        end_angle = start_angle + angle

        if animated:
            current_end_angle = start_angle
            while current_end_angle < end_angle:
                current_end_angle += 2
                pygame.draw.arc(screen, colors[i], (center[0] - radius, center[1] - radius, radius * 2, radius * 2),
                               math.radians(start_angle), math.radians(current_end_angle), radius)
                pygame.display.flip()
                pygame.time.delay(5)
            start_angle = end_angle
        else:
            pygame.draw.arc(screen, colors[i], (center[0] - radius, center[1] - radius, radius * 2, radius * 2),
                           math.radians(start_angle), math.radians(end_angle), radius)
            start_angle = end_angle

def draw_back_button(screen):
    pygame.draw.polygon(screen, GRAY, [(10, 20), (30, 10), (30, 30)])
    pygame.draw.line(screen, GRAY, (50, 20), (30, 20), 5)

def check_back_button_click(pos):
    return 10 <= pos[0] <= 30 and 10 <= pos[1] <= 30

def main():
    center = (screen_width // 2, screen_height // 2)
    radius = 200

    running = True
    animated = True
    selected_index = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reset animation
                    animated = True
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

        screen.fill(WHITE)

        if animated:
            draw_pie_chart(values, screen, COLORS, center, radius, animated)
            animated = False
        else:
            draw_pie_chart(values, screen, COLORS, center, radius)

        # Draw value text
        for i, value in enumerate(values):
            color = COLORS[i] if i != selected_index else BLACK
            text = pygame.font.SysFont(None, 36).render(str(value), True, color)
            text_rect = text.get_rect(center=(center[0], center[1] + radius + 20 * (i + 1)))
            screen.blit(text, text_rect)

        # Draw back button
        draw_back_button(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
