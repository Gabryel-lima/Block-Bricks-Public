import pygame
from player_base import PlayerBase

class Player(PlayerBase):
    def __init__(self, rect_manager):
        super().__init__(rect_manager)

    def draw(self):
        pygame.draw.rect(
            self.rect_manager.screen,
            (255, 5, 5),
            (self.x, self.y, self.width, self.height)
        )

    def input_player(self):
        x = self.x
        keys = pygame.key.get_pressed()
        # Move para a esquerda
        if keys[pygame.K_a]:
            x -= 3.5
            if keys[pygame.K_LSHIFT]:
                x -= 4.5
        # Move para a direita
        if keys[pygame.K_d]:
            x += 3.5
            if keys[pygame.K_LSHIFT]:
                x += 4.5
        self.x = x
        self._player_collision()
