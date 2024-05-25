import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 450
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Demo Phone App")

# Define colors
WHITE = (240, 237, 229)
DARK_GRAY = (169, 169, 169)
LIGHT_GRAY = (211, 211, 211)

# Load a font
font = pygame.font.SysFont(None, 36)

# Render the text
text = font.render("Welcome to the Demo Phone App", True, DARK_GRAY)
text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2 - 50))

# Define the button
button_text = font.render("Go to Next Screen", True, DARK_GRAY)
button_rect = pygame.Rect(50, screen_height / 2 + 50, 350, 50)  # Adjusted button width to fit text
button_color = LIGHT_GRAY

def main():
    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    # Button clicked, run the next screen code
                    import next_screen
                    next_screen.main()
                    running = False

        # Clear the screen
        screen.fill(WHITE)

        # Draw the text
        screen.blit(text, text_rect)

        # Draw the button
        pygame.draw.rect(screen, button_color, button_rect)
        screen.blit(button_text, button_text.get_rect(center=button_rect.center))

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
