import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Desativa mensagens de aviso do TensorFlow
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Desativa as operações customizadas do oneDNN para evitar mensagens de aviso

import tensorflow as tf
tf.get_logger().setLevel('ERROR')  # Desativa mensagens de log do TensorFlow

from .imports import pygame
import numpy as np
import keras

class Bot:
    def __init__(self, game_base):
        self.game_base = game_base 
        self._pos_x = 280
        self._pos_y = 402
        self.width_draw_x = 40
        self.height_draw_y = 1
        self.rect = pygame.Rect(self._pos_x, self._pos_y, self.width_draw_x, self.height_draw_y)
        self.model = None
        self.load_weights()
    
    @property
    def pos_x(self):
        return self._pos_x

    @property
    def pos_y(self):
        return self._pos_y
    
    @pos_x.setter
    def pos_x(self, value):
        """Limita o valor de pos_x para evitar ultrapassar as bordas"""
        if value < self.game_base.border.left:
            value = self.game_base.border.left
        elif value + self.width_draw_x > self.game_base.border.right:
            value = self.game_base.border.right - self.width_draw_x
        
        self._pos_x = value
        self.rect.x = self._pos_x

    def load_weights(self):
        """
        Verifica se o arquivo do modelo existe e carrega os pesos.
        Caso contrário, exibe uma mensagem de erro.
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        model_path = os.path.join(base_dir, 'best_model.keras')

        if os.path.exists(model_path):
            self.model = keras.models.load_model(model_path)
            print(f"Modelo carregado dir={base_dir} path={model_path}")
        else:
            print(f"Modelo não encontrado no caminho: {model_path}")
            self.model = None
    
    def draw_bot(self):
        pygame.draw.rect(self.game_base.screen, (20, 155, 40),
                         (self._pos_x, self._pos_y, self.width_draw_x, 5))
        
    def reset_bot(self):
        self.pos_x = self.game_base.width / 2
    
    def move_left(self):
        self.pos_x -= 5.0
    
    def move_right(self):
        self.pos_x += 5.0
    
    def fine_adjustment(self, distance_to_ball):
        if abs(distance_to_ball) < 25:
            if distance_to_ball < 0:
                self.pos_x -= 3.0
            elif distance_to_ball > 0:
                self.pos_x += 3.0
    
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
    
    def get_observation(self):
        obs = np.array(pygame.surfarray.array3d(self.game_base.screen_surface), dtype=np.float32) 
        obs /= 255.0  # Normaliza a observação para o intervalo [0, 1]
        return obs
    
    def calculate_distance_to_ball(self):
        # Implementa o cálculo da distância entre o jogador e a bola
        ball_center = self.game_base.ball.bola_Rect.centerx
        player_center = self.rect.centerx
        distance = ball_center - player_center
        return distance
    
    def clear_rect(self):
        self.rect.update(0, 0, 0, 0)

    def __str__(self):
        return f"Bot(pos_x={self._pos_x}, pos_y={self._pos_y}, width={self.width_draw_x}, height={self.height_draw_y})"

    def __repr__(self):
        return f"Bot(game_base={self.game_base}, pos_x={self._pos_x}, pos_y={self._pos_y})"

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
    #     self.game_base.ball.iniciar_movimento()