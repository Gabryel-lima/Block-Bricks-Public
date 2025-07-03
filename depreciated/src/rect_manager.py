from src.imports import pygame, os
from typing_extensions import Union

from enum import Enum

class Style:
    COLORS = {
        "default": (127, 127, 127),
        "hover": (170, 170, 170),
        "highlight": (255, 255, 255),
    }
    FONT_SIZE = 30
    ANIMATION_INCREMENT = 3

class EnumRects(Enum):
    # REcts initial screen
    BLIT_TEXT_PLAYER1 = (245, 170, 170, 40)
    BLIT_TEXT_PLAYER2 = (245, 230, 230, 40)
    BLIT_TEXT_BOT = (245, 290, 120, 40)
    BUTTON_PLAYER1 = (245, 170, 120, 40)
    BUTTON_PLAYER2 = (245, 230, 120, 40)
    BUTTON_BOT = (245, 290, 120, 40)
    UNDERLINE_BUTTON_PLAYER1 = (245, 210, 0, 5)
    UNDERLINE_BUTTON_PLAYER2 = (245, 270, 0, 5)
    UNDERLINE_BUTTON_BOT = (245, 330, 0, 5)
    BUTTON_CREATOR_LINK = (40, 522, 280, 40)
    UNDERLINE_CREATOR_LINK = (40, 558, 0, 3)

    # Rects da tela pré-jogo
    BUTTON_BACK = (40, 300, 85, 30)
    UNDERLINE_BACK = (40, 340, 0, 3)

    BLIT_TEXT_GAME_OVER = (215, 225, 0, 0)
    BLIT_TEXT_BACK = (40, 300, 0, 0)

    # Rects durante o jogo
    BLIT_TEXT_LEVEL = (40, 430, 0, 0)
    BLIT_TEXT_POINTS = (40, 480, 0, 0)
    BLIT_TEXT_BEST_POINTS = (40, 530, 0, 0)
    
    # Estes são dois rects que vão se usar a mesma posição
    BLIT_TEXT_WIN = BLIT_TEXT_GAME_OVER # Por enquanto vou deixá-lo igual ao outro, que está centralizado

    # Interação para iniciar o jogo
    BLIT_TEXT_ITER = (95, 195, 0, 0) 

    # Rect dinâmico para borda da tela
    SCREEN_BORDER = (0, 0, 0, 0)

    def __new__(cls, x, y, width, height):
        obj = object.__new__(cls)
        obj._value_ = pygame.Rect(x, y, width, height)
        return obj

    def update_rect(self, x, y, width, height):
        self.value.update(x, y, width, height)

    def to_rect(self):
        return pygame.Rect(self.value)
    
class PreRuningGroup:
    def __init__(self, rect_manager, fonts):
        self.rect_manager = rect_manager
        self.fonts = fonts

    def animate(self):
        pos_mouse = pygame.mouse.get_pos()

        # Animação do botão "Back"
        underline_back = self.rect_manager.rects[EnumRects.UNDERLINE_BACK]
        button_back = self.rect_manager.rects[EnumRects.BUTTON_BACK]

        if button_back.collidepoint(pos_mouse):
            underline_back.width = min(underline_back.width + Style.ANIMATION_INCREMENT, button_back.width)
        else:
            underline_back.width = max(underline_back.width - Style.ANIMATION_INCREMENT, 0)

        pygame.draw.rect(self.rect_manager.screen, Style.COLORS["highlight"], underline_back)

    def draw(self):
        font = self.fonts.get_fonts_system(name='arial', size=Style.FONT_SIZE, bold=True)

        # Desenho do botão "Back"
        button_back = self.rect_manager.rects[EnumRects.BUTTON_BACK]
        color = Style.COLORS["hover"] if button_back.collidepoint(pygame.mouse.get_pos()) else Style.COLORS["default"]
        back_text = font.render("Back", False, color)
        self.rect_manager.screen.blit(back_text, button_back)

        # Texto para iniciar o jogo
        text_iter = self.rect_manager.rects[EnumRects.BLIT_TEXT_ITER]
        iter_text = font.render("Pressione ENTER para iniciar", False, Style.COLORS["default"])
        self.rect_manager.screen.blit(iter_text, text_iter.topleft)

        self.animate()

