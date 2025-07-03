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
    # Textos do menu
    BLIT_TEXT_PLAYER1 = (245, 170, 170, 40)
    BLIT_TEXT_PLAYER2 = (245, 230, 230, 40)
    BLIT_TEXT_BOT = (245, 290, 120, 40)
    BLIT_TEXT_TITLE = (200, 100, 0, 0)
    BLIT_TEXT_ITER = (95, 195, 0, 0)

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
        
        # Título do jogo
        font_title = pygame.font.SysFont('arial', 36, bold=True)
        title_text = font_title.render('BLOCK BRICKS', True, (255, 255, 255))
        title_rect = self.rects[self.enum_rects.BLIT_TEXT_TITLE]
        self.screen.blit(title_text, title_rect)
        
        # Botões do menu
        font_button = pygame.font.SysFont('arial', 24, bold=True)
        mouse_pos = pygame.mouse.get_pos()
        
        # Botão Player 1
        button_p1 = self.rects[self.enum_rects.BUTTON_PLAYER1]
        color_p1 = (200, 200, 200) if button_p1.collidepoint(mouse_pos) else (150, 150, 150)
        pygame.draw.rect(self.screen, color_p1, button_p1)
        text_p1 = font_button.render('Player 1', True, (0, 0, 0))
        self.screen.blit(text_p1, (button_p1.x + 10, button_p1.y + 10))
        
        # Botão Player 2
        button_p2 = self.rects[self.enum_rects.BUTTON_PLAYER2]
        color_p2 = (200, 200, 200) if button_p2.collidepoint(mouse_pos) else (150, 150, 150)
        pygame.draw.rect(self.screen, color_p2, button_p2)
        text_p2 = font_button.render('Player 2', True, (0, 0, 0))
        self.screen.blit(text_p2, (button_p2.x + 10, button_p2.y + 10))
        
        # Botão Bot
        button_bot = self.rects[self.enum_rects.BUTTON_BOT]
        color_bot = (200, 200, 200) if button_bot.collidepoint(mouse_pos) else (150, 150, 150)
        pygame.draw.rect(self.screen, color_bot, button_bot)
        text_bot = font_button.render('AI Bot', True, (0, 0, 0))
        self.screen.blit(text_bot, (button_bot.x + 10, button_bot.y + 10))
        
        pygame.display.update()

    def render_pre_runing(self):
        self.clear_bg_screen()
        self.draw_border()
        
        # Texto de instrução
        font_instruction = pygame.font.SysFont('arial', 24, bold=True)
        instruction_text = font_instruction.render('Pressione ENTER para iniciar', True, (255, 255, 255))
        instruction_rect = self.rects[self.enum_rects.BLIT_TEXT_ITER]
        self.screen.blit(instruction_text, instruction_rect)
        
        # Botão Back
        font_button = pygame.font.SysFont('arial', 18, bold=True)
        mouse_pos = pygame.mouse.get_pos()
        button_back = self.rects[self.enum_rects.BUTTON_BACK]
        color_back = (200, 200, 200) if button_back.collidepoint(mouse_pos) else (150, 150, 150)
        pygame.draw.rect(self.screen, color_back, button_back)
        text_back = font_button.render('Back', True, (0, 0, 0))
        self.screen.blit(text_back, (button_back.x + 10, button_back.y + 5))
        
        pygame.display.update()

    def render_game(self):
        self.clear_bg_screen()
        self.draw_border()
        pygame.display.update()
