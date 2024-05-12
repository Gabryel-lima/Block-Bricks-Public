

import random
# import csv
# import os

import pygame


from src.data.coleta_dados import ColetaDados

class Ball:
    def __init__(self, game_base):
        self.game_base = game_base
        self.coleta = ColetaDados(game_base=self.game_base)
        self.x = 300
        self.y = 350
        self.VPos_x = 0.0
        self.VPos_y = 0.0
        self.raio = 5
        self._left = float(self.x - self.raio)
        self._top = float(self.y - self.raio)
        self.bola_Rect = pygame.Rect(self._left, self._top, self.raio, self.raio)

    def desenho_bola(self):
        pygame.draw.circle(self.game_base.screen, (255, 255, 255), (self.x, self.y), self.raio)
    
    def iniciar_movimento(self):
        self.VPos_x = random.uniform(-3.0,3.0)  # random.uniform(-3.0,3.0)
        self.VPos_y = random.uniform(-2.0,-2.0)  # random.uniform(-2.0,-2.0)

    def _save_data(self):
        angle_xp = self.coleta._data_angle_ball_x_to_player_x(ball_rect_x=self.bola_Rect.centerx, player_rect_x=self.game_base.player.rect.centerx)
        angle_yp = self.coleta._data_angle_ball_y_to_player_y(ball_rect_y=self.bola_Rect.centery, player_rect_y=self.game_base.player.rect.centery)
        magnitude = self.coleta._data_magnitude_ball_to_critic_zone(ball_rect_x=self.bola_Rect.centerx, ball_rect_y=self.bola_Rect.centery)
        distance = self.coleta._data_ball_distance_to_player(ball_rect_centerx=self.bola_Rect.centerx, player_rect_centerx=self.game_base.player.rect.centerx)
        count_reinits = self.coleta._recebe_count_reinits_decorator()
        level = self.coleta._recebe_nivel()
        points = self.coleta._recebe_points()
        self.coleta.coletar_dados(ang_ball_centerx_to_player_centerx=angle_xp, 
                                  ang_ball_y_to_player_centery=angle_yp,
                                  magnitude_ball_center_xy=magnitude,
                                  distance_ball_centerx_to_player_centerx=distance,
                                  count_reinits=count_reinits,
                                  level=level,
                                  points=points)
        self.coleta.salvar_dados()

    def atualizar(self):
        self.x += self.VPos_x
        self.y += self.VPos_y
        self.bola_Rect.center = (self.x, self.y)

        if self.x - self.raio <= 0 or self.x + self.raio >= self.game_base.width:  # Responsável pelo rebauce da border
            self.VPos_x *= -1

            self.VPos_x /= 1  # Adicionei para resetar a atualização constante ao tocar na border

        if self.y - self.raio <= 0 or self.y + self.raio >= self.game_base.height:  # Responsável pelo rebauce da border
            self.VPos_y *= -1

            self.VPos_y /= 1  # Adicionei para resetar a atualização constante ao tocar na border

        #self._save_data()

    def inverter_direcao(self):
        if pygame.key.get_pressed()[pygame.constants.K_a]:
            self.VPos_x -= 0.7
            self.VPos_y /= -1
        elif pygame.key.get_pressed()[pygame.constants.K_d]:
            self.VPos_x += 0.7
            self.VPos_y /= -1
        else:
            self.VPos_x *= 1
            self.VPos_y *= -1

    def inverter_direcao2(self):
        if pygame.key.get_pressed()[pygame.constants.K_LEFT]:
            self.VPos_x -= 0.7
            self.VPos_y /= -1
        elif pygame.key.get_pressed()[pygame.constants.K_RIGHT]:
            self.VPos_x += 0.7
            self.VPos_y /= -1
        else:
            self.VPos_x *= 1
            self.VPos_y *= -1

    def reset(self):
        self.x = 300
        self.y = 350
        self.VPos_x = 0.0
        self.VPos_y = 0.0
        self.bola_Rect.center = (self.x, self.y)

    def animacao_menu(self):
        self.desenho_bola()
        self.atualizar()
