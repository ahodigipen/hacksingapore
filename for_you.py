import pygame
import sys
import config

# Initialize Pygame
pygame.init()

# Set up the display
screen = config.screen
pygame.display.set_caption("For You")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def draw_back_button(screen):
    pygame.draw.polygon(screen, BLACK, [(10, 20), (30, 10), (30, 30)])
    pygame.draw.line(screen, BLACK, (50, 20), (30, 20), 5)

def check_back_button_click(pos):
    return 10 <= pos[0] <= 30 and 10 <= pos[1] <= 30

def main():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if check_back_button_click(event.pos):
                    import next_screen
                    next_screen.main()
                    running = False

        screen.fill(WHITE)
        font = pygame.font.SysFont(None, 48)
        text = font.render("For You Page", True, BLACK)
        screen.blit(text, text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)))

        draw_back_button(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
