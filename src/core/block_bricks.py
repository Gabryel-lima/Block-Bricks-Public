import pygame, json, random, os
from enum import Enum

from src.core.game_base import GameBase

from src.utils.utils import scaled_surface_percent, apenda_dot

from src.data.coleta_dados import count_reinits
from src.core.decorators import clock, bool_game_over
import numpy as np

PATH = os.path.abspath('.') + '/'

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
        self.loading_last_points = self.carregar_melhor_pontuacao()
        self.mens_bp = f'Best Points: {self.loading_last_points}'
        self.mens_game_over = f'Game over!'
        self.game_init = False
        self.current_game = 0

        # TODO: Melhorar este carinhas aqui em baixo ...
        self.channels = 3
        self.screen_surface = scaled_surface_percent(self.screen, percentage=10)
        self.window_size = (self.screen_surface.get_width(), self.screen_surface.get_height())
        self.sensor_line_data: np.ndarray = None

    def update_caption_with_fps(self):
        # Obtém o FPS atual e atualiza o título da janela
        fps = self.clock_game.get_fps()
        pygame.display.set_caption(f'Block-Bricks *1.8 - FPS: {fps:.1f}')

    def verify_height_ball(self):
        # pos_y lim 420.0
        if self.ball.y + self.ball.raio >= self.height - self.relative_height_ball:
            text_format = self.fonts.font_arial.render(f'{self.mens_game_over}',
                                                        False,  (127, 127, 127))
            self.screen.blit(text_format, self.mesg_fj_blit_xy)

            self.particao_verificar_colisao()

    def verificar_colisao(self):
        if self.ball.bola_Rect.colliderect(self.player.rect):
            self.ball.inverter_direcao()

        elif self.ball.bola_Rect.colliderect(self.player2.rect):
            self.ball.inverter_direcao()
        
        elif self.ball.bola_Rect.colliderect(self.bot.rect):
            self.ball.inverter_direcao_bot()

        self.verify_height_ball()
            
        for blocks in self.blocks.lis_blocos:
            if self.ball.bola_Rect.colliderect(blocks):
                self.invert_direction_ball_block()
                #self.sound_ball_and_blocks()
                self.blocks.animacao_blocos(index=self.blocks.lis_blocos.index(blocks))
                self.blocks.lis_blocos.remove(blocks)
                if self.player_mode == "Player1":
                    self.atualiza_pontuacao()
                    self.atualiza_melhor_pontuacao()
                elif self.player_mode == "Player2":
                    self.atualiza_pontuacao2()
                    self.update_best_pontuation_player2()
                elif self.player_mode == "AI":
                    pass

    def particao_verificar_colisao(self):
        #self.som_de_fim_de_jogo()
        pygame.display.flip()
        pygame.time.delay(3000)
        self.salvar_melhor_pontuacao()
        modo_selecionado = self.selecao_de_modos_estrutura()

        if modo_selecionado == self.executar_particao(particao=self.player.desenho_player):
            self.blocks.resetar_blocos()
            self.ball.reset()
            self.ball.iniciar_movimento()
            self.ball.atualizar()
            self.reset_pontos_and_levels()
            self.reset_pontos2()

        elif modo_selecionado == self.executar_particao(particao=self.player2.desenho_player):
            self.blocks.resetar_blocos()
            self.ball.reset()
            self.ball.iniciar_movimento()
            self.ball.atualizar()
            self.reset_pontos_and_levels()
            self.reset_pontos2()

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

    def carregar_melhor_pontuacao(self):
        try:
            with open('src/json/best_score.json', 'r') as file:
                data = json.load(file)
                return data['best_score']
        except (FileNotFoundError, KeyError):
            return 0
            
    def salvar_melhor_pontuacao(self):
        data = {'best_score': self.loading_last_points}
        with open('src/json/best_score.json', 'w') as file:
            json.dump(data, file)

    def atualiza_melhor_pontuacao(self):
        if self.init_points > self.loading_last_points:
            self.loading_last_points = self.init_points
            self.salvar_melhor_pontuacao()
            self.mens_bp = f'Best points: {self.loading_last_points}'

    def reset_pontos2(self):
        if self.mensagem_fim_de_nivel:
            self.mesg2 = f'Points: {self.init_points}'
        else:
            self.init_points = 0
            self.mesg2 = f'Points: {self.init_points}'

    def atualiza_pontuacao(self):
        self.init_points += 1
        self.mens_points_1_2 = f'Points: {self.init_points}'

    def reset_pontos_and_levels(self):
        if self.mensagem_fim_de_nivel:
            self.mens_points_1_2 = f'Points: {self.init_points}'
            self.mesg_nivel = f'Level: {self.level}'
        self.init_points = 0
        self.mens_points_1_2 = f'Points: {self.init_points}'
        self.blocks.level_blocks = 0
        self.mesg_nivel = f'Level: {self.blocks.level_blocks}'

    def reset(self): # Esse metodo retorna o menu.
        if self.width == 600:
            self.game_init = False
            self.ball.reset()
            self.player.reset()
            self.player2.reset()
            self.rect_botao_player1 = self.list_tela_inicial[0]
            self.rect_botao_player2 = self.list_tela_inicial[1]
            self.rect_botao_config = self.list_tela_config[7]

        elif self.width > 600:
            self.game_init = False
            self.rect_botao_player1 = self.list_tela_inicial[0]
            self.rect_botao_player2 = self.list_tela_inicial[1]
            self.rect_botao_config = self.list_tela_config[7]

    def exibir_pontuacao(self):
        mensagem = self.mens_points_1_2
        texto_formatado = self.fonts.font_candara.render(mensagem, False, (127,127,127))
        self.screen.blit(texto_formatado, self.blit_xy_mesg1_pontos)

    def exibe_melhor_pontuacao(self):
        mensagem = self.mens_bp
        texo_formatado = self.fonts.font_candara.render(mensagem, False, (127,127,127))
        self.screen.blit(texo_formatado, self.blit_xy_mesg_bp1)

    def exibir_nivel(self):
        mensagem = self.mens_level
        texto_formatado = self.fonts.font_candara.render(mensagem, False, (127, 127, 127))
        self.screen.blit(texto_formatado, self.blit_xy_exibe_nivel)

    def mensagem_fim_de_nivel(self):
        if len(self.blocks.lis_blocos) == 0:
            texto_formatado = self.fonts.font_arial.render(f'You win! {self.level}', True, (127, 127, 127))
            self.screen.blit(texto_formatado, self.mesg_fj_blit_xy)
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
            if self.ball.bola_Rect.colliderect(block):
                # Calcula as distâncias das bordas da bola em relação ao bloco
                dist_top: int = abs(self.ball.bola_Rect.bottom - block.top)
                dist_bottom: int = abs(self.ball.bola_Rect.top - block.bottom)
                dist_left: int = abs(self.ball.bola_Rect.right - block.left)
                dist_right: int = abs(self.ball.bola_Rect.left - block.right)
                
                # Verifica se a colisão é mais próxima dos lados vertical ou horizontal
                if min(dist_top, dist_bottom) < min(dist_left, dist_right):
                    # Colisão no topo ou na base do bloco, inverte o eixo Y
                    self.ball.VPos_y *= -1
                else:
                    # Colisão nos lados esquerdo ou direito do bloco, inverte o eixo X
                    self.ball.VPos_x *= -1
                    
    def layout(self):
        self.screen.fill((0, 0, 0))
        self.desenho_borda()
        self.botoes_tela_inicial_modos()
        self.selecao_de_modos_estrutura()
        
        if self.game_init:
            self.desenho_borda()
            self.ball.desenho_bola()
            self.blocks.desenhar_blocos()
            #self.new_sensor.draw_lines_sensor(self.screen)
            #self.sensor.draw_lines_sensor(self.screen)

            if self.player_mode == "Player1":
                self.player.desenho_player()

            elif self.player_mode == "Player2":
                self.player.desenho_player()
                self.player2.desenho_player()

            elif self.player_mode == "AI":
                self.bot.draw_bot()

    def reset_env(self): # Realmente tenho que ver que canário reseta o jogo todo
        self.screen.fill((0, 0, 0))
        self.ball.reset_with_custom()
        self.blocks.resetar_blocos()
        self.player.reset() # Ele parece generaizar melhor as experiencias retornando para o estado inicial
        self.ball.iniciar_movimento()
        #self.reset_pontos_and_levels() # Só por enquanto ...

    def render_frame(self):
        #self.clock_game.tick(120) # Mantém a o frame_hate como no jogo normal
 
        self.screen.fill((0, 0, 0))

        canvas = self.screen_surface

        self.desenho_borda()

        self.player2.rect = pygame.Rect(0, 0, 0, 0)

        self.ball.desenho_bola()
        self.blocks.desenhar_blocos()
        self.player.desenho_player()

        self.verificar_colisao()
        self.ball.atualizar()

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
                self.ball.atualizar()

                if self.player_mode == "Player1":
                    self.exibir_nivel()
                    self.exibe_melhor_pontuacao()
                    self.exibir_pontuacao()
                    self.player.player_collision()
                    self.player.input_player()

                elif self.player_mode == "Player2":
                    self.exibir_nivel()
                    self.exibe_melhor_pontuacao2()
                    self.exibir_pontuacao2()
                    self.player.player_collision()
                    self.player.input_player()
                    self.player2.player_collision()
                    self.player2.input_player2()

                elif self.player_mode == "AI":
                    #self.clock_game.tick(120) # Mantém a o frame_hate como no jogo normal
                    self.exibir_nivel()
                    self.exibe_melhor_pontuacao()
                    self.exibir_pontuacao()
                    self.bot.bot_collision()
                    self.bot.update()

            self.mensagem_fim_de_nivel()
            pygame.display.update()
            #return pygame.surfarray.array3d(self.screen)

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

