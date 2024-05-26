import pygame
import sys
import math
import config
from styles import Styles

# Initialize Pygame
pygame.init()

# Set up the display
screen = config.screen
pygame.display.set_caption("Financial Dashboard")

# Define colors
WHITE = (255, 255, 255)
OFF_WHITE = (245, 243, 242)
DARK_RED = (139, 0, 0)
LIGHT_RED = (255, 102, 102)
MEDIUM_RED = (255, 77, 77)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BUTTON_COLOR = (255, 77, 77)
BUTTON_HOVER_COLOR = (255, 102, 102)
PIE_COLORS_EXPENDITURE = [(255, 153, 153), (255, 102, 102), (255, 51, 51), (204, 0, 0)]
GREEN = (0, 255, 0)

# Define font styles
DEFAULT_FONT = Styles.DEFAULT_FONT
TEXTBOX_FONT_SIZE = Styles.TEXTBOX_FONT_SIZE
TEXTBOX_PADDING = Styles.TEXTBOX_PADDING

# Define constants
TEXTBOX_WIDTH = 100
TEXTBOX_HEIGHT = 40
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 60
ICON_BUTTON_WIDTH = 80
ICON_BUTTON_HEIGHT = 80
ICON_BUTTON_PADDING = 20

# Pie chart values for two accounts
account1_values = [69, 10, 90, 180]
account2_values = [100, 200, 50, 75]
account_balance = [6000, 3654]  # Savings

values = account1_values

textbox1_rect = pygame.Rect(config.SCREEN_WIDTH / 2 - 35, config.SCREEN_HEIGHT / 2 - 180, TEXTBOX_WIDTH, TEXTBOX_HEIGHT)
button_rect = pygame.Rect((config.SCREEN_WIDTH - BUTTON_WIDTH) // 2, config.SCREEN_HEIGHT - BUTTON_HEIGHT - 50, BUTTON_WIDTH, BUTTON_HEIGHT)

def calculate_total(array):
    return sum(array)

def draw_pie_chart(values, screen, colors, center, radius, outline_color, outline_thickness, animation_progress=None):
    total_value = sum(values)
    start_angle = 0

    pygame.draw.circle(screen, outline_color, center, radius + outline_thickness, outline_thickness)

    for i, value in enumerate(values):
        angle = (value / total_value) * 360
        end_angle = start_angle + angle

        if animation_progress is not None and animation_progress < end_angle:
            end_angle = animation_progress

        # Draw the pie slice
        pygame.draw.arc(screen, colors[i % len(colors)], (center[0] - radius, center[1] - radius, radius * 2, radius * 2),
                        math.radians(start_angle), math.radians(end_angle), radius)

        # Draw the outline for the pie slice
        if animation_progress is None or animation_progress >= end_angle:
            pygame.draw.arc(screen, outline_color, (center[0] - radius, center[1] - radius, radius * 2, radius * 2),
                            math.radians(start_angle), math.radians(end_angle), outline_thickness)

        start_angle = end_angle

    pygame.draw.circle(screen, WHITE, center, int(0.9 * radius))

def draw_balance_circle(screen, center, radius, color, outline_color, outline_thickness, animation_progress=None):
    inner_circle_radius = int(0.9 * radius)
    pygame.draw.circle(screen, outline_color, center, radius + outline_thickness, outline_thickness)

    if animation_progress is not None:
        pygame.draw.arc(screen, color, (center[0] - radius, center[1] - radius, radius * 2, radius * 2),
                        0, math.radians(animation_progress), radius)
    else:
        pygame.draw.circle(screen, color, center, radius)

    pygame.draw.circle(screen, WHITE, center, inner_circle_radius)

def draw_warning_text(screen):
    font = pygame.font.Font(DEFAULT_FONT, TEXTBOX_FONT_SIZE)
    warning_text1 = font.render("Your money is losing value!", True, DARK_RED)
    warning_text2 = font.render("Protect your future now", True, DARK_RED)

    warning_text1_rect = warning_text1.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 100))
    warning_text2_rect = warning_text2.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 150))

    screen.blit(warning_text1, warning_text1_rect)
    screen.blit(warning_text2, warning_text2_rect)

def draw_navigation_bar(screen, tab_rects, tab_texts, active_tab):
    nav_bar_height = 50
    tab_color_inactive = LIGHT_RED
    tab_color_active = RED
    font = pygame.font.SysFont(None, 24)
    outline_color = DARK_RED
    outline_thickness = 2

    pygame.draw.rect(screen, RED, (0, 0, config.SCREEN_WIDTH, nav_bar_height))

    for i, rect in enumerate(tab_rects):
        color = tab_color_active if i == active_tab else tab_color_inactive
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, outline_color, rect, outline_thickness)
        text = font.render(tab_texts[i], True, WHITE if i == active_tab else BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

def draw_red_line_separator(screen):
    line_width = 4
    line_length = int(config.SCREEN_WIDTH * 0.8)
    line_start_pos = (config.SCREEN_WIDTH // 2 - line_length // 2, config.SCREEN_HEIGHT // 2 + 245)
    line_end_pos = (config.SCREEN_WIDTH // 2 + line_length // 2, config.SCREEN_HEIGHT // 2 + 245)
    pygame.draw.line(screen, DARK_RED, line_start_pos, line_end_pos, line_width)

def draw_plan_button(screen, rect, hover=False):
    color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, DARK_RED, rect, 2)
    font = pygame.font.Font(DEFAULT_FONT, TEXTBOX_FONT_SIZE)
    label = font.render("Your Plan", True, WHITE)
    screen.blit(label, label.get_rect(center=rect.center))

def draw_icon_button(screen, rect, text, hover=False):
    color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, DARK_RED, rect, 2)
    font = pygame.font.Font(DEFAULT_FONT, TEXTBOX_FONT_SIZE)
    label = font.render(text, True, WHITE)
    screen.blit(label, label.get_rect(center=rect.center))

def draw_text(screen, text, font, color, center):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=center)
    screen.blit(text_surface, text_rect)

