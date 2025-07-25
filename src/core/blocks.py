
import pygame
import numpy as np

class Blocks:
    def __init__(self, game_base):
        self.game_base = game_base
        self._largura_bloco = 57
        self._altura_bloco = 20
        self.cor_blocos = (150, 80, 35)
        self.cor_animacao = (127, 127, 127)
        self.cor_animacao_none = (127, 127, 127)
        #self.rand_color = np.random.randint(10, 255, size=3)
        self.level_blocks = 0
        self._espaco_blocos = 17
        self.lis_blocos = []
        self.num_blocos_por_fileira = 0
        self.num_colunas = 0
        self.fileira_init = 0
        self.coluna_init = 0
        self.niveis = {
            0: (8,3),  # nível 1: (n_row, n_columns)
            1: (8,4),  # nível 2
            2: (8,4),  # nível 3
            3: (8,5),  # nível 4
            4: (8,5),  # nível 5
            5: (8,6),  # nível 6
            6: (8,6),  # nível 7
            7: (8,7),  # nível 8 
            8: (8,7),  # nível 9
            9: (8,8)  # nível 10
        }
        self.criar_blocos()

    @property
    def espaco_blocos(self) -> int:
        """Permite eu reescrever seu valor retornado em um @property.setter"""
        return self._espaco_blocos
    
    @property
    def largura_bloco(self) -> int:
        """Permite eu reescrever seu valor retornado em um @property.setter"""
        return self._largura_bloco
    
    @property
    def altura_bloco(self) -> int:
        """Permite eu reescrever seu valor retornado em um @property.setter"""
        return self._altura_bloco

    @espaco_blocos.setter
    def dimensionamento_espaco_blocos(self, novo_valor:int):
        self._espaco_blocos = novo_valor
        self.lis_blocos.clear()
        self.criar_blocos()  

    @largura_bloco.setter
    def dimensionamento_largura_bloco(self, novo_valor:int):
        self._largura_bloco = novo_valor
        self.lis_blocos.clear()
        self.criar_blocos()  
    
    @altura_bloco.setter
    def dimensionamento_altura_bloco(self, novo_valor:int):
        self._altura_bloco = novo_valor
        self.lis_blocos.clear()
        self.criar_blocos()

    def criar_blocos(self):

        row, column = self.niveis[self.level_blocks]

        for fileira in range(row):
            for coluna in range(column):
                x = self._espaco_blocos + fileira * (self._largura_bloco + self._espaco_blocos)
                y = self._espaco_blocos + coluna * (self._altura_bloco + self._espaco_blocos)
                self.bloco_Rect = pygame.Rect(x, y, self._largura_bloco, self._altura_bloco)
                self.lis_blocos.append(self.bloco_Rect)

    def desenhar_blocos(self):
        #self.rand_color = np.random.randint(10, 255, size=3) # Colocando a instância aqui só para ficar engraçado kkkk
        for bloco in self.lis_blocos:
            pygame.draw.rect(self.game_base.screen, self.cor_blocos, bloco, width=0, border_radius=3)
            
    def animacao_blocos(self, index:int):
        for indice, bloco in enumerate(self.lis_blocos):
            if indice == index:
                bloco_antigo = bloco.copy()
                bloco_novo = bloco_antigo.copy()
                bloco_antigo.inflate_ip(1.0, 1.3)
                pygame.draw.rect(self.game_base.screen, self.cor_animacao, bloco_antigo, width=0, border_radius=3)
                pygame.draw.rect(self.game_base.screen, self.cor_animacao_none, bloco_novo, width=5, border_radius=2)

    def resetar_blocos(self):
        self.lis_blocos.clear()
        self.num_blocos_por_fileira = self.fileira_init  # Reatribui o estado inicial
        self.num_colunas = self.coluna_init  # Reatribui o estado inicial
        self.criar_blocos()
