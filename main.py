import pygame
import sys
import config
from styles import Styles

# Use the screen initialized in config.py
screen = config.screen

# Import styles
WHITE = Styles.WHITE
DARK_GRAY = Styles.DARK_GRAY
LIGHT_GRAY = Styles.LIGHT_GRAY
BLACK = Styles.BLACK
RED = Styles.RED

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

# Define the button
button_text = pygame.font.Font(DEFAULT_FONT, BUTTON_FONT_SIZE).render("LOGIN", True, WHITE)
button_rect = pygame.Rect(50, config.SCREEN_HEIGHT / 2 + 50, BUTTON_WIDTH, BUTTON_HEIGHT)
button_color = DARK_GRAY

# Define textboxes
textbox1_rect = pygame.Rect(50, config.SCREEN_HEIGHT / 2 - 150, TEXTBOX_WIDTH, TEXTBOX_HEIGHT)
textbox2_rect = pygame.Rect(50, config.SCREEN_HEIGHT / 2 - 75, TEXTBOX_WIDTH - TOGGLE_BUTTON_WIDTH - 10, TEXTBOX_HEIGHT)  # Adjusted width for password textbox
toggle_button_rect = pygame.Rect(50 + TEXTBOX_WIDTH - TOGGLE_BUTTON_WIDTH, config.SCREEN_HEIGHT / 2 - 75, TOGGLE_BUTTON_WIDTH, TOGGLE_BUTTON_HEIGHT)  # Toggle button rect

# Initialize textbox input strings
textbox1_text = ""
textbox2_text = ""
hidden_password = True  # Flag to indicate whether password is hidden

# User data
users = [
    {"username": "user1", "password": "password1", "full_name" : "Tan Jun Wei", "pass_type" : "citizen", "age": "65", "occupation": "unemployed"},
    {"username": "user2", "password": "password2", "full_name" : "Raj", "pass_type" : "employment", "age": "33", "occupation": "software developer"},
    {"username": "user3", "password": "password3", "full_name" : "Deen", "pass_type" : "work", "age": "35", "occupation": "construction worker"}
]

def authenticate(username, password):
    for user in users:
        if user["username"] == username and user["password"] == password:
            return True
    return False

def main():
    global textbox1_text, textbox2_text
    global hidden_password

    # Font for the prompt text
    prompt_font = pygame.font.Font(DEFAULT_FONT, PROMPT_FONT_SIZE)
    
    # Prompt variables
    prompt_text = None
    prompt_rect = None
    prompt_visible = False

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    # Authenticate the user
                    if authenticate(textbox1_text, textbox2_text):
                        # Authentication successful, go to next screen
                        import next_screen
                        next_screen.main()
                        running = False
                    else:
                        # Authentication failed, reset textboxes and display prompt
                        textbox1_text = ""
                        textbox2_text = ""
                        prompt_text = prompt_font.render("Username or Password is incorrect! Please try again!", True, RED)
                        prompt_rect = prompt_text.get_rect(center=(config.SCREEN_WIDTH / 2, textbox1_rect.y - 30))  # Position above the username text field
                        prompt_visible = True

                elif toggle_button_rect.collidepoint(event.pos):
                    # Toggle password visibility
                    hidden_password = not hidden_password

            if event.type == pygame.KEYDOWN:
                if textbox1_rect.collidepoint(pygame.mouse.get_pos()):
                    if event.key == pygame.K_BACKSPACE:
                        textbox1_text = textbox1_text[:-1]
                    else:
                        textbox1_text += event.unicode
                elif textbox2_rect.collidepoint(pygame.mouse.get_pos()):
                    if event.key == pygame.K_BACKSPACE:
                        textbox2_text = textbox2_text[:-1]
                    else:
                        textbox2_text += event.unicode

        # Clear the screen
        screen.fill(WHITE)

        # Draw the button
        pygame.draw.rect(screen, button_color, button_rect, border_radius=BORDER_RADIUS)
        screen.blit(button_text, button_text.get_rect(center=button_rect.center))

        # Draw textboxes
        pygame.draw.rect(screen, LIGHT_GRAY, textbox1_rect, border_radius=BORDER_RADIUS)
        pygame.draw.rect(screen, LIGHT_GRAY, textbox2_rect, border_radius=BORDER_RADIUS)
        pygame.draw.rect(screen, LIGHT_GRAY, toggle_button_rect, border_radius=BORDER_RADIUS)

        # Draw placeholder text if textboxes are empty
        if not textbox1_text:
            placeholder1_surface = pygame.font.Font(DEFAULT_FONT, PLACEHOLDER_FONT_SIZE).render("Username", True, BLACK)
            screen.blit(placeholder1_surface, (textbox1_rect.x + TEXTBOX_PADDING, textbox1_rect.y + TEXTBOX_HEIGHT // 2 - PLACEHOLDER_FONT_SIZE // 2))
        if not textbox2_text:
            placeholder2_surface = pygame.font.Font(DEFAULT_FONT, PLACEHOLDER_FONT_SIZE).render("Password", True, BLACK)
            screen.blit(placeholder2_surface, (textbox2_rect.x + TEXTBOX_PADDING, textbox2_rect.y + TEXTBOX_HEIGHT // 2 - PLACEHOLDER_FONT_SIZE // 2))

        # Render and blit the input text
        textbox1_surface = pygame.font.Font(DEFAULT_FONT, TEXTBOX_FONT_SIZE).render(textbox1_text, True, BLACK)
        textbox2_surface = pygame.font.Font(DEFAULT_FONT, TEXTBOX_FONT_SIZE).render("*" * len(textbox2_text) if hidden_password else textbox2_text, True, BLACK)
        screen.blit(textbox1_surface, (textbox1_rect.x + TEXTBOX_PADDING, textbox1_rect.y + TEXTBOX_HEIGHT // 2 - TEXTBOX_FONT_SIZE // 2))
        screen.blit(textbox2_surface, (textbox2_rect.x + TEXTBOX_PADDING, textbox2_rect.y + TEXTBOX_HEIGHT // 2 - TEXTBOX_FONT_SIZE // 2))

        # Draw toggle button text
        toggle_text = "Show" if hidden_password else "Hide"
        toggle_button_text_surface = pygame.font.Font(DEFAULT_FONT, TEXTBOX_FONT_SIZE).render(toggle_text, True, BLACK)
        toggle_button_text_rect = toggle_button_text_surface.get_rect(center=toggle_button_rect.center)
        screen.blit(toggle_button_text_surface, toggle_button_text_rect)

        # Render and blit the prompt text if it exists and is visible
        if prompt_visible:
            screen.blit(prompt_text, prompt_rect)

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
