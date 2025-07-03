import pygame
from enum import Enum

class EnumRects(Enum):
    BUTTON_PLAYER1 = (245, 170, 120, 40)
    BUTTON_PLAYER2 = (245, 230, 120, 40)
    BUTTON_BOT = (245, 290, 120, 40)
    BUTTON_BACK = (40, 300, 85, 30)
    BLIT_TEXT_GAME_OVER = (215, 225, 0, 0)
    BLIT_TEXT_LEVEL = (40, 430, 0, 0)
    BLIT_TEXT_POINTS = (40, 480, 0, 0)
    BLIT_TEXT_BEST_POINTS = (40, 530, 0, 0)
    SCREEN_BORDER = (0, 0, 608, 608)

    def __new__(cls, x, y, width, height):
        obj = object.__new__(cls)
        obj._value_ = pygame.Rect(x, y, width, height)
        return obj

    def to_rect(self):
        return pygame.Rect(self.value)

class RectManager:
    def __init__(self, width=608, height=608, bg_color=(0, 0, 0)):
        self.enum_rects = EnumRects
        self.rects = {key: key.to_rect() for key in EnumRects}
        self.screen = pygame.display.set_mode((width, height))
        self.bg_color = bg_color
        self.width = width
        self.height = height

    def clear_bg_screen(self):
        self.screen.fill(self.bg_color)

    def draw_border(self, color=(115, 115, 115), thickness=3):
        border_rect = self.enum_rects.SCREEN_BORDER.value
        pygame.draw.rect(self.screen, color, border_rect, thickness)

    def render_menu(self):
        self.clear_bg_screen()
        self.draw_border()
        # Aqui pode-se adicionar desenho de botões/menu
        pygame.display.update()

    def render_pre_runing(self):
        self.clear_bg_screen()
        self.draw_border()
        # Aqui pode-se adicionar desenho de tela pré-jogo
        pygame.display.update()

    def render_game(self):
        self.clear_bg_screen()
        self.draw_border()
        # Aqui pode-se adicionar desenho dos elementos do jogo
        pygame.display.update()
