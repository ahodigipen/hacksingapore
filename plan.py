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
    font = pygame.font.Font(Styles.DEFAULT_FONT, Styles.TITLE_FONT_SIZE)
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
                # Draw text box for each option
                text_box_rect = pygame.Rect(15, y_offset, 400, 100)  # Adjust position and size as needed
                pygame.draw.rect(screen, Styles.LIGHT_GRAY, text_box_rect, border_radius=5)

                # Render text for the option
                option_text = font.render(option, True, Styles.BLACK)
                option_text_rect = option_text.get_rect(center=(text_box_rect.centerx, text_box_rect.centery))
                screen.blit(option_text, option_text_rect)

                # Increment y_offset for the next text box
                y_offset += 150  # Increase this value to add more space between text boxes

        pygame.display.flip()

    pygame.quit()
    sys.exit()
