from .imports import pygame
from .Player_Base import PlayerBase

class Player2(PlayerBase):
    def __init__(self, game):
        super().__init__(game)

    def draw(self):
        """Draws the player on the screen."""
        pygame.draw.rect(
            self.game.rect_manager.screen,
            (120, 120, 180),
            (self.x, self.y, self.width, self.height)
        )

    def _player_collision(self):
        return super()._player_collision()

    def input_player(self):
        """Handles player input for movement."""
        x = self.x
        keys = pygame.key.get_pressed()
        
        # Move left
        if keys[pygame.constants.K_a]:
            x -= 3.5
            if keys[pygame.constants.K_LSHIFT]:
                x -= 4.5

        # Move right
        if keys[pygame.constants.K_d]:
            x += 3.5
            if keys[pygame.constants.K_LSHIFT]:
                x += 4.5

        # Update position and validate with collision
        self.x = x
        self._player_collision()  # Garantir que o jogador não saia dos limites

    def reset(self):
        """Resets the player position."""
        super().reset()
        self.x = self.border.width / 2 + 40
        self.rect.x = self.x  # Sincroniza retângulo com posição