class InitialScreenGroup:
    def __init__(self, rect_manager, fonts):
        self.rect_manager = rect_manager
        self.fonts = fonts

    def animate(self):
        pos_mouse = pygame.mouse.get_pos()
        font = self.fonts.get_fonts_system(name='arial', size=Style.FONT_SIZE, bold=True)

        for underline_enum, text_enum, text in [
            (EnumRects.UNDERLINE_BUTTON_PLAYER1, EnumRects.BUTTON_PLAYER1, "Player 1"),
            (EnumRects.UNDERLINE_BUTTON_PLAYER2, EnumRects.BUTTON_PLAYER2, "Player 2"),
            (EnumRects.UNDERLINE_BUTTON_BOT, EnumRects.BUTTON_BOT, "Bot"),
            (EnumRects.UNDERLINE_CREATOR_LINK, EnumRects.BUTTON_CREATOR_LINK, "Created by: Gabryel-lima"),
        ]:
            underline_rect = self.rect_manager.rects[underline_enum]
            button_rect = self.rect_manager.rects[text_enum]

            # Calcula a largura do texto renderizado
            text_surface = font.render(text, False, Style.COLORS["default"])
            text_width = text_surface.get_width()

            # Ajusta a largura da animação do sublinhado
            if button_rect.collidepoint(pos_mouse):
                underline_rect.width = min(underline_rect.width + Style.ANIMATION_INCREMENT, text_width)
            else:
                underline_rect.width = max(underline_rect.width - Style.ANIMATION_INCREMENT, 0)

            # Desenha o sublinhado
            pygame.draw.rect(self.rect_manager.screen, Style.COLORS["highlight"], underline_rect)

    def draw(self):
        pos_mouse = pygame.mouse.get_pos()
        font = self.fonts.get_fonts_system(name='arial', size=Style.FONT_SIZE, bold=True)

        for rect_enum, text in [
            (EnumRects.BUTTON_PLAYER1, "Player 1"),
            (EnumRects.BUTTON_PLAYER2, "Player 2"),
            (EnumRects.BUTTON_BOT, "Bot"),
            (EnumRects.BUTTON_CREATOR_LINK, "Created by: Gabryel-lima"),
        ]:
            rect = self.rect_manager.rects[rect_enum]
            color = Style.COLORS["hover"] if rect.collidepoint(pos_mouse) else Style.COLORS["default"]
            text_surface = font.render(text, False, color)
            self.rect_manager.screen.blit(text_surface, rect)

        self.animate()

class RectManager:
    def __init__(self, game, fonts):
        self.enum_rects = EnumRects
        self.rects = {key: key.to_rect() for key in EnumRects}
        self.screen = None
        self.groups = {}
        self.game = game
        self.fonts = fonts

        self.set_screen_dimensions(width=608, height=608, bg_color=(0, 0, 0))
        self.groups['initial_screen'] = InitialScreenGroup(self, self.fonts)
        self.groups['pre_runing_screen'] = PreRuningGroup(self, self.fonts)

    def set_screen_dimensions(self, width: int, height: int, bg_color=(0, 0, 0)):
        if width <= 0 or height <= 0:
            raise ValueError("Largura e altura devem ser maiores que 0.")
        self.screen = pygame.display.set_mode((width, height))
        self.enum_rects.SCREEN_BORDER.update_rect(0, 0, width, height)
        self._screen_config = {"width": width, "height": height, "bg_color": bg_color}

    def clear_bg_screen(self):
        if self.screen:
            self.screen.fill(self._screen_config.get("bg_color"))

    def draw_border(self, color=(115, 115, 115), thickness=3):
        """Desenha uma borda ao redor da tela."""
        if self.screen:
            border_rect = self.enum_rects.SCREEN_BORDER.value
            pygame.draw.rect(self.screen, color, border_rect, thickness)

    def _fun_menu(self):
        self.game.ball.menu_animation()
        #self.game.bot.draw_bot()

    def render_init(self):
        self.clear_bg_screen()
        self.draw_border()
        self._fun_menu()
        self.groups['initial_screen'].draw()
        pygame.display.update()

    def render_pre_runing(self):
        self.clear_bg_screen()
        self.draw_border()
        self.groups['pre_runing_screen'].draw()
        pygame.display.update()
