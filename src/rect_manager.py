import pygame.draw_py
from .imports import pygame

from .imports import pygame, os
from typing_extensions import Union

from enum import Enum

class EnumRects(Enum):
    BLIT_TEXT_PLAYER1 = (245, 170, 170, 40)
    BLIT_TEXT_PLAYER2 = (245, 230, 230, 40)
    BLIT_TEXT_BOT = (245, 290, 120, 40)

    BUTTON_PLAYER1 = (240, 170, 120, 40)
    BUTTON_PLAYER2 = (240, 230, 120, 40)
    BUTTON_BOT = (240, 290, 120, 40)

    UNDERLINE_BUTTON_PLAYER1 = (245, 210, 0, 5)
    UNDERLINE_BUTTON_PLAYER2 = (245, 270, 0, 5)
    UNDERLINE_BUTTON_BOT = (245, 330, 0, 5)

    BLIT_TEXT_CREATOR = (40, 520, 0, 40)
    BUTTON_CREATOR_LINK = (40, 522, 280, 40)
    UNDERLINE_CREATOR_LINK = (40, 558, 0, 3)

    # Rects da tela pré-jogo
    BUTTON_BACK = (40, 300, 85, 30)
    UNDERLINE_BACK = (40, 340, 0, 3)

    BLIT_TEXT_GAME_OVER = (215, 225, 0, 0)
    BLIT_TEXT_BACK = (40, 300, 0, 0)
    BLIT_TEXT_POINTS_PLAYER1 = (40, 430, 0, 0)
    BLIT_TEXT_BEST_POINTS_PLAYER1 = (40, 530, 0, 0)
    BLIT_TEXT_LEVEL = (40, 480, 0, 0)
    BLIT_TEXT_POINTS_PLAYER2 = (40, 430, 0, 0)
    BLIT_TEXT_BEST_POINTS_PLAYER2 = (40, 530, 0, 0)

    # Rects da tela de configurações
    BLIT_RESOLUTION_OPTION1 = (0, 0, 0, 0)
    BLIT_RESOLUTION_OPTION2 = (240, 230, 120, 40)
    BLIT_RESOLUTION_OPTION3 = (240, 290, 120, 40)

    BLIT_IMAGE_CONFIG_ICON = (475, 495, 0, 0)
    BUTTON_CONFIG = (474, 494, 53, 53)

    BLIT_TEXT_RESOLUTION_OPTION1 = (245, 170, 0, 0)
    BLIT_TEXT_RESOLUTION_OPTION2 = (245, 230, 0, 0)
    BLIT_TEXT_RESOLUTION_OPTION3 = (232, 290, 0, 0)

    # Rect dinâmico para borda da tela
    SCREEN_BORDER = (0, 0, 0, 0)

    def __new__(cls, x, y, width, height):
        """Cria e retorna um objeto pygame.Rect como valor da constante."""
        obj = object.__new__(cls)
        obj._value_ = pygame.Rect(x, y, width, height)
        return obj
    
    def update_rect(self, x, y, width, height):
        """Atualiza dinamicamente o rect da enumeração."""
        self.value.update(x, y, width, height)

    def to_rect(self):
        """Converte o valor da enumeração em um objeto pygame.Rect."""
        return pygame.Rect(*self.value)

