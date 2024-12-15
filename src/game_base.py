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
from .Texts import Texts
from .Points import Points
from .utils.color import Color

from collections.abc import Callable

class SetModes:
    def __init__(self):
        pass

class GameBase:
    """Base class for managing the game."""
    __subclasses__ = []

    def __init__(self):
        self.color = Color
        self.fonts = Fonts()
        self.text = Texts(self, fonts=self.fonts)
        self.rect_manager = RectManager(self, fonts=self.fonts)

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

    def run(self):
        """
        Loop principal do jogo, gerencia os estados.
        """
        running = True
        while running:
            pygame.time.Clock().tick(60)
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

    def handle_menu_events(self, event: Callable):
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

    def handle_pre_runing_events(self, event: Callable):
        """
        Gerencia os eventos na tela de pré-jogo.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            button_back = self.rect_manager.rects[self.rect_manager.enum_rects.BUTTON_BACK]
            if button_back.collidepoint(pygame.mouse.get_pos()):
                self.current_state = "menu"

        if event.type == pygame.KEYDOWN and event.key == pygame.constants.K_RETURN:
            self.start_game()

    def handle_playing_events(self, event: Callable):
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
        self.rect_manager.draw_border()
        self.blocks.draw()
        self.ball.draw()
        self.ball.update()

        if self.player_mode == "Player1":
            self.player.draw()
            self.points.draw_level(self.rect_manager, self.fonts)
            self.points.draw_pontuation(self.rect_manager, self.fonts)
            self.points.draw_best_pontuation(self.rect_manager, self.fonts)

        elif self.player_mode == "Player2":
            self.player.draw()
            self.player2.draw()
            self.points.draw_level(self.rect_manager, self.fonts)
            self.points.draw_pontuation(self.rect_manager, self.fonts)
            self.points.draw_best_pontuation(self.rect_manager, self.fonts)

        elif self.player_mode == "AI":
            self.bot.draw_bot()
            self.points.draw_level(self.rect_manager, self.fonts)
            self.points.draw_pontuation(self.rect_manager, self.fonts)
            self.points.draw_best_pontuation(self.rect_manager, self.fonts)
