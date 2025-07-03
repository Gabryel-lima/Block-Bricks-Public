import pygame
import numpy as np

class Blocks:
    def __init__(self, rect_manager, level_blocks=0):
        self.rect_manager = rect_manager
        self.level_blocks = level_blocks
        self.lis_blocks = []
        self._width = 60
        self._height = 20
        self._padding = 10
        self.color = (200, 200, 50)
        self.color_animated = (255, 255, 100)
        self.color_animated_none = (255, 255, 255)
        self.niveis = [(5, 7), (6, 8), (7, 9)]  # Exemplo de níveis: (linhas, colunas)
        self.fileira_init = 5
        self.coluna_init = 7
        self.create_blocks()

    def create_blocks(self):
        self.lis_blocks.clear()
        row, column = self.niveis[self.level_blocks % len(self.niveis)]
        for i in range(row):
            for j in range(column):
                x = self._padding + j * (self._width + self._padding)
                y = self._padding + i * (self._height + self._padding)
                bloco_rect = pygame.Rect(x, y, self._width, self._height)
                self.lis_blocks.append(bloco_rect)

    def draw(self):
        for bloco in self.lis_blocks:
            pygame.draw.rect(self.rect_manager.screen, self.color, bloco, width=0, border_radius=3)

    def animated_rect_collision(self, index):
        if 0 <= index < len(self.lis_blocks):
            block = self.lis_blocks[index]
            new_block = block.copy()
            new_block.inflate_ip(1.0, 1.3)
            pygame.draw.rect(self.rect_manager.screen, self.color_animated, new_block, width=0, border_radius=3)
            pygame.draw.rect(self.rect_manager.screen, self.color_animated_none, new_block, width=5, border_radius=2)

    def reset(self):
        self.level_blocks = (self.level_blocks + 1) % len(self.niveis)
        self.create_blocks()
