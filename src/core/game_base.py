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
from src.core.rect_manager import RectManager


class GameBase:
    def __init__(self):
        self.rect_manager = RectManager()
        self.player = Player(self)
        self.player2 = Player2(self)
        self.bot = Bot(self)
        self.ball = Ball(self)
        self.blocks = Blocks(self)
        self.fonts = Fonts()
        self.config_button = ConfigButton(self)
        self.resizeinterface = ResizeInterface(self)
        self.setings = ConfigVars(self)

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

