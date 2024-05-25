import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 300
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Demo Phone App")

# Define colors
WHITE = (255, 255, 255)
DARK_GRAY = (169, 169, 169)

# Load a font
font = pygame.font.SysFont(None, 36)

# Render the text
text = font.render("Welcome to the Demo Phone App", True, DARK_GRAY)
text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Draw the text
    screen.blit(text, text_rect)

    # Update the display
    pygame.display.flip()

# Clean up
pygame.quit()
sys.exit()
