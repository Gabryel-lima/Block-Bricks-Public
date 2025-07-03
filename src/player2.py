import pygame
from player_base import PlayerBase

class Player2(PlayerBase):
    def __init__(self, rect_manager):
        super().__init__(rect_manager)
        self.x = self.border.width // 2 + 40  # Posição inicial diferente

    def draw(self):
        pygame.draw.rect(
            self.rect_manager.screen,
            (120, 120, 180),
            (self.x, self.y, self.width, self.height)
        )

    def input_player(self):
        x = self.x
        keys = pygame.key.get_pressed()
        # Move para a esquerda
        if keys[pygame.K_LEFT]:
            x -= 3.5
            if keys[pygame.K_RSHIFT]:
                x -= 4.5
        # Move para a direita
        if keys[pygame.K_RIGHT]:
            x += 3.5
            if keys[pygame.K_RSHIFT]:
                x += 4.5
        self.x = x
        self._player_collision()
