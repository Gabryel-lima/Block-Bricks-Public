
from src.core.imports import pygame, json, webbrowser


from src.core.setings import ConfigVars
from src.core.player import Player
from src.core.player2 import Player2
from src.core.bot import Bot
from src.core.ball import Ball
from src.core.blocks import Blocks
from src.core.config_button import ConfigButton
from src.core.resize_Interface import ResizeInterface
from src.core.fonts import Fonts


class GameBase:
    def __init__(self):
        self.vars_screen_dimensions()
        self.vars_tela_inicial()
        self.vars_tela_config()
        self.vars_pre_pos_start()
        self.player = Player(self)
        self.player2 = Player2(self)
        self.bot = Bot(self)
        self.ball = Ball(self)
        self.blocks = Blocks(self)
        self.fonts = Fonts()
        self.config_button = ConfigButton(self)
        self.resizeinterface = ResizeInterface(self)
        self.setings = ConfigVars(self)
        #self.mens_ite_init = f'Pressione a tecla "Enter" para iniciar'
        self.resolution_base = (600, 600)
        self.resolution_base2 = (745, 690)
        self.modo_player1 = 'Player 1'
        self.modo_player2 = 'Player 2'
        self.modo_bot = "Bot"
        self.back = f"Back"
        self.level = 1
        self.mens_level = f'Level: {self.level}'
        self.init_points = 0
        self.mens_points_1_2 = f'Points: {self.init_points}'
        self.loading_lp2 = self.load_best_pontuation_player2()
        self.mens_bp2 = f'Best pontuation: {self.loading_lp2}'
        self.player_mode = None

    __subclasses__ = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        GameBase.__subclasses__.append(cls)
        cls.__instace_count__ = 0

    def __new__(cls, *args, **kwargs):
        if cls.__instace_count__ >= 1:
            raise Exception(f"Já existe uma instância da classe '{cls.__name__}'. Apenas uma instância é permitida.")
        
        instance = super().__new__(cls)
        cls.__instace_count__ += 1
        return instance

    def vars_screen_dimensions(self, width: int = 608, height: int = 608) -> object | int | tuple[int]:
        self.width = width
        self.height = height
        self.relative_height_ball = 180
        self.screen = pygame.display.set_mode(size=(self.width, self.height))
        self.border = pygame.Rect((0, 0), (self.width, self.height))
        self.dimension_list_screen = [self.border]

        return self

    def vars_tela_inicial(self):
        self.blit_xy_player1 = pygame.Rect(245, 170, 170, 0)
        self.blit_xy_player2 = pygame.Rect(245, 230, 230, 0)
        self.blit_xy_bot = pygame.Rect(245, 290, 120, 0)  # Alinhar horizontalmente ao player1 e player2
        self.rect_botao_player1 = pygame.Rect(240, 170, 120, 40)
        self.rect_botao_player2 = pygame.Rect(240, 230, 120, 40)
        self.rect_botao_bot = pygame.Rect(240, 290, 120, 40)  # Alinhar horizontalmente ao player1 e player2
        self.rect_botao_sublinhar_mod_player = pygame.Rect(245, 210, 0, 5)
        self.rect_botao_sublinhar_mod_player2 = pygame.Rect(245, 270, 0, 5)
        self.rect_botao_sublinhar_bot = pygame.Rect(245, 330, 0, 5)  # Mantendo o alinhamento e proporção de sublinhar
        self.blit_xy_clink = pygame.Rect(40, 520, 0, 0)
        self.clink_rect = pygame.Rect(40, 522, 280, 30)
        self.rect_botao_sublinhar_clink = pygame.Rect(40, 558, 0, 3)
        self.list_tela_inicial = [self.rect_botao_player1,
                                    self.rect_botao_player2,
                                    self.blit_xy_player1,
                                    self.blit_xy_player2,
                                    self.rect_botao_sublinhar_mod_player,
                                    self.rect_botao_sublinhar_mod_player2,
                                    self.blit_xy_clink,
                                    self.clink_rect,
                                    self.rect_botao_sublinhar_clink]
        return self
    
    def vars_pre_pos_start(self):
        self.rect_botao_voltar = pygame.Rect(40, 300, 85, 30)
        self.rect_botao_sublinhar_voltar = pygame.Rect(40, 340, 0, 3)
        self.mesg_fj_blit_xy = pygame.Rect(215, 225, 0, 0)
        self.blit_xy_voltar = pygame.Rect(40, 300, 0, 0)
        self.blit_xy_mesg1_pontos = pygame.Rect(40, 430, 0, 0)
        self.blit_xy_mesg_bp1 = pygame.Rect(40, 530, 0, 0)
        self.blit_xy_exibe_nivel = pygame.Rect(40, 480, 0, 0)
        self.blit_xy_mesg2_pontos = pygame.Rect(40, 430, 0, 0)
        self.blit_xy_mesg_bp2 = pygame.Rect(40, 530, 0, 0)
        # self.blit_xy_iniciar_enter = pygame.Rect(95, 195, 0, 0)
        # self.blit_xy_iniciar_controles = pygame.Rect(55, 235, 0, 0)
        # self.blit_xy_iniciar_controles2 = pygame.Rect(45, 265, 0, 0)
        self.list_pre_pos_start = [self.rect_botao_voltar,
                                self.rect_botao_sublinhar_voltar,
                                self.mesg_fj_blit_xy,
                                self.blit_xy_voltar,
                                self.blit_xy_mesg1_pontos,
                                self.blit_xy_mesg_bp1,
                                self.blit_xy_exibe_nivel,
                                self.blit_xy_mesg2_pontos,
                                self.blit_xy_mesg_bp2,
                                ]
        return self

    def vars_tela_config(self):
        #self.fonte_config = pygame.font.SysFont('arial', 32, True, False)
        self.rect_resolucao_texto1 = pygame.Rect(0, 0, 0, 0) # 240,170,120,40
        self.rect_resolucao_texto2 = pygame.Rect(240, 230, 120, 40)
        self.rect_resolucao_texto3 = pygame.Rect(240, 290, 120, 40)
        self.img_xy = pygame.Rect(475, 495, 0, 0)
        self.rect_botao_config = pygame.Rect(474.5, 494.0, 53.0, 53.0)
        self.blit_xy_resolucao_texto1 = pygame.Rect(245, 170, 0, 0)
        self.blit_xy_resolucao_texto2 = pygame.Rect(245, 230, 0, 0)
        self.blit_xy_resolucao_texto3 = pygame.Rect(232, 290, 0, 0)
        self.list_tela_config = [self.rect_resolucao_texto1,
                                    self.rect_resolucao_texto2,
                                    self.rect_resolucao_texto3,
                                    self.blit_xy_resolucao_texto1,
                                    self.blit_xy_resolucao_texto2,
                                    self.blit_xy_resolucao_texto3,
                                    self.img_xy, 
                                    self.rect_botao_config]
        return self
            
    def load_best_pontuation_player2(self):
        try:
            with open('src/json/best_score2.json', 'r') as file:
                data = json.load(file)
                return data['best_score2']
        except (FileNotFoundError, KeyError):
            return 0

    def save_best_pontuation_player2(self):
        data = {'best_score2': self.loading_lp2}
        with open('src/json/best_score2.json', 'w') as file:
            json.dump(data, file)

    def update_best_pontuation_player2(self):
        if self.init_points > self.loading_lp2:
            self.loading_lp2 = self.init_points
            self.save_best_pontuation_player2()
            self.mens_bp2 = f'Best pontuation: {self.loading_lp2}'

    def exibe_melhor_pontuacao2(self):
        mensagem = self.mens_bp2
        texo_formatado = self.fonts.font_candara.render(mensagem, False, (127, 127, 127))
        self.screen.blit(texo_formatado, self.blit_xy_mesg_bp2)
    
    def exibir_pontuacao2(self):
        mensagem = self.mens_points_1_2
        texto_formatado = self.fonts.font_candara.render(mensagem, False, (127, 127, 127))
        self.screen.blit(texto_formatado, self.blit_xy_mesg2_pontos)

    def atualiza_pontuacao2(self):
        self.init_points += 1
        self.mens_points_1_2 = f'Points: {self.init_points}'

    def desenho_borda(self):
        pygame.draw.rect(self.screen, (115, 115, 115), self.border, 3)

    def animaçao_de_sublinhar_botao_tela_inicial(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect_botao_sublinhar_mod_player)
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect_botao_sublinhar_mod_player2)
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect_botao_sublinhar_bot)
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect_botao_sublinhar_clink)

        self.rect_botao_sublinhar_mod_player.width = min(self.rect_botao_sublinhar_mod_player.width, 120)
        self.rect_botao_sublinhar_mod_player.width = max(self.rect_botao_sublinhar_mod_player.width, 0)
        self.rect_botao_sublinhar_mod_player2.width = min(self.rect_botao_sublinhar_mod_player2.width, 122)
        self.rect_botao_sublinhar_mod_player2.width = max(self.rect_botao_sublinhar_mod_player2.width, 0)
        self.rect_botao_sublinhar_bot.width = min(self.rect_botao_sublinhar_bot.width, 50)
        self.rect_botao_sublinhar_bot.width = max(self.rect_botao_sublinhar_bot.width, 0)
        self.rect_botao_sublinhar_clink.width = min(self.rect_botao_sublinhar_clink.width, 3)
        self.rect_botao_sublinhar_clink.width = max(self.rect_botao_sublinhar_clink.width, 0)

    def botoes_tela_inicial_modos(self):  # 1
        pos_mouse = pygame.mouse.get_pos()
        mod1 = self.modo_player1
        mod2 = self.modo_player2
        bot_mode = self.modo_bot
        rect_modo1 = self.rect_botao_player1
        rect_modo2 = self.rect_botao_player2
        rect_bot = self.rect_botao_bot  # Adicionei aqui o retângulo do botão do bot
        rect_c = self.clink_rect

        # Cor do botão Player 1
        self.cor_botao_modo1 = (170, 170, 170) if rect_modo1.collidepoint(pos_mouse) else (127, 127, 127)
        self.rect_botao_sublinhar_mod_player.width += 3 if rect_modo1.collidepoint(pos_mouse) else -2

        # Cor do botão Player 2
        self.cor_botao_modo2 = (170, 170, 170) if rect_modo2.collidepoint(pos_mouse) else (127, 127, 127)
        self.rect_botao_sublinhar_mod_player2.width += 3 if rect_modo2.collidepoint(pos_mouse) else -2

        # Cor do botão Bot
        self.cor_botao_bot = (170, 170, 170) if rect_bot.collidepoint(pos_mouse) else (127, 127, 127)
        self.rect_botao_sublinhar_bot.width += 3 if rect_modo2.collidepoint(pos_mouse) else -2
        
        # Cor do link
        self.cor_clink = (170, 170, 170) if rect_c.collidepoint(pos_mouse) else (127, 127, 127)
        self.rect_botao_sublinhar_clink.width += 280 if rect_c.collidepoint(pos_mouse) else -280

        if self.rect_botao_player1.width > 0 and self.rect_botao_player2.width > 0 and self.clink_rect.width > 0 and self.rect_botao_bot.width > 0:
            # Renderizar texto para os botões
            texto_formatado1 = self.fonts.font_arial.render(mod1, False, self.cor_botao_modo1)
            self.screen.blit(texto_formatado1, self.blit_xy_player1)
            texto_formatado2 = self.fonts.font_arial.render(mod2, False, self.cor_botao_modo2)
            self.screen.blit(texto_formatado2, self.blit_xy_player2)

            # Renderizar botão do Bot
            texto_formatado_bot = self.fonts.font_arial.render(bot_mode, False, self.cor_botao_bot)
            self.screen.blit(texto_formatado_bot, self.blit_xy_bot)

            # Renderizar o link
            texto_clink = 'Criado por: Gabryel-lima'
            texto_formatado_c = self.fonts.font_impact.render(texto_clink, False, self.cor_clink)
            self.screen.blit(texto_formatado_c, self.blit_xy_clink)

            # Outros componentes
            self.config_button.button_config()  # 2
            self.animaçao_de_sublinhar_botao_tela_inicial()  # 3

    def executar_particao_proporcao_resolucao(self):
        self.resizeinterface.calculo_obter_proporcao(nova_resolucao=self.resolution_base)
        self.resizeinterface.calculo_obter_proporcao_blocos(nova_resolucao=self.resolution_base)
        self.resizeinterface.calculo_obter_proporcao_players(nova_resolucao=self.resolution_base)
        self.config_button.copy_surface.fill((0, 0, 0))

    def executar_particao_proporcao_resolucao2(self):
        self.list_tela_config[0] = pygame.Rect(240, 170, 120, 40)

        self.resizeinterface.calculo_obter_proporcao(nova_resolucao=self.resolution_base2)
        self.vars_screen_dimensions(width=self.resolution_base2[0], height=self.resolution_base2[1])

        self.resizeinterface.calculo_obter_proporcao_blocos(nova_resolucao=self.resolution_base2)
        self.resizeinterface.calculo_obter_proporcao_players(nova_resolucao=self.resolution_base2)
        
        self.config_button.copy_surface.fill((0, 0, 0))

    def executar_particao_desenho_botoes_resolucao(self, particao_config: None): # ou 5
        while True:
            for event in pygame.event.get():
                if event.type == pygame.constants.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    rect1, rect2, rect3 = self.config_button.partition_draw_buttons_resolutions()

                    if rect1.collidepoint(pygame.mouse.get_pos()):
                        self.executar_particao_proporcao_resolucao()
                        return
                    elif rect2.collidepoint(pygame.mouse.get_pos()):
                        self.executar_particao_proporcao_resolucao2()
                        return

            self.screen.fill((0, 0, 0))
            self.desenho_borda()
            particao_config()
            pygame.display.update()

    def desenho_botao_back(self) -> pygame.Rect:
        pos_mouse = pygame.mouse.get_pos()
        rect_botao = self.rect_botao_voltar
        mensagem = self.back

        self.cor_botao_voltar = (150,150,150) if rect_botao.collidepoint(pos_mouse) else (127,127,127)
        self.rect_botao_sublinhar_voltar.width += 68 if rect_botao.collidepoint(pos_mouse) else -6

        if self.rect_botao_voltar.width > 0:  
            texto_formatado1 = self.fonts.font_arial.render(mensagem, False, self.cor_botao_voltar)
            self.screen.blit(texto_formatado1, self.blit_xy_voltar)

            self.animaçao_de_sublinhar_botao_voltar()

        return rect_botao

    def animaçao_de_sublinhar_botao_voltar(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect_botao_sublinhar_voltar)

        self.rect_botao_sublinhar_voltar.width = min(self.rect_botao_sublinhar_voltar.width, 6)
        self.rect_botao_sublinhar_voltar.width = max(self.rect_botao_sublinhar_voltar.width, 0)

    def selecao_de_modos_estrutura(self): # 4 em decisão de onde o palyer vai interagir 
        for event in pygame.event.get():
            if event.type == pygame.constants.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect_botao_player1.collidepoint(pygame.mouse.get_pos()):
                    self.rect_botao_player1 = pygame.Rect(0,0,0,0)
                    pygame.time.delay(300)
                    self.player_mode = "Player1"

                    self.executar_particao(particao=self.player.desenho_player)

                elif self.rect_botao_player2.collidepoint(pygame.mouse.get_pos()):
                    self.rect_botao_player2 = pygame.Rect(0,0,0,0)
                    pygame.time.delay(300)
                    self.player_mode = "Player2"

                    self.executar_particao(particao=self.player2.desenho_player)

                elif self.rect_botao_bot.collidepoint(pygame.mouse.get_pos()):
                    self.rect_botao_bot = pygame.Rect(0,0,0,0)
                    pygame.time.delay(300)
                    self.player_mode = "AI"

                    self.executar_particao(particao=self.bot.draw_bot)

                elif self.clink_rect.collidepoint(pygame.mouse.get_pos()):
                    webbrowser.open("https://github.com/Gabryel-lima")
                    pygame.time.delay(300)
                
                elif self.rect_botao_config.collidepoint(pygame.mouse.get_pos()):
                    self.config_button.draw_button_config(show=False)
                    pygame.time.delay(300)
                    
                    self.executar_particao_desenho_botoes_resolucao(particao_config=self.config_button.partition_draw_buttons_resolutions)

    def executar_particao(self, particao=None): # 5
        while True:
            for event in pygame.event.get():
                if event.type == pygame.constants.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.desenho_botao_back().collidepoint(pygame.mouse.get_pos()):
                        self.reset()
                        self.screen.fill((0, 0, 0))
                        pygame.time.delay(300)
                        return

                if event.type == pygame.constants.KEYDOWN and event.key == pygame.constants.K_RETURN:
                    self.rect_botao_config = pygame.rect.Rect(0,0,0,0)
                    self.game_init = True
                    self.ball.start_movement()
                    if self.player_mode == "Player1":
                        self.player.reset()
                        self.player2.rect = pygame.rect.Rect(0,0,0,0)
                        self.screen.fill((0, 0, 0))
                        return
                    
                    elif self.player_mode == "Player2":
                        self.player.resetp_1()
                        self.player2.reset()
                        self.player2.rect = pygame.rect.Rect(self.player2.pos_x,
                                                 self.player2.pos_y,
                                                 self.player2.width_draw_x,
                                                 self.player2.height_draw_y)
                        self.screen.fill((0, 0, 0))
                        return
                    
                    elif self.player_mode == "AI":
                        self.bot.reset_bot()
                        self.reset_env()
                        self.player.rect = pygame.rect.Rect(0,0,0,0)
                        self.player2.rect = pygame.rect.Rect(0,0,0,0)
                        self.bot.rect = pygame.rect.Rect(self.bot.pos_x,
                                                         self.bot.pos_y,
                                                         self.bot.width_draw_x,
                                                         self.bot.height_draw_y)
                        self.screen.fill((0, 0, 0))
                        return

            self.screen.fill((0, 0, 0))
            self.desenho_botao_back()
            self.desenho_borda()
            self.ball.draw()
            self.blocks.desenhar_blocos()
            particao()
            pygame.display.update()

    def niveis_count(self):
        self.level += 1
        self.mens_level = f'Level: {self.level}'
                
    def manipula_nivel(self):
        while True:
            self.blocks.criar_blocos()
            break

    def continuar_prox_nivel(self):
        self.game_init = True
        self.ball.start_movement()
        self.manipula_nivel()
        self.rect_botao_player1 = pygame.Rect(0,0,0,0)
        self.rect_botao_player2 = pygame.Rect(0,0,0,0)

