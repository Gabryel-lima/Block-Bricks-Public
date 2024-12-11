from src.core.imports import pygame

from src.core.player_base import PlayerBase

class Player(PlayerBase):
    def __init__(self, game_base):
        super().__init__(game_base)

    def desenho_player(self):
        pygame.draw.rect(self.game_base.rect_manager.screen, (255, 5, 5),
                         ((self.pos_x), (self.pos_y), self.width_draw_x, 5))

    def input_player(self):
        novo_x = self.pos_x
        if pygame.key.get_pressed()[pygame.constants.K_a]:
            novo_x -= 3.5

            if pygame.key.get_pressed()[pygame.constants.K_LSHIFT]:
                novo_x -= 4.5

        if pygame.key.get_pressed()[pygame.constants.K_d]:
            novo_x += 3.5

            if pygame.key.get_pressed()[pygame.constants.K_LSHIFT]:
                novo_x += 4.5

        self.pos_x = novo_x

    def resetp_1(self):
        self.pos_x = self.game_base.width / 2

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
