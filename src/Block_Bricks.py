import pygame
from src.game_base import GameBase
from src.rect_manager import RectManager
from src.player import Player
from src.player2 import Player2
from src.bot import Bot
from src.ball import Ball
from src.blocks import Blocks
from src.points import Points

class BlockBricks(GameBase):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.rect_manager = RectManager()
        self.player = Player(self.rect_manager)
        self.player2 = Player2(self.rect_manager)
        self.bot = Bot(self.rect_manager)
        self.ball = Ball(self.rect_manager)
        self.blocks = Blocks(self.rect_manager)
        self.points = Points(self.blocks)
        self.player_mode = None  # 'Player1', 'Player2', 'AI'
        self.set_entities(
            player=self.player,
            player2=self.player2,
            bot=self.bot,
            ball=self.ball,
            blocks=self.blocks,
            points=self.points,
            rect_manager=self.rect_manager
        )
        self.current_state = 'menu'

    def handle_event(self, event):
        if self.current_state == 'menu':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if self.rect_manager.rects[self.rect_manager.enum_rects.BUTTON_PLAYER1].collidepoint(pos):
                    self.player_mode = 'Player1'
                    self.current_state = 'pre_runing'
                elif self.rect_manager.rects[self.rect_manager.enum_rects.BUTTON_PLAYER2].collidepoint(pos):
                    self.player_mode = 'Player2'
                    self.current_state = 'pre_runing'
                elif self.rect_manager.rects[self.rect_manager.enum_rects.BUTTON_BOT].collidepoint(pos):
                    self.player_mode = 'AI'
                    self.current_state = 'pre_runing'
        elif self.current_state == 'pre_runing':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if self.rect_manager.rects[self.rect_manager.enum_rects.BUTTON_BACK].collidepoint(pos):
                    self.current_state = 'menu'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.start_game()
        elif self.current_state == 'playing':
            if self.player_mode == 'Player1':
                self.player.input_player()
            elif self.player_mode == 'Player2':
                self.player.input_player()
                self.player2.input_player()
            elif self.player_mode == 'AI':
                self.bot.update(self.ball)

    def update(self):
        if self.current_state == 'playing':
            self.ball.update()
            # Colisão com jogadores/bot
            if self.player_mode == 'Player1':
                if self.ball.rect.colliderect(self.player.rect):
                    self.ball.VPos_y *= -1
            elif self.player_mode == 'Player2':
                if self.ball.rect.colliderect(self.player.rect):
                    self.ball.VPos_y *= -1
                if self.ball.rect.colliderect(self.player2.rect):
                    self.ball.VPos_y *= -1
            elif self.player_mode == 'AI':
                if self.ball.rect.colliderect(self.bot.rect):
                    self.ball.VPos_y *= -1
            # Colisão com blocos
            for idx, bloco in enumerate(self.blocks.lis_blocks):
                if self.ball.rect.colliderect(bloco):
                    self.ball.VPos_y *= -1
                    self.blocks.animated_rect_collision(idx)
                    self.blocks.lis_blocks.pop(idx)
                    self.points.update_points()
                    self.points.update_best_pontuation()
                    break
            # Fim de nível
            if not self.blocks.lis_blocks:
                self.blocks.reset()
                self.points.update_level()
            # Game over (bola caiu)
            if self.ball.y + self.ball.raio >= self.rect_manager.height - self.ball.relative_ball_pos:
                self.current_state = 'pre_runing'
                self.ball.reset()
                self.player.reset()
                self.player2.reset()
                self.bot.reset_bot()
                self.points.reset_points_and_levels()

    def render(self):
        if self.current_state == 'menu':
            self.rect_manager.render_menu()
        elif self.current_state == 'pre_runing':
            self.rect_manager.render_pre_runing()
        elif self.current_state == 'playing':
            self.rect_manager.clear_bg_screen()
            self.rect_manager.draw_border()
            self.blocks.draw()
            self.ball.draw()
            if self.player_mode == 'Player1':
                self.player.draw()
            elif self.player_mode == 'Player2':
                self.player.draw()
                self.player2.draw()
            elif self.player_mode == 'AI':
                self.bot.draw_bot()
            self.points.draw_level(self.rect_manager)
            self.points.draw_pontuation(self.rect_manager)
            self.points.draw_best_pontuation(self.rect_manager)

    def start_game(self):
        self.current_state = 'playing'
        self.ball.reset()
        self.ball.start_movement()
        self.player.reset()
        self.player2.reset()
        self.bot.reset_bot()
        self.points.reset_points_and_levels()
