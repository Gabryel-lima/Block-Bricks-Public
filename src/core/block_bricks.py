from src.core.imports import pygame, json, os

from src.core.game_base import GameBase

from src.utils.utils import scaled_surface_percent, apenda_dot

from src.data.coleta_dados import count_reinits
from src.core.decorators import clock, bool_game_over
import numpy as np

from paths import PATH


class Game(GameBase):
    def __init__(self):
        super().__init__()
        # self.moving_sprites = pygame.sprite.Group()
        # self.moving_sprites.add(self.blocks)
        self.clock_game = pygame.time.Clock()
        self.icon = pygame.image.load(PATH + '/assets/logo.ico').convert_alpha()
        pygame.display.set_caption('Block-Bricks *2.0')
        pygame.display.set_icon(self.icon)
        #self.sound_collision = pygame.mixer.Sound('sounds/encosta_bloco.wav')
        #self.sound_game_over = pygame.mixer.Sound('sounds/som_de_fim.wav')
        #self.sound_over_level = pygame.mixer.Sound('sounds/som_fim_nivel.wav')
        # self.loading_last_points = self.carregar_melhor_pontuacao()
        # self.mens_bp = f'Best Points: {self.loading_last_points}'
        # self.mens_game_over = f'Game over!'
        # self.game_init = False
        # self.current_game = 0

        # TODO: Melhorar este carinhas aqui em baixo ...
        self.channels = 3
        self.screen_surface = scaled_surface_percent(self.rect_manager.screen, percentage=10)
        self.window_size = (self.screen_surface.get_width(), self.screen_surface.get_height())

    def update_caption_with_fps(self):
        # Obtém o FPS atual e atualiza o título da janela
        fps = self.clock_game.get_fps()
        pygame.display.set_caption(f'Block-Bricks 2.0 - FPS: {fps:.1f}')

    def verify_height_ball(self):
        # pos_y lim 420.0
        if self.ball.y + self.ball.raio >= self.rect_manager.screen.get_height() - self.ball.relative_ball_pos:
            text_format = self.fonts.font_arial.render(f'{self.text.over}',
                                                        False,  (127, 127, 127))
            self.rect_manager.screen.blit(text_format, self.rect_manager.rects.get("blit_text_game_over"))

            self.particao_verificar_colisao()

    def verificar_colisao(self):
        if self.ball.rect.colliderect(self.player.rect):
            self.ball.invert_direction(player=self.player.rect)

        elif self.ball.rect.colliderect(self.player2.rect):
            self.ball.invert_direction(player=self.player2.rect)
        
        elif self.ball.rect.colliderect(self.bot.rect):
            self.ball.invert_direction(player=self.bot.rect)

        self.verify_height_ball()
            
        for blocks in self.blocks.lis_blocos:
            if self.ball.rect.colliderect(blocks):
                self.invert_direction_ball_block()
                #self.sound_ball_and_blocks()
                self.blocks.animacao_blocos(index=self.blocks.lis_blocos.index(blocks))
                self.blocks.lis_blocos.remove(blocks)
                if self.player_mode == "Player1":
                    self.points.update_points()
                    self.points.update_best_pontuation_player1()
                elif self.player_mode == "Player2":
                    self.points.update_points()
                    self.points.update_best_pontuation_player2()
                elif self.player_mode == "AI":
                    pass

    def particao_verificar_colisao(self):
        #self.som_de_fim_de_jogo()
        pygame.display.flip()
        pygame.time.delay(3000)
        self.points._save_best_pontuation(file_path="../json/")
        modo_selecionado = self.selecao_de_modos_estrutura()

        if modo_selecionado == self.executar_particao(particao=self.player.desenho_player):
            self.blocks.resetar_blocos()
            self.ball.reset()
            self.ball.start_movement()
            self.ball.update()
            self.points.reset_points_and_levels()
            #self.points.reset_points()

        elif modo_selecionado == self.executar_particao(particao=self.player2.desenho_player):
            self.blocks.resetar_blocos()
            self.ball.reset()
            self.ball.start_movement()
            self.ball.update()
            self.points.reset_points_and_levels()
            #self.points.reset_points()

        elif modo_selecionado == self.executar_particao(particao=self.bot.draw_bot):
            self.reset_env()

    def sound_ball_and_blocks(self):
        sound = self.sound_collision
        sound.set_volume(0.30)
        sound.play()

    def som_de_fim_de_jogo(self):
        sound = self.sound_game_over
        sound.set_volume(0.30)
        sound.play()

    def som_de_fim_de_nivel(self):
        sound = self.sound_over_level
        sound.set_volume(0.30)
        sound.play()

    def reset(self): # Esse metodo retorna o menu.
        self.game_init = False

        if self.rect_manager.screen.get_width() == 600:
            self.ball.reset()
            self.player.reset()
            self.player2.reset()
            self.rect_manager.rects.update(self.rect_manager.get_rect("button_player1"))
            self.rect_manager.rects.update(self.rect_manager.get_rect("button_player2"))
            self.rect_manager.rects.update(self.rect_manager.get_rect("button_bot"))
            self.rect_manager.rects.update(self.rect_manager.get_rect("button_config")) # TODO: Ainda falta configurar o botão de config

        elif self.rect_manager.screen.get_width() > 600:
            self.rect_manager.rects.update(self.rect_manager.get_rect("button_player1"))
            self.rect_manager.rects.update(self.rect_manager.get_rect("button_player2"))
            self.rect_manager.rects.update(self.rect_manager.get_rect("button_bot"))
            self.rect_manager.rects.update(self.rect_manager.get_rect("button_config")) # TODO: Ainda falta configurar o botão de config

    def mensagem_fim_de_nivel(self):
        if len(self.blocks.lis_blocos) == 0:
            texto_formatado = self.fonts.font_arial.render(f'{self.text.win} {self.blocks.level_blocks}', True, (self.color.GRAY))
            self.rect_manager.screen.blit(texto_formatado, self.rect_manager.rects.get("blit_text_game_over"))
            self.niveis_count()
            #self.som_de_fim_de_nivel()
            pygame.display.flip()
            pygame.time.delay(3000)
            self.blocks.resetar_blocos()
            self.ball.reset()
            self.continuar_prox_nivel()

    def colision_player_player2(self):
        if self.player.rect.colliderect(self.player2.rect) and pygame.key.get_pressed()[pygame.constants.K_d]:
            self.player.pos_x -= 3.5
            if pygame.key.get_pressed()[pygame.constants.K_LSHIFT]:
                self.player.pos_x -= 4.5
        
        if self.player2.rect.colliderect(self.player.rect) and pygame.key.get_pressed()[pygame.constants.K_LEFT]:
            self.player2.pos_x += 3.5
            if pygame.key.get_pressed()[pygame.constants.K_RSHIFT]:
                self.player2.pos_x += 4.5

    def invert_direction_ball_block(self):
        for block in self.blocks.lis_blocos:
            if self.ball.rect.colliderect(block):
                # Calcula as distâncias das bordas da bola em relação ao bloco
                dist_top: int = abs(self.ball.rect.bottom - block.top)
                dist_bottom: int = abs(self.ball.rect.top - block.bottom)
                dist_left: int = abs(self.ball.rect.right - block.left)
                dist_right: int = abs(self.ball.rect.left - block.right)
                
                # Verifica se a colisão é mais próxima dos lados vertical ou horizontal
                if min(dist_top, dist_bottom) < min(dist_left, dist_right):
                    # Colisão no topo ou na base do bloco, inverte o eixo Y
                    self.ball.VPos_y *= -1
                else:
                    # Colisão nos lados esquerdo ou direito do bloco, inverte o eixo X
                    self.ball.VPos_x *= -1
                    
    def layout(self):
        self.rect_manager.screen.fill((0, 0, 0))
        self.draw_manager.desenho_borda()
        self.draw_manager.botoes_tela_inicial_modos()
        self.selecao_de_modos_estrutura()
        
        if self.game_init:
            self.draw_manager.desenho_borda()
            self.ball.draw()
            self.blocks.desenhar_blocos()

            if self.player_mode == "Player1":
                self.player.desenho_player()

            elif self.player_mode == "Player2":
                self.player.desenho_player()
                self.player2.desenho_player()

            elif self.player_mode == "AI":
                self.bot.draw_bot()

    def reset_env(self): # Realmente tenho que ver que canário reseta o jogo todo
        # TODO: Tem muita coisa bagunçada aqui ainda
        self.rect_manager.screen.fill((0, 0, 0))
        self.ball.reset()
        self.blocks.resetar_blocos()
        self.player.reset()
        self.ball.start_movement()
        self.points.reset_points_and_levels() # Só por enquanto ...

    def render_frame(self):
        #self.clock_game.tick(120) # Mantém a o frame_hate como no jogo normal TODO: Ainda não impacta diretamente no treinamento do agente, devo ajustar também.
 
        self.rect_manager.screen.fill((0, 0, 0))

        canvas = self.screen_surface

        self.draw_manager.desenho_borda()

        self.player2.rect = pygame.Rect(0, 0, 0, 0)

        self.ball.draw()
        self.blocks.desenhar_blocos()
        self.player.desenho_player()

        self.verificar_colisao()
        self.ball.update()

        self.player.player_collision()
        pygame.display.flip()

        return np.array(pygame.surfarray.array3d(canvas), dtype=np.float32)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.constants.QUIT:
                    pygame.quit()

            self.clock_game.tick(60)
            self.update_caption_with_fps()
            self.layout()

            # self.moving_sprites.update() # Tálvez usar sprite no futuro...

            if self.game_init:
                self.verificar_colisao()
                self.colision_player_player2()
                self.ball.update()

                if self.player_mode == "Player1":
                    self.text.draw_level()
                    self.text.draw_pontuation()
                    self.text.draw_best_pontuation()
                    self.player.player_collision()
                    self.player.input_player()

                elif self.player_mode == "Player2":
                    self.text.draw_level()
                    self.text.draw_best_pontuation2()
                    self.text.exibir_pontuacao2()
                    self.player.player_collision()
                    self.player.input_player()
                    self.player2.player_collision()
                    self.player2.input_player2()

                elif self.player_mode == "AI":
                    #self.clock_game.tick(120) # Mantém a o frame_hate como no jogo normal TODO: Ou deveria kkkk
                    self.text.draw_level()
                    self.text.draw_best_pontuation_bot()
                    self.text.draw_pontuation()
                    #self.bot.bot_collision()
                    self.bot.update()

            self.mensagem_fim_de_nivel()
            pygame.display.update()
            #return pygame.surfarray.array3d(self.rect_manager.screen)

""" Mensage_box exemple: """

# import random

# answer = pygame.display.message_box(
#     "I will open two windows! Continue?",
#     "Hello!",
#     message_type="info",
#     buttons=("Yes", "No", "Chance"),
#     return_button=0,
#     escape_button=1,
# )

# if answer == 1 or (answer == 2 and random.random() < 0.5):
#     import sys

#     sys.exit(0)

