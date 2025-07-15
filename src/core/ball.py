
import pygame, random
#from src.data.coleta_dados import ColetaDados
import numpy as np

class Ball:
    def __init__(self, game_base):
        self.game_base = game_base
        #self.coleta = ColetaDados(game_base=self.game_base)
        self.x = 300
        self.y = 150 # 350
        self.VPos_x = 0
        self.VPos_y = 0
        # self.acceleration = 0.2  # Valor de aceleração
        # self.max_speed = 3.8  # Velocidade máxima permitida
        self.raio = 5
        self._left = float(self.x - self.raio)
        self._top = float(self.y - self.raio)
        self.bola_Rect = pygame.Rect(self._left, self._top, self.raio, self.raio)
        self.rand_color = np.random.randint(50, 255, size=3)
        #self.iniciar_movimento() # Estranho demais

    @property
    def get_center_array(self) -> np.ndarray:
        return np.array(self.bola_Rect.center, dtype=np.float32)

    @property
    def get_pos_center_y(self) -> int:
        return self.bola_Rect.centery
    
    @get_pos_center_y.setter
    def set_pos_center_y(self, novo_valor: int):
        self.bola_Rect.centery = novo_valor

    @property
    def get_pos_x(self) -> int:
        return self.x

    @get_pos_x.setter
    def set_x(self, novo_valor: int):
        self.x = novo_valor
        self.bola_Rect.x = novo_valor

    @property
    def get_pos_y(self) -> int:
        return self.y

    @get_pos_y.setter
    def set_pos_y(self, novo_valor: int):
        self.y = novo_valor
        self.bola_Rect.y = novo_valor

    def desenho_bola(self):                       # self.rand_color[:3]
        pygame.draw.circle(self.game_base.screen, self.rand_color[:3], self.bola_Rect.center, self.raio)
    
    def iniciar_movimento(self):
        self.VPos_x = random.uniform(-3.0, 3.0)
        self.VPos_y = random.uniform(2.0, 2.0)

    def atualizar(self):
        self.x += int(self.VPos_x)
        self.y += int(self.VPos_y)
        self.bola_Rect.center = (self.x, self.y)

        # Rebote nas bordas
        if self.x - self.raio <= 0 or self.x + self.raio >= self.game_base.border.width:
            self.VPos_x *= -1

        if self.y - self.raio <= 0 or self.y + self.raio >= self.game_base.border.height:
            self.VPos_y *= -1

    def inverter_direcao(self):
        if self.bola_Rect.centerx <= self.game_base.player.rect.centerx:
            self.VPos_x -= 1
            self.VPos_y *= -1
        elif self.bola_Rect.centerx >= self.game_base.player.rect.centerx:
            self.VPos_x += 1
            self.VPos_y *= -1
        else:
            self.VPos_x *= 1
            self.VPos_y *= -1

    def inverter_direcao_bot(self):
        if self.bola_Rect.centerx <= self.game_base.bot.rect.centerx:
            self.VPos_x -= 1
            self.VPos_y *= -1
        elif self.bola_Rect.centerx >= self.game_base.bot.rect.centerx:
            self.VPos_x += 1
            self.VPos_y *= -1
        else:
            self.VPos_x *= 1
            self.VPos_y *= -1

    def reset(self):
        self.x = 300
        self.y = 150
        self.VPos_x = int()
        self.VPos_y = int()
        self.bola_Rect.center = (300, 150)

    def reset_with_custom(self):
        self.x = 300
        self.y = 150
        self.VPos_x = 0
        self.VPos_y = 0
        self.bola_Rect.center = (300, 150)

    def animacao_menu(self):
        self.desenho_bola()
        self.atualizar()
