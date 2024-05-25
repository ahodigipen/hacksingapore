import pygame
import sys
import config
import auth
from auth import users
from styles import Styles

# Use the screen initialized in config.py
screen = config.screen

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
button_color = RED

# Define textboxes
textbox1_rect = pygame.Rect(50, config.SCREEN_HEIGHT / 2 - 150, TEXTBOX_WIDTH, TEXTBOX_HEIGHT)
textbox2_rect = pygame.Rect(50, config.SCREEN_HEIGHT / 2 - 75, TEXTBOX_WIDTH - TOGGLE_BUTTON_WIDTH - 10, TEXTBOX_HEIGHT)  # Adjusted width for password textbox
toggle_button_rect = pygame.Rect(50 + TEXTBOX_WIDTH - TOGGLE_BUTTON_WIDTH, config.SCREEN_HEIGHT / 2 - 75, TOGGLE_BUTTON_WIDTH, TOGGLE_BUTTON_HEIGHT)  # Toggle button rect

# Initialize textbox input strings
textbox1_text = ""
textbox2_text = ""
hidden_password = True  # Flag to indicate whether password is hidden



def authenticate(username, password):
    for user in users:
        if user["username"] == username and user["password"] == password:
            auth.authenticated_user = user
            return True
        
    return False

def main():
    global textbox1_text, textbox2_text
    global hidden_password
    global active_textbox

    # Load the eye icon image
    eye_icon = pygame.image.load("img/view.png")    
    hidden_icon = pygame.image.load("img/hide.png")
    # Load the background image
    background_image = pygame.image.load("img/background.jpg")  # Replace "background_image.jpg" with the path to your image
    # Set background image
    screen.blit(background_image, (0, 0))
    # Resize the background image to match the window size
    # background_image = pygame.transform.scale(background_image, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    # Define the toggle button icon position and size
    toggle_icon_rect = toggle_button_rect.inflate(-10, -15)  # Adjusted icon position and size

    # Font for the prompt text
    prompt_font = pygame.font.Font(DEFAULT_FONT, PROMPT_FONT_SIZE)
    
    # Prompt variables
    prompt_text = None
    prompt_rect = None
    prompt_visible = False
    
    # Variable to keep track of active textbox
    active_textbox = None

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if mouse click was inside textbox1
                if textbox1_rect.collidepoint(event.pos):
                    active_textbox = "textbox1"
                # Check if mouse click was inside textbox2
                elif textbox2_rect.collidepoint(event.pos):
                    active_textbox = "textbox2"
                else:
                    active_textbox = None

                if button_rect.collidepoint(event.pos):
                    # Authenticate the user
                    if authenticate(textbox1_text, textbox2_text):
                        # Authentication successful, go to next screen
                        import next_screen
                        next_screen.main()
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

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    if active_textbox == "textbox1":
                        active_textbox = "textbox2"
                    elif active_textbox == "textbox2":
                        active_textbox = None
                    else:
                        active_textbox = "textbox1"

                elif event.key == pygame.K_RETURN:
                        # Authenticate the user
                        if authenticate(textbox1_text, textbox2_text):
                            # Authentication successful, go to next screen
                            import next_screen
                            next_screen.main()
                        else:
                            # Authentication failed, reset textboxes and display prompt
                            
                            textbox1_text = ""
                            textbox2_text = ""
                            prompt_text = prompt_font.render("Username or Password is incorrect! Please try again!", True, RED)
                            prompt_rect = prompt_text.get_rect(center=(config.SCREEN_WIDTH / 2, textbox1_rect.y - 30))  # Position above the username text field
                            prompt_visible = True

                elif event.key == pygame.K_BACKSPACE:
                    if active_textbox == "textbox1":
                        textbox1_text = textbox1_text[:-1]
                    elif active_textbox == "textbox2":
                        textbox2_text = textbox2_text[:-1]

                elif active_textbox:
                    if len(event.unicode) == 1:
                        if active_textbox == "textbox1":
                            textbox1_text += event.unicode
                        elif active_textbox == "textbox2":
                            textbox2_text += event.unicode

        # Draw the button
        pygame.draw.rect(screen, button_color, button_rect, border_radius=BORDER_RADIUS)
        screen.blit(button_text, button_text.get_rect(center=button_rect.center))

       
        # Draw textboxes
        pygame.draw.rect(screen, WHITE, textbox1_rect, border_radius=BORDER_RADIUS)
        pygame.draw.rect(screen, WHITE, textbox2_rect, border_radius=BORDER_RADIUS)
        pygame.draw.rect(screen, WHITE, toggle_button_rect, border_radius=BORDER_RADIUS)

        # Draw border around active textbox
        if active_textbox == "textbox1":
            pygame.draw.rect(screen, BLACK, textbox1_rect, 2)  # Draw a black border around textbox1
        elif active_textbox == "textbox2":
            pygame.draw.rect(screen, BLACK, textbox2_rect, 2)  # Draw a black border around textbox2

        # Draw placeholder text if textboxes are empty
        if not textbox1_text:
            placeholder1_surface = pygame.font.Font(DEFAULT_FONT, PLACEHOLDER_FONT_SIZE).render("USERNAME", True, DARK_GRAY)
            screen.blit(placeholder1_surface, (textbox1_rect.x + TEXTBOX_PADDING, textbox1_rect.y + TEXTBOX_HEIGHT // 2 - PLACEHOLDER_FONT_SIZE // 2))
        if not textbox2_text:
            placeholder2_surface = pygame.font.Font(DEFAULT_FONT, PLACEHOLDER_FONT_SIZE).render("PASSWORD", True, DARK_GRAY)
            screen.blit(placeholder2_surface, (textbox2_rect.x + TEXTBOX_PADDING, textbox2_rect.y + TEXTBOX_HEIGHT // 2 - PLACEHOLDER_FONT_SIZE // 2))

        # Render and blit the input text
        textbox1_surface = pygame.font.Font(DEFAULT_FONT, TEXTBOX_FONT_SIZE).render(textbox1_text, True, DARK_GRAY)
        textbox2_surface = pygame.font.Font(DEFAULT_FONT, TEXTBOX_FONT_SIZE).render("*" * len(textbox2_text) if hidden_password else textbox2_text, True, DARK_GRAY)
        screen.blit(textbox1_surface, (textbox1_rect.x + TEXTBOX_PADDING, textbox1_rect.y + TEXTBOX_HEIGHT // 2 - TEXTBOX_FONT_SIZE // 2))
        screen.blit(textbox2_surface, (textbox2_rect.x + TEXTBOX_PADDING, textbox2_rect.y + TEXTBOX_HEIGHT // 2 - TEXTBOX_FONT_SIZE // 2))

        # Draw toggle button icon
        if hidden_password:
            screen.blit(hidden_icon, toggle_icon_rect)
        else:
            screen.blit(eye_icon, toggle_icon_rect)

        # Render and blit the prompt text if it exists and is visible
        if prompt_text and prompt_visible:
            screen.blit(prompt_text, prompt_rect)

        # Draw text and underline "PIN"
        forgot_pin_text = pygame.font.Font(DEFAULT_FONT, PROMPT_FONT_SIZE).render("Forgot your ", True, WHITE)
        pin_text = pygame.font.Font(DEFAULT_FONT, PROMPT_FONT_SIZE).render("PIN", True, WHITE)
        pin_text_width = forgot_pin_text.get_width() + pin_text.get_width()  # Total width of "Forgot your PIN"
        pin_underline_rect = pygame.Rect(50 + forgot_pin_text.get_width(), textbox2_rect.bottom + 20 + 13, pin_text.get_width(), 2)  # Underline rectangle
        pygame.draw.rect(screen, WHITE, pin_underline_rect)  # Draw underline
        screen.blit(forgot_pin_text, (50, textbox2_rect.bottom + 20))
        screen.blit(pin_text, (50 + forgot_pin_text.get_width(), textbox2_rect.bottom + 20))

        # Update the display
        pygame.display.flip()



    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
