from src.core.imports import pygame


class TextManager:
    def __init__(self, fonnts):
        self.fonts = fonnts
        self.over: str = 'Game Over'
        self.win: str = 'You win!'
        self.player_1_2: str = f'Player {0}'
        self.modo_bot: str = 'Bot'
        self.back: str = 'Back'
        self.best_pontuation: str = f'Best pontuation: {0}'
        self.button_iter: str = f'Pressione a tecla {"Enter"} para iniciar'
        self.init_points_1_2: str = f'Points: {0}'
        self.init_level: int = 1
        self.level: str = f'Level: {self.init_level}'

    def draw_pontuation(self):
        mensagem = self.mens_points_1_2
        texto_formatado = self.fonts.font_candara.render(mensagem, False, (127,127,127))
        self.screen.blit(texto_formatado, self.blit_xy_mesg1_pontos)

    def draw_best_pontuation(self):
        mensagem = self.mens_bp
        texo_formatado = self.fonts.font_candara.render(mensagem, False, (127,127,127))
        self.screen.blit(texo_formatado, self.blit_xy_mesg_bp1)

    def draw_level(self):
        mensagem = self.mens_level
        texto_formatado = self.fonts.font_candara.render(mensagem, False, (127, 127, 127))
        self.screen.blit(texto_formatado, self.blit_xy_exibe_nivel)

