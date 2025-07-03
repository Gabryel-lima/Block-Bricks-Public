import pygame
from player_base import PlayerBase

class Bot(PlayerBase):
    def __init__(self, rect_manager):
        super().__init__(rect_manager)

    def draw(self):
        self.draw_bot()

    def draw_bot(self):
        pygame.draw.rect(
            self.rect_manager.screen,
            (20, 155, 40),
            (self.x, self.y, self.width, self.height)
        )

    def update(self, ball):
        # Movimento simples: segue a bola
        if ball.x > self.x:
            self.x += 3.0
        elif ball.x < self.x:
            self.x -= 3.0
        self._player_collision()

    def reset_bot(self):
        self.x = self.border.width // 2
