

import random
# import csv
# import os

import pygame


# from data.bot_ia import ColetaDados

class Ball:
    def __init__(self, game_base: object):
        self.game_base = game_base
        # self.coleta = ColetaDados()
        #self.vetor = Vector2()
        self.angle = 0.0
        self.vf_x = 0.0
        self.vf_y = 0.0
        self.x = 300
        self.y = 350
        self.VPos_x = 0.0
        self.VPos_y = 0.0
        self.raio = 5
        self.bola_Rect = pygame.Rect(self.x - self.raio, self.y - self.raio, self.raio, self.raio)

    def desenho_bola(self):
        pygame.draw.circle(self.game_base.screen, (255, 255, 255), (self.x, self.y), self.raio)

    def iniciar_movimento(self):
        self.VPos_x = random.uniform(-3.0, 3.0)  # random.uniform(-3.0,3.0)
        self.VPos_y = random.uniform(-2.0, -2.5)  # random.uniform(-2.0,-2.5)

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

        # self.registrar_dados()

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

        # self.registrar_dados()

    """ def registrar_dados(self):
        self.angle = self.vetor.angle_to([self.VPos_x, self.VPos_y])
        self.angle = round(self.angle, 2)
        self.coleta.coletar_dados(pos_x=self.x, pos_y=self.y, ang=self.angle)
        self.coleta.salva_dados()
        
        self.coleta.salva_dados() """

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
