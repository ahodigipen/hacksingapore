import pygame
import sys
import config
from styles import Styles

# Define investment options for different risk tiers
investment_options = {
    "High Risk": ["Option 1"],
    "Medium Risk": ["Option 2"],
    "Low Risk": ["Option 3"]
}

def show_investment_options():
    # Initialize Pygame
    pygame.init()

    # Set up the display
    screen = config.screen
    pygame.display.set_caption("Investment Options")

    # Display investment options
    font = pygame.font.Font(Styles.DEFAULT_FONT, Styles.BUTTON_FONT_SIZE)
    running = True

    while running:
        screen.fill(Styles.WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Display investment options for each risk tier
        y_offset = 50
        for risk, options in investment_options.items():
            # Draw section header
            section_header = font.render(risk, True, Styles.BLACK)
            section_header_rect = section_header.get_rect(center=(config.SCREEN_WIDTH // 2, y_offset))
            screen.blit(section_header, section_header_rect)
            y_offset += 50

            # Draw options for this risk tier
            for option in options:
                text = font.render(option, True, Styles.BLACK)
                text_rect = text.get_rect(center=(config.SCREEN_WIDTH // 2, y_offset))
                screen.blit(text, text_rect)
                y_offset += 30

            # Add some space between sections
            y_offset += 50

        pygame.display.flip()

    pygame.quit()
    sys.exit()
