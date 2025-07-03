from src.imports import pygame


class DrawManager:
    def __init__(self,
                 screen: pygame.Surface, blocks, text_manager, rect_manager: pygame.rect.Rect, 
                 fonts, color):
        """
        Inicializa o DrawManager com a tela, o RectManager e outras dependências.

        :param screen: Superfície principal do jogo (pygame.display.set_mode).
        :param blocks: Se refere aos alvos a serem destruidos do jogo.
        :param text_manager: Textos do jogo.
        :param rect_manager: Instância do RectManager para gerenciar os rects.
        :param fonts: Objeto para gerenciar fontes.
        :param config_button: Instância para gerenciar o botão de configurações.
        :param color: Cores do jogo.
        """
        self.screen = screen
        self.blocks = blocks
        self.text_manager = text_manager
        self.rect_manager = rect_manager
        self.fonts = fonts
        #self.config_button = config_button
        self.color = color

        # Cores e pontuações iniciais
        self.cor_botao_modo1 = (self.color.GRAY)
        self.cor_botao_modo2 = (self.color.GRAY)
        self.cor_botao_bot = (self.color.GRAY)
        self.cor_clink = (self.color.GRAY)