class RectManager:
    def __init__(self):
        self.enum_rects = EnumRects
        self.rects: dict[EnumRects, pygame.Rect] = {key: key.to_rect() for key in EnumRects}
        self.groups: dict[str, list[EnumRects]] = {}
        self.screen = None

        # Inicializa a tela e configurações iniciais
        self.set_screen_dimensions(width=608, height=608, bg_color=(0, 0, 0))
        self.setup_initial_screen()
        self.setup_additional_groups()

    def set_screen_dimensions(self, width: int, height: int, bg_color=(0, 0, 0)):
        """Configura as dimensões e cor de fundo da tela."""
        if width <= 0 or height <= 0:
            raise ValueError("Largura e altura devem ser maiores que 0.")
        
        self.screen = pygame.display.set_mode((width, height))
        self.enum_rects.SCREEN_BORDER.update_rect(0, 0, width, height)
        
        # Atualiza as configurações da tela
        self._screen_config = {
            "width": width,
            "height": height,
            "bg_color": bg_color,
        }

    def clear_bg_screen(self):
        """Limpa a tela com a cor de fundo."""
        if self.screen:
            self.screen.fill(self._screen_config.get("bg_color"))

    def setup_initial_screen(self):
        """Agrupa os rects para a tela inicial."""
        self.groups['initial_screen'] = [
            self.enum_rects.BLIT_TEXT_PLAYER1.value,
            self.enum_rects.BLIT_TEXT_PLAYER2.value,
            self.enum_rects.BUTTON_PLAYER1.value,
            self.enum_rects.BUTTON_PLAYER2.value,
            self.enum_rects.BUTTON_BOT.value,
            self.enum_rects.UNDERLINE_BUTTON_PLAYER1.value,
            self.enum_rects.UNDERLINE_BUTTON_PLAYER2.value,
            self.enum_rects.UNDERLINE_BUTTON_BOT.value,
        ]

    def setup_additional_groups(self):
        """Configura grupos adicionais de rects."""
        self.groups['pre_game_screen'] = [
            self.enum_rects.BUTTON_BACK.value,
            self.enum_rects.UNDERLINE_BACK.value,
        ]

        self.groups['game_over_screen'] = [
            self.enum_rects.BLIT_TEXT_GAME_OVER.value,
            self.enum_rects.BLIT_TEXT_BACK.value,
            self.enum_rects.BLIT_TEXT_POINTS_PLAYER1.value,
            self.enum_rects.BLIT_TEXT_BEST_POINTS_PLAYER1.value,
            self.enum_rects.BLIT_TEXT_LEVEL.value,
            self.enum_rects.BLIT_TEXT_POINTS_PLAYER2.value,
            self.enum_rects.BLIT_TEXT_BEST_POINTS_PLAYER2.value,
        ]

        self.groups['settings_screen'] = [
            self.enum_rects.BLIT_RESOLUTION_OPTION1.value,
            self.enum_rects.BLIT_RESOLUTION_OPTION2.value,
            self.enum_rects.BLIT_RESOLUTION_OPTION3.value,
            self.enum_rects.BLIT_IMAGE_CONFIG_ICON.value,
            self.enum_rects.BUTTON_CONFIG.value,
            self.enum_rects.BLIT_TEXT_RESOLUTION_OPTION1.value,
            self.enum_rects.BLIT_TEXT_RESOLUTION_OPTION2.value,
            self.enum_rects.BLIT_TEXT_RESOLUTION_OPTION3.value,
        ]

        self.groups['creator_info'] = [
            self.enum_rects.BLIT_TEXT_CREATOR.value,
            self.enum_rects.BUTTON_CREATOR_LINK.value,
            self.enum_rects.UNDERLINE_CREATOR_LINK.value,
        ]

        self.groups['dynamic_components'] = [
            self.enum_rects.SCREEN_BORDER.value,
        ]

    def draw_group(self, group: str, color=(255, 255, 255), px=2):
        """Desenha todos os rects pertencentes a um grupo."""
        if self.screen and group in self.groups:
            for rect_enum in self.groups[group]:
                pygame.draw.rect(self.screen, color, self.rects[rect_enum], px)

    def move_rect(self, rect_enum: EnumRects, dx: int, dy: int):
        """Move um único rect."""
        rect = self.rects.get(rect_enum)
        if rect:
            rect.move_ip(dx, dy)

    def collide_button(self, rect_enum: EnumRects):
        """Verifica se o mouse colide com um rect específico."""
        rect = self.rects.get(rect_enum)
        return rect and rect.collidepoint(pygame.mouse.get_pos())

    def clear_rect(self, rect_enum: EnumRects):
        """Limpa o rect definindo-o como um tamanho zero."""
        rect = self.rects.get(rect_enum)
        if rect:
            rect.update(0, 0, 0, 0)

    def desenho_borda(self): #TODO
        """Desenha a borda da tela."""
        rect = self.rect_manager.enum_rects.SCREEN_BORDER.value
        pygame.draw.rect(self.screen, (115, 115, 115), rect, 3)

    def animação_de_sublinhar_botao_tela_inicial(self):
        """Anima e desenha os sublinhados na tela inicial."""
        underline_player1 = self.rect_manager.enum_rects.UNDERLINE_BUTTON_PLAYER1.value
        underline_player2 = self.rect_manager.enum_rects.UNDERLINE_BUTTON_PLAYER2.value
        underline_bot = self.rect_manager.enum_rects.UNDERLINE_BUTTON_BOT.value
        underline_link = self.rect_manager.enum_rects.UNDERLINE_CREATOR_LINK.value

        if underline_player1 and underline_player2 and underline_bot and underline_link:
            # Ajusta a largura dos sublinhados com limites e incrementos
            underline_player1.width = min(max(underline_player1.width + 3, 0), 120)
            underline_player2.width = min(max(underline_player2.width + 3, 0), 122)
            underline_bot.width = min(max(underline_bot.width + 3, 0), 50)
            underline_link.width = min(max(underline_link.width + 3, 0), 280)

            # Desenha os sublinhados na tela
            pygame.draw.rect(self.rect_manager.screen, (255, 255, 255), underline_player1)
            pygame.draw.rect(self.rect_manager.screen, (255, 255, 255), underline_player2)
            pygame.draw.rect(self.rect_manager.screen, (255, 255, 255), underline_bot)
            pygame.draw.rect(self.rect_manager.screen, (255, 255, 255), underline_link)

    def botoes_tela_inicial_modos(self):
        """Renderiza e gerencia os botões e textos da tela inicial."""
        pos_mouse = pygame.mouse.get_pos()

        # Obtém os rects dos botões e textos
        rect_modo1 = self.rect_manager.enum_rects.BUTTON_PLAYER1.value
        rect_modo2 = self.rect_manager.enum_rects.BUTTON_PLAYER2.value
        rect_bot = self.rect_manager.enum_rects.BUTTON_BOT.value
        rect_creator = self.rect_manager.enum_rects.BUTTON_CREATOR_LINK.value

        blit_player1 = self.rect_manager.enum_rects.BLIT_TEXT_PLAYER1.value
        blit_player2 = self.rect_manager.enum_rects.BLIT_TEXT_PLAYER2.value
        blit_bot = self.rect_manager.enum_rects.BLIT_TEXT_BOT.value
        blit_creator = self.rect_manager.enum_rects.BLIT_TEXT_CREATOR.value

        # Atualiza as cores dos botões com base na posição do mouse
        cor_player1 = (170, 170, 170) if rect_modo1 and rect_modo1.collidepoint(pos_mouse) else (127, 127, 127)
        cor_player2 = (170, 170, 170) if rect_modo2 and rect_modo2.collidepoint(pos_mouse) else (127, 127, 127)
        cor_bot = (170, 170, 170) if rect_bot and rect_bot.collidepoint(pos_mouse) else (127, 127, 127)
        cor_creator = (170, 170, 170) if rect_creator and rect_creator.collidepoint(pos_mouse) else (127, 127, 127)

        # Renderiza os textos nos botões e no link
        font = self.fonts.font_impact
        if blit_player1:
            texto_player1 = font.render("Player1", False, cor_player1)
            self.rect_manager.screen.blit(texto_player1, blit_player1)
        if blit_player2:
            texto_player2 = font.render("Player2", False, cor_player2)
            self.rect_manager.screen.blit(texto_player2, blit_player2)
        if blit_bot:
            texto_bot = font.render("Bot", False, cor_bot)
            self.rect_manager.screen.blit(texto_bot, blit_bot)
        if blit_creator:
            texto_creator = font.render("Criado por: Gabryel-lima", False, cor_creator)
            self.rect_manager.screen.blit(texto_creator, blit_creator)

        # Executa a animação dos sublinhados
        self.animação_de_sublinhar_botao_tela_inicial()

