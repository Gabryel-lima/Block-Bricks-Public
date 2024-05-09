

import pygame


class Blocks(pygame.sprite.Sprite):
    def __init__(self, game_base):
        super().__init__()
        self.game_base = game_base
        self._largura_bloco = 57
        self._altura_bloco = 20
        self.cor_blocos = (150, 75, 0)
        self.cor_animacao = (250, 250, 250)
        self.cor_animacao_none = (150, 150, 100)
        self.nivel_atual = 0
        self._espaco_blocos = 16
        self.lis_blocos = []
        self.niveis = [
            (8,3),  # nível 1: (num_blocos_por_fileira, num_colunas)
            (8,4),  # nível 2
            (8,4),  # nível 3
            (8,5),  # nível 4
            (8,5),  # nível 5
            (8,6),  # nível 6
            (8,6),  # nível 7
            (8,7),  # nível 8
            (8,7),  # nível 9
            (8,8)  # nível 10
        ]
        self.configurar_nivel()

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
        for fileira in range(self.num_blocos_por_fileira):
            for coluna in range(self.num_colunas):
                x = self._espaco_blocos + coluna * (self._largura_bloco + self._espaco_blocos)
                y = self._espaco_blocos + fileira * (self._altura_bloco + self._espaco_blocos)
                self.bloco_Rect = pygame.Rect(x, y, self._largura_bloco, self._altura_bloco)
                self.lis_blocos.append(self.bloco_Rect)

    def desenhar_blocos(self):
        for bloco in self.lis_blocos:
            pygame.draw.rect(self.game_base.screen, self.cor_blocos, bloco, width=0, border_radius=3) #self.game_base.screen.blit(self.bloco_img, bloco)
            
    def animacao_blocos(self, index=int):
        for indice, bloco in enumerate(self.lis_blocos):
            if indice == index:
                bloco_antigo = bloco.copy()
                bloco_novo = bloco_antigo.copy()
                bloco_antigo.scale_by_ip(1.0, 1.3)
                pygame.draw.rect(self.game_base.screen, self.cor_animacao, bloco_antigo, width=0, border_radius=3)
                pygame.draw.rect(self.game_base.screen, self.cor_animacao_none, bloco_novo, width=5, border_radius=2)

    def configurar_nivel(self):
        if self.nivel_atual < len(self.niveis):
            self.num_colunas, self.num_blocos_por_fileira = self.niveis[self.nivel_atual]
            self.criar_blocos()

    def resetar_blocos(self):
        self.lis_blocos.clear()
        self.nivel = 0
        self.criar_blocos()

