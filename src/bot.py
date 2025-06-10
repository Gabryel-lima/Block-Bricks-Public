import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Desativa mensagens de aviso do TensorFlow
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Desativa as operações customizadas do oneDNN para evitar mensagens de aviso

import tensorflow as tf
tf.get_logger().setLevel('ERROR')  # Desativa mensagens de log do TensorFlow

from src.imports import pygame
import numpy as np
import keras
from src.player_base import PlayerBase

class Bot(PlayerBase):
    def __init__(self, game):
        super().__init__(game)
        self.game = game 
        # self._pos_x = 280
        # self._pos_y = 402
        # self.width_draw_x = 42
        # self.height_draw_y = 5
        # self.rect = pygame.Rect(self._pos_x, self._pos_y, self.width_draw_x, self.height_draw_y)
        # self.border = self.game.rect_manager.enum_rects.SCREEN_BORDER.value
        self.model = None
        self.load_weights()
    
    def _player_collision(self):
        return super()._player_collision()

    def load_weights(self):
        """
        Verifica se o arquivo do modelo existe e carrega os pesos.
        Caso contrário, exibe uma mensagem de erro.
        """
        model_path = 'src/model/best_model.keras'

        if os.path.exists(model_path):
            self.model = keras.models.load_model(model_path)
            print(f"Modelo carregado path={model_path}")
        else:
            print(f"Modelo não encontrado no caminho: {model_path}")
            self.model = None
    
    def draw_bot(self):
        pygame.draw.rect(
            self.game.rect_manager.screen,
            (20, 155, 40),
            (self.x, self.y, self.width, self.height)
        )
        
    def reset_bot(self):
        self.x = self.border.width / 2
    
    def move_left(self):
        self.x -= 5.0
    
    def move_right(self):
        self.x += 5.0
    
    def fine_adjustment(self, distance_to_ball):
        if abs(distance_to_ball) < 30:
            if distance_to_ball < 0:
                self.x -= 3.0
            elif distance_to_ball > 0:
                self.x += 3.0
    
    def update(self):
        # Obtém a observação atual do estado do jogo
        state = self.get_observation()
        
        # Usa o modelo para prever a ação
        action_values = self.model.predict(np.expand_dims(state, axis=0))
        action = np.argmax(action_values[0])
        
        # Calcula a distância até a bola
        distance_to_ball = self.calculate_distance_to_ball()
        
        # Executa a ação correspondente
        if action == 0:
            self.move_right()
        elif action == 1:
            self.move_left()
        elif action == 2:
            self.fine_adjustment(distance_to_ball)

        self._player_collision()
    
    def get_observation(self):
        obs = np.array(pygame.surfarray.array3d(self.game.screen_surface), dtype=np.float32) 
        obs /= 255.0  # Normaliza a observação para o intervalo [0, 1]
        return obs
    
    def calculate_distance_to_ball(self):
        # Implementa o cálculo da distância entre o jogador e a bola
        ball_center = self.game.ball.rect.centerx
        player_center = self.rect.centerx
        distance = ball_center - player_center
        return distance
    
    def clear_rect(self):
        self.rect.update(0, 0, 0, 0)

    # def __str__(self):
    #     return f"Bot(pos_x={self._pos_x}, pos_y={self._pos_y}, width={self.width_draw_x}, height={self.height_draw_y})"

    # def __repr__(self):
    #     return f"Bot(game={self.game}, pos_x={self._pos_x}, pos_y={self._pos_y})"

    # def move_left(self, distance_to_ball):
    #     # Distância é negativa se a bola estiver à esquerda
    #     speed_factor = min(max(abs(distance_to_ball) / 10, 5.0), 20.0)
    #     self.pos_x -= speed_factor

    # def move_right(self, distance_to_ball):
    #     # Distância é positiva se a bola estiver à direita
    #     speed_factor = min(max(abs(distance_to_ball) / 10, 5.0), 20.0)
    #     self.pos_x += speed_factor

    # def fine_adjustment(self, distance_to_ball):
    #     if abs(distance_to_ball) < 25:
    #         if distance_to_ball < 0:
    #             self.pos_x -= 3.0  # Ajuste fino para esquerda
    #         elif distance_to_ball > 0:
    #             self.pos_x += 3.0  # Ajuste fino para direita

    # def stop(self):
    #     self.pos_x *= 1.0

    # def move_left(self, distance_to_ball):
    #     if abs(distance_to_ball) > 24:
    #         self.pos_x -= 9.0
    #     else:
    #         self.pos_x -= 5.0

    # def move_right(self, distance_to_ball):
    #     if abs(distance_to_ball) > 24:
    #         self.pos_x += 9.0
    #     else:
    #         self.pos_x += 5.0

    # def fine_adjustment(self, distance_to_ball):
    #     if abs(distance_to_ball) < 25:
    #         if distance_to_ball < 0:
    #             self.pos_x -= 3.0
    #         elif distance_to_ball > 0:
    #             self.pos_x += 3.0

    # def move_left(self):
    #     self.pos_x -= 5.0

    # def move_right(self):
    #     self.pos_x += 5.0

    # def fine_adjustment(self, distance_to_ball):
    #     if abs(distance_to_ball) < 25:
    #         if distance_to_ball < 0:
    #             self.pos_x -= 3.0
    #         elif distance_to_ball > 0:
    #             self.pos_x += 3.0

    # def init_ball_movement(self):
    #     self.game.ball.iniciar_movimento()