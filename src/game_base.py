from .imports import pygame, json, webbrowser

from .setings import ConfigVars
from .Event_Handler import EventHandler
from .player import Player
from .player2 import Player2
from .bot import Bot
from .ball import Ball
from .blocks import Blocks
from .fonts import Fonts
from .rect_manager import RectManager #, ConfigButton
from .draw_manager import DrawManager
from .text_manager import TextManager
from .points import Points
from .color import Color

from collections.abc import Callable


class GameBase:
    """Base class for managing the game."""
    __subclasses__ = []

    def __init__(self):
        self.color = Color
        #self.event_handler = EventHandler()
        self.rect_manager = RectManager(self)
        self.fonts = Fonts()
        self.text = TextManager(self, fonts=self.fonts)
        self.player = Player(self)
        self.player2 = Player2(self)
        self.bot = Bot(self)
        self.ball = Ball(self)
        self.blocks = Blocks(self)
        self.points = Points(text_manager=self.text, blocks=self.blocks)
        self.draw_manager = DrawManager(
            screen=self.rect_manager.screen,
            blocks=self.blocks,
            text_manager=self.text,
            rect_manager=self.rect_manager,
            fonts=self.fonts,
            color=self.color
        )
        #self.setings = ConfigVars(self) # TODO: Ainda tenho que ver como vai funcionar melhor.

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

    def desenho_botao_back(self) -> pygame.Rect: # TODO: Isso aqui definitivamente está horroroso
        pos_mouse = pygame.mouse.get_pos()
        rect_botao = self.rect_manager.get_rect("button_back")
        mensagem = self.text.back
        rect_back_sublime = self.rect_manager.get_rect("underline_back")

        self.cor_botao_voltar = (150, 150, 150) if rect_botao.collidepoint(pos_mouse) else (127, 127, 127)
        rect_back_sublime.width += 68 if rect_botao.collidepoint(pos_mouse) else -6

        if rect_botao.width > 0:  
            texto_formatado1 = self.fonts.font_arial.render(mensagem, False, self.cor_botao_voltar)
            self.rect_manager.screen.blit(texto_formatado1, self.rect_manager.get_rect("blit_text_back"))

            self.animaçao_de_sublinhar_botao_voltar()

        return rect_botao

    def animaçao_de_sublinhar_botao_voltar(self):
        rect_back_sublime = self.rect_manager.get_rect("underline_back")

        pygame.draw.rect(self.rect_manager.screen, (255, 255, 255), rect_back_sublime)

        rect_back_sublime.width = min(rect_back_sublime.width, 6)
        rect_back_sublime.width = max(rect_back_sublime.width, 0)

    def selecao_de_modos_estrutura(self): # 4 em decisão de onde o palyer vai interagir 
        button_player1 = self.rect_manager.get_rect("button_player1")

        for event in pygame.event.get():
            if event.type == pygame.constants.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_player1.collidepoint(pygame.mouse.get_pos()):
                    self.rect_botao_player2 = pygame.Rect(0,0,0,0)
                    self.bot.rect = pygame.Rect(0,0,0,0)
                    pygame.time.delay(300)
                    self.player_mode = "Player1"

                    self.executar_particao(particao=self.player.draw)

                elif self.rect_botao_player2.collidepoint(pygame.mouse.get_pos()):
                    button_player1 = pygame.Rect(0,0,0,0)
                    self.bot.rect = pygame.Rect(0,0,0,0)
                    pygame.time.delay(300)
                    self.player_mode = "Player2"

                    self.executar_particao(particao=self.player2.draw)

                elif self.rect_botao_bot.collidepoint(pygame.mouse.get_pos()):
                    self.rect_botao_bot = pygame.Rect(0,0,0,0)
                    button_player1 = pygame.Rect(0,0,0,0)
                    self.rect_botao_player2 = pygame.Rect(0,0,0,0)
                    pygame.time.delay(300)
                    self.player_mode = "AI"

                    self.executar_particao(particao=self.bot.draw_bot)

                elif self.clink_rect.collidepoint(pygame.mouse.get_pos()):
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
                    if self.desenho_botao_back().collidepoint(pygame.mouse.get_pos()):
                        self.reset()
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
            self.desenho_botao_back()
            self.draw_manager.desenho_borda()
            self.ball.draw()
            self.blocks.draw()
            particao()
            pygame.display.update()
                
    def next_level(self):
        self.game_init = True
        self.ball.start_movement()
        self.rect_manager.clear_rect(name="button_player1")
        self.rect_manager.clear_rect(name="button_player2")