# class ConfigButton:
#     def __init__(self, game_base):
#         self.game_base = game_base
#         self.fonte_config = pygame.font.SysFont('arial', 32, True, False)
#         self.img_config_load = pygame.image.load(PATH + 'assets/gear_config.png')
#         self.img_config = pygame.transform.scale(self.img_config_load, (50, 50))
#         self.resolution_text1 = f'600x600'
#         self.resolution_text2 = f'750x720'
#         self.resolution_text3 = f'Fullscreen'
#         self.copy_surface = pygame.SurfaceType((50, 50), pygame.SRCALPHA)
        
#     def button_config(self):
#         self.draw_button_config()
#         pos_mouse = pygame.mouse.get_pos()

#         if self.game_base.setings.rect_botao_config.collidepoint(pos_mouse):
#             scaled_copy = pygame.transform.scale_by(self.img_config, (1.1, 1.1))
#             self.game_base.screen.blit(scaled_copy, self.game_base.setings.img_xy)
#         return self.game_base.setings.rect_botao_config
        
#     def draw_button_config(self, show: bool = True):
#         if show:
#             self.copy_surface.blit(self.img_config, (0, 0))
#             self.game_base.screen.blit(self.copy_surface, self.game_base.setings.img_xy)
#         return self.game_base.setings.rect_botao_config

#     @staticmethod
#     def get_value_list(list_name: list[pygame.Rect], index: int):
#         return list_name[index]

#     def partition_draw_buttons_resolutions(self) -> Union[pygame.Rect]:
#         pos_mouse = pygame.mouse.get_pos()
#         resolution1 = self.resolution_text1
#         resolution2 = self.resolution_text2
#         resolution3 = self.resolution_text3
        
#         rect1 = self.get_value_list(list_name=self.game_base.vars_tela_config().list_tela_config, index=0)
#         rect2 = self.get_value_list(list_name=self.game_base.vars_tela_config().list_tela_config, index=1)
#         rect3 = self.get_value_list(list_name=self.game_base.vars_tela_config().list_tela_config, index=2)

#         color_rect_resolution1 = (170, 170, 170) if rect1.collidepoint(pos_mouse) else (255, 255, 255)
#         color_rect_resolution2 = (170, 170, 170) if rect2.collidepoint(pos_mouse) else (255, 255, 255)
#         color_rect_resolution3 = (170, 170, 170) if rect3.collidepoint(pos_mouse) else (255, 255, 255)

#         text1 = self.fonte_config.render(resolution1, False, color_rect_resolution1)
#         self.game_base.screen.blit(text1, self.game_base.setings.blit_xy_resolucao_texto1)
#         text2 = self.fonte_config.render(resolution2, False, color_rect_resolution2)
#         self.game_base.screen.blit(text2, self.game_base.setings.blit_xy_resolucao_texto2)
#         text3 = self.fonte_config.render(resolution3, False, color_rect_resolution3)
#         self.game_base.screen.blit(text3, self.game_base.setings.blit_xy_resolucao_texto3)

#         return rect1, rect2, rect3
