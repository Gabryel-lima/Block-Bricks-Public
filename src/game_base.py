from .imports import pygame, json, webbrowser

from .Setings import ConfigVars
from .Event_Handler import EventHandler
from .Player import Player
from .Player2 import Player2
from .Bot import Bot
from .Ball import Ball
from .Blocks import Blocks
from .Fonts import Fonts
from .Rect_Manager import RectManager #, ConfigButton
from ._draw_manager import DrawManager
from .Texts import Texts
from .Points import Points
from .utils.color import Color

from collections.abc import Callable


class GameBase:
    """Base class for managing the game."""
    __subclasses__ = []

    def __init__(self):
        self.color = Color
        self.fonts = Fonts()
        self.rect_manager = RectManager(fonts=self.fonts)
        self.text = Texts(self, fonts=self.fonts)

        # Inicializa outros componentes do jogo
        self.player = Player(self)
        self.player2 = Player2(self)
        self.bot = Bot(self)
        self.ball = Ball(self)
        self.blocks = Blocks(self)
        self.points = Points(text_manager=self.text, blocks=self.blocks)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        GameBase.__subclasses__.append(cls)
        cls.__instance_count__ = 0

    def __new__(cls, *args, **kwargs):
        if cls.__instance_count__ >= 1:
            raise Exception(f"Only one instance of '{cls.__name__}' is allowed.")
        instance = super().__new__(cls)
        cls.__instance_count__ += 1
        return instance

    def selecao_de_modos_estrutura(self): # 4 em decisão de onde o palyer vai interagir 
        button_player1 = self.rect_manager.enum_rects.BUTTON_PLAYER1.to_rect()
        button_player2 = self.rect_manager.enum_rects.BUTTON_PLAYER2.to_rect()
        button_bot = self.rect_manager.enum_rects.BUTTON_BOT.to_rect()
        link = self.rect_manager.enum_rects.BUTTON_CREATOR_LINK.to_rect()

        for event in pygame.event.get():
            if event.type == pygame.constants.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_player1.collidepoint(pygame.mouse.get_pos()):
                    #self.rect_manager.clear_rect(name=button_player1)
                    pygame.time.delay(300)
                    self.player_mode = "Player1"

                    self.executar_particao(particao=self.player.draw)

                elif button_player2.collidepoint(pygame.mouse.get_pos()):
                    #self.rect_manager.clear_rect(name=button_player2)
                    pygame.time.delay(300)
                    self.player_mode = "Player2"

                    self.executar_particao(particao=self.player2.draw)

                elif button_bot.collidepoint(pygame.mouse.get_pos()):
                    #self.rect_manager.clear_rect(name=button_bot)
                    pygame.time.delay(300)
                    self.player_mode = "AI"

                    self.executar_particao(particao=self.bot.draw_bot)

                elif link.collidepoint(pygame.mouse.get_pos()):
                    webbrowser.open("https://github.com/Gabryel-lima")
                    pygame.time.delay(300)
                
                # elif self.rect_botao_config.collidepoint(pygame.mouse.get_pos()):
                #     self.config_button.draw_button_config(show=False)
                #     pygame.time.delay(300)
                    
                #     self.executar_particao_desenho_botoes_resolucao(particao_config=self.config_button.partition_draw_buttons_resolutions)

    def executar_particao(self, particao: Callable): # 5
        while True:
            for event in pygame.event.get():
                if event.type == pygame.constants.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.rect_manager.enum_rects.BUTTON_BACK.value.collidepoint(pygame.mouse.get_pos()):
                        #self.reset()
                        self.rect_manager.clear_bg_screen()
                        pygame.time.delay(300)
                        return

                if event.type == pygame.constants.KEYDOWN and event.key == pygame.constants.K_RETURN:
                    #self.rect_botao_config = pygame.rect.Rect(0,0,0,0)
                    self.game_init = True
                    self.ball.start_movement()
                    if self.player_mode == "Player1":
                        self.player.reset()
                        self.player2.rect = pygame.rect.Rect(0,0,0,0)
                        self.rect_manager.clear_bg_screen()
                        return
                    
                    elif self.player_mode == "Player2":
                        self.player.reset()
                        self.player2.reset()
                        # self.player2.rect = pygame.rect.Rect(self.player2.pos_x,
                        #                          self.player2.pos_y,
                        #                          self.player2.width_draw_x,
                        #                          self.player2.height_draw_y)
                        self.rect_manager.clear_bg_screen()
                        return
                    
                    elif self.player_mode == "AI":
                        self.bot.reset_bot()
                        self.reset_env()
                        self.player.rect = pygame.rect.Rect(0,0,0,0)
                        self.player2.rect = pygame.rect.Rect(0,0,0,0)
                        # self.bot.rect = pygame.rect.Rect(self.bot.pos_x,
                        #                                  self.bot.pos_y,
                        #                                  self.bot.width_draw_x,
                        #                                  self.bot.height_draw_y)
                        self.bot.reset_bot()
                        self.rect_manager.clear_bg_screen()
                        return

            self.rect_manager.clear_bg_screen()
            self.rect_manager.enum_rects.BUTTON_BACK.value
            self.rect_manager.render()
            self.ball.draw()
            self.blocks.draw()
            particao()
            pygame.display.update()

    def executar_pre_runing(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.constants.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    button_back = self.rect_manager.rects[self.rect_manager.enum_rects.BUTTON_BACK.to_rect()]
                    if button_back.collidepoint(pygame.mouse.get_pos()):
                        return  # Volta ao menu inicial

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return  # Sai do pré-jogo para o jogo

            self.rect_manager.render_pre_runing()
                
    def next_level(self):
        self.game_init = True
        self.ball.start_movement()
        # self.rect_manager.clear_rect(self.rect_manager.enum_rects.BUTTON_PLAYER1.to_rect())
        # self.rect_manager.clear_rect(self.rect_manager.enum_rects.BUTTON_PLAYER2.to_rect())

class GameBaseNew:
    def __init__(self):
        self.color = Color
        self.fonts = Fonts()
        self.text = Texts(self, fonts=self.fonts)
        self.rect_manager = RectManager(fonts=self.fonts)

        # Inicializa outros componentes do jogo
        self.player = Player(self)
        self.player2 = Player2(self)
        self.bot = Bot(self)
        self.ball = Ball(self)
        self.blocks = Blocks(self)
        self.points = Points(text=self.text, blocks=self.blocks)

        # Estados do jogo
        self.game_init = False
        self.current_state = "menu"  # Pode ser "menu", "pre_runing", "playing"

    def run(self):
        """
        Loop principal do jogo, gerencia os estados.
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.constants.QUIT:
                    running = False

                if self.current_state == "menu":
                    self.handle_menu_events(event)

                elif self.current_state == "pre_runing":
                    self.handle_pre_runing_events(event)

                elif self.current_state == "playing":
                    self.handle_playing_events(event)

            # Renderiza a tela com base no estado atual
            if self.current_state == "menu":
                self.rect_manager.render_init()

            elif self.current_state == "pre_runing":
                self.rect_manager.render_pre_runing()

            elif self.current_state == "playing":
                self.render_game()

            pygame.display.update()

        pygame.quit()

    def handle_menu_events(self, event):
        """
        Gerencia os eventos no menu inicial.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            button_player1 = self.rect_manager.rects[self.rect_manager.enum_rects.BUTTON_PLAYER1]
            button_player2 = self.rect_manager.rects[self.rect_manager.enum_rects.BUTTON_PLAYER2]
            button_bot = self.rect_manager.rects[self.rect_manager.enum_rects.BUTTON_BOT]

            if button_player1.collidepoint(pygame.mouse.get_pos()):
                self.current_state = "pre_runing"
                self.player_mode = "Player1"

            elif button_player2.collidepoint(pygame.mouse.get_pos()):
                self.current_state = "pre_runing"
                self.player_mode = "Player2"

            elif button_bot.collidepoint(pygame.mouse.get_pos()):
                self.current_state = "pre_runing"
                self.player_mode = "AI"

    def handle_pre_runing_events(self, event):
        """
        Gerencia os eventos na tela de pré-jogo.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            button_back = self.rect_manager.rects[self.rect_manager.enum_rects.BUTTON_BACK]
            if button_back.collidepoint(pygame.mouse.get_pos()):
                self.current_state = "menu"

        if event.type == pygame.KEYDOWN and event.key == pygame.constants.K_RETURN:
            self.start_game()

    def handle_playing_events(self, event):
        """
        Gerencia os eventos durante o jogo.
        """
        if self.player_mode in ["Player1", "Player2"]:
            self.player.input_player()
            if self.player_mode == "Player2":
                self.player2.input_player()

        if self.player_mode == "AI":
            self.bot.update()

    def start_game(self):
        """
        Configura o estado inicial do jogo.
        """
        self.game_init = True
        self.current_state = "playing"
        self.ball.start_movement()
        self.player.reset()
        self.player2.reset() if self.player_mode == "Player2" else None
        self.bot.reset_bot() if self.player_mode == "AI" else None

    def render_game(self):
        """
        Renderiza a tela durante o jogo.
        """
        self.rect_manager.clear_bg_screen()
        self.blocks.draw()
        self.ball.draw()

        if self.player_mode == "Player1":
            self.player.draw()
            self.points.draw_pontuation()
            self.points.draw_best_pontuation()
            self.points.draw_level()

        elif self.player_mode == "Player2":
            self.player.draw()
            self.player2.draw()
            self.points.draw_pontuation()
            self.points.draw_best_pontuation()
            self.points.draw_level()

        elif self.player_mode == "AI":
            self.bot.draw_bot()
            self.points.draw_pontuation()
            #self.points.draw_best_bot_pontuation()
            self.points.draw_level()

