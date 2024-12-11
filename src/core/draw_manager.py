from src.core.imports import pygame


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
        self.init_points = 0

    def exibe_melhor_pontuacao2(self):
        """Exibe a melhor pontuação do jogador 2."""
        mensagem = self.text_manager.mens_bp2
        texto_formatado = self.fonts.font_candara.render(mensagem, False, (127, 127, 127))
        rect = self.rect_manager.get_rect('blit_text_best_points_player2')
        self.screen.blit(texto_formatado, rect)

    def exibir_pontuacao2(self):
        """Exibe a pontuação atual do jogador 2."""
        mensagem = self.text_manager.mens_points_1_2
        texto_formatado = self.fonts.font_candara.render(mensagem, False, (127, 127, 127))
        rect = self.rect_manager.get_rect('blit_text_points_player2')
        self.screen.blit(texto_formatado, rect)

    def atualiza_pontuacao2(self):
        """Atualiza a pontuação do jogador 2."""
        self.init_points += 1
        self.text_manager.mens_points_1_2 = f"Points: {self.init_points}"

    def desenho_borda(self):
        """Desenha a borda da tela."""
        rect = self.rect_manager.get_rect('screen_border')
        pygame.draw.rect(self.screen, (115, 115, 115), rect, 3)

    def animação_de_sublinhar_botao_tela_inicial(self):
        """Anima o sublinhado dos botões na tela inicial."""
        underline_player1 = self.rect_manager.get_rect('underline_button_player1')
        underline_player2 = self.rect_manager.get_rect('underline_button_player2')
        underline_bot = self.rect_manager.get_rect('underline_button_bot')
        underline_link = self.rect_manager.get_rect('underline_creator_link')

        # Ajusta a largura dos rects de sublinhar
        underline_player1.width = min(underline_player1.width + 2, 120)
        underline_player1.width = max(underline_player1.width - 1, 0)
        underline_player2.width = min(underline_player2.width + 2, 122)
        underline_player2.width = max(underline_player2.width - 1, 0)
        underline_bot.width = min(underline_bot.width + 2, 50)
        underline_bot.width = max(underline_bot.width - 1, 0)
        underline_link.width = min(underline_link.width + 5, 280)
        underline_link.width = max(underline_link.width - 5, 0)

        # Desenha os rects de sublinhar
        pygame.draw.rect(self.screen, (255, 255, 255), underline_player1)
        pygame.draw.rect(self.screen, (255, 255, 255), underline_player2)
        pygame.draw.rect(self.screen, (255, 255, 255), underline_bot)
        pygame.draw.rect(self.screen, (255, 255, 255), underline_link)

    def botoes_tela_inicial_modos(self):
        """Renderiza os botões da tela inicial."""
        pos_mouse = pygame.mouse.get_pos()

        # Obtém os rects dos botões e textos
        rect_modo1 = self.rect_manager.get_rect('button_player1')
        rect_modo2 = self.rect_manager.get_rect('button_player2')
        rect_bot = self.rect_manager.get_rect('button_bot')
        rect_c = self.rect_manager.get_rect('button_creator_link')

        blit_player1 = self.rect_manager.get_rect('blit_text_player1')
        blit_player2 = self.rect_manager.get_rect('blit_text_player2')
        blit_bot = self.rect_manager.get_rect('blit_text_bot')
        blit_clink = self.rect_manager.get_rect('blit_text_creator')

        # Atualiza as cores com base no posicionamento do mouse
        self.cor_botao_modo1 = (170, 170, 170) if rect_modo1.collidepoint(pos_mouse) else (127, 127, 127)
        self.cor_botao_modo2 = (170, 170, 170) if rect_modo2.collidepoint(pos_mouse) else (127, 127, 127)
        self.cor_botao_bot = (170, 170, 170) if rect_bot.collidepoint(pos_mouse) else (127, 127, 127)
        self.cor_clink = (170, 170, 170) if rect_c.collidepoint(pos_mouse) else (127, 127, 127)

        # Renderiza os textos nos botões
        texto_formatado1 = self.fonts.font_arial.render("Player 1", False, self.cor_botao_modo1)
        self.screen.blit(texto_formatado1, blit_player1)

        texto_formatado2 = self.fonts.font_arial.render("Player 2", False, self.cor_botao_modo2)
        self.screen.blit(texto_formatado2, blit_player2)

        texto_formatado_bot = self.fonts.font_arial.render("Bot", False, self.cor_botao_bot)
        self.screen.blit(texto_formatado_bot, blit_bot)

        texto_clink = "Criado por: Gabryel-lima"
        texto_formatado_c = self.fonts.font_impact.render(texto_clink, False, self.cor_clink)
        self.screen.blit(texto_formatado_c, blit_clink)

        # Renderiza os componentes adicionais
        #self.config_button.button_config()
        self.animação_de_sublinhar_botao_tela_inicial()
