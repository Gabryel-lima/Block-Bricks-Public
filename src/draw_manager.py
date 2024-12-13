from .imports import pygame


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

    def exibe_melhor_pontuacao2(self): #TODO
        """Exibe a melhor pontuação do jogador 2."""
        mensagem = self.text_manager.mens_bp2
        texto_formatado = self.fonts.font_candara.render(mensagem, False, (127, 127, 127))
        rect = self.rect_manager.get_rect('blit_text_best_points_player2')
        self.screen.blit(texto_formatado, rect)

    def exibir_pontuacao2(self): #TODO
        """Exibe a pontuação atual do jogador 2."""
        mensagem = self.text_manager.mens_points_1_2
        texto_formatado = self.fonts.font_candara.render(mensagem, False, (127, 127, 127))
        rect = self.rect_manager.get_rect('blit_text_points_player2')
        self.screen.blit(texto_formatado, rect)

    def atualiza_pontuacao2(self): #TODO
        """Atualiza a pontuação do jogador 2."""
        self.init_points += 1
        self.text_manager.mens_points_1_2 = f"Points: {self.init_points}"

    def desenho_borda(self): #TODO
        """Desenha a borda da tela."""
        rect = self.rect_manager.get_rect('screen_border')
        pygame.draw.rect(self.screen, (115, 115, 115), rect, 3)

    def animação_de_sublinhar_botao_tela_inicial(self):
        """Anima e desenha os sublinhados na tela inicial."""
        underline_player1 = self.rect_manager.get_rect('underline_button_player1')
        underline_player2 = self.rect_manager.get_rect('underline_button_player2')
        underline_bot = self.rect_manager.get_rect('underline_button_bot')
        underline_link = self.rect_manager.get_rect('underline_creator_link')

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
        rect_modo1 = self.rect_manager.get_rect('button_player1')
        rect_modo2 = self.rect_manager.get_rect('button_player2')
        rect_bot = self.rect_manager.get_rect('button_bot')
        rect_creator = self.rect_manager.get_rect('button_creator_link')

        blit_player1 = self.rect_manager.get_rect('blit_text_player1')
        blit_player2 = self.rect_manager.get_rect('blit_text_player2')
        blit_bot = self.rect_manager.get_rect('blit_text_bot')
        blit_creator = self.rect_manager.get_rect('blit_text_creator')

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