def main():
    global values, show_expenditure

    center = (config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 3)
    screen.fill(OFF_WHITE)

    radius = 100
    running = True
    animated = True
    animation_progress = 0
    show_expenditure = False
    expenditure_animation_played = True
    balance_animation_played = False

    tab_rects = [
        pygame.Rect(0, 0, config.SCREEN_WIDTH // 2, 50),
        pygame.Rect(config.SCREEN_WIDTH // 2, 0, config.SCREEN_WIDTH // 2, 50)
    ]
    tab_texts = ["Savings", "Expenditure"]
    active_tab = 0

    icon_button_rects = [
        pygame.Rect(center[0] - 2 * ICON_BUTTON_WIDTH - 1.5 * ICON_BUTTON_PADDING, center[1] + radius + 30, ICON_BUTTON_WIDTH, ICON_BUTTON_HEIGHT),
        pygame.Rect(center[0] - 1 * ICON_BUTTON_WIDTH - 0.5 * ICON_BUTTON_PADDING, center[1] + radius + 30, ICON_BUTTON_WIDTH, ICON_BUTTON_HEIGHT),
        pygame.Rect(center[0] + 0 * ICON_BUTTON_WIDTH + 0.5 * ICON_BUTTON_PADDING, center[1] + radius + 30, ICON_BUTTON_WIDTH, ICON_BUTTON_HEIGHT),
        pygame.Rect(center[0] + 1 * ICON_BUTTON_WIDTH + 1.5 * ICON_BUTTON_PADDING, center[1] + radius + 30, ICON_BUTTON_WIDTH, ICON_BUTTON_HEIGHT)
    ]

    while running:
        mouse_pos = pygame.mouse.get_pos()
        hover_plan = button_rect.collidepoint(mouse_pos)
        hover_icons = [rect.collidepoint(mouse_pos) for rect in icon_button_rects]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(tab_rects):
                    if rect.collidepoint(event.pos):
                        if active_tab != i:
                            active_tab = i
                            show_expenditure = (active_tab == 1)
                            expenditure_animation_played = False
                            balance_animation_played = False
                            animation_progress = 0
                            animated = True
                if button_rect.collidepoint(event.pos):
                    import for_you
                    for_you.main()
                for i, rect in enumerate(icon_button_rects):
                    if rect.collidepoint(event.pos):
                        print(f"Icon button {i+1} clicked")

        screen.fill(OFF_WHITE)
        draw_navigation_bar(screen, tab_rects, tab_texts, active_tab)

        if show_expenditure:
             # Draw the "Spendings this month:" text above the pie chart
            draw_text(screen, "Spendings this month:", pygame.font.Font(DEFAULT_FONT, TEXTBOX_FONT_SIZE), DARK_RED, (center[0], center[1] - radius - 20))

            if animated and not expenditure_animation_played:
                if animation_progress >= 360:
                    animated = False
                    expenditure_animation_played = True
                else:
                    animation_progress += 1.2
                draw_pie_chart(values, screen, PIE_COLORS_EXPENDITURE, center, radius, DARK_RED, 2, animation_progress)
            else:
                draw_pie_chart(values, screen, PIE_COLORS_EXPENDITURE, center, radius, DARK_RED, 2)

            total_expenditure = calculate_total(values)
            total_text = pygame.font.Font(DEFAULT_FONT, TEXTBOX_FONT_SIZE).render(f"${total_expenditure}", True, DARK_RED)
            screen.blit(total_text, (textbox1_rect.x + TEXTBOX_PADDING, textbox1_rect.y + TEXTBOX_HEIGHT // 2 + TEXTBOX_FONT_SIZE // 2))
        else:
            if animated and not balance_animation_played:
                if animation_progress >= 360:
                    animated = False
                    balance_animation_played = True
                else:
                    animation_progress += 1.2
                draw_balance_circle(screen, center, radius, GREEN, DARK_RED, 2, animation_progress)
            else:
                draw_balance_circle(screen, center, radius, GREEN, DARK_RED, 2)

            total_balance = calculate_total(account_balance)
            total_text = pygame.font.Font(DEFAULT_FONT, TEXTBOX_FONT_SIZE).render(f"${total_balance}", True, DARK_RED)
            screen.blit(total_text, (textbox1_rect.x + TEXTBOX_PADDING, textbox1_rect.y + TEXTBOX_HEIGHT // 2 + TEXTBOX_FONT_SIZE // 2))

        textbox1_surface = pygame.font.Font(DEFAULT_FONT, TEXTBOX_FONT_SIZE).render("Total:", True, DARK_RED)
        screen.blit(textbox1_surface, (textbox1_rect.x + TEXTBOX_PADDING, textbox1_rect.y + TEXTBOX_HEIGHT // 2 - TEXTBOX_FONT_SIZE // 2))

        draw_warning_text(screen)
        draw_red_line_separator(screen)
        draw_plan_button(screen, button_rect, hover_plan)
        
        icon_texts = ["Icon1", "Icon2", "Icon3", "Icon4"]
        for i, rect in enumerate(icon_button_rects):
            draw_icon_button(screen, rect, icon_texts[i], hover_icons[i])

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
