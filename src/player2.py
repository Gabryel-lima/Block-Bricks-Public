from .imports import pygame
from .Player_Base import PlayerBase

class Player2(PlayerBase):
    def __init__(self, game_base):
        super().__init__(game_base)

    def draw(self):
        """Draws the player on the screen."""
        pygame.draw.rect(
            self.game_base.rect_manager.screen,
            (120, 120, 180),
            (self.pos_x, self.pos_y, self.width_draw_x, self.height_draw_y)
        )

    def _player_collision(self):
        return super()._player_collision()

    def input_player(self):
        """Handles player input for movement."""
        novo_x = self.pos_x
        keys = pygame.key.get_pressed()
        
        # Move left
        if keys[pygame.constants.K_a]:
            novo_x -= 3.5
            if keys[pygame.constants.K_LSHIFT]:
                novo_x -= 4.5

        # Move right
        if keys[pygame.constants.K_d]:
            novo_x += 3.5
            if keys[pygame.constants.K_LSHIFT]:
                novo_x += 4.5

        # Update position and validate with collision
        self.pos_x = novo_x
        self._player_collision()  # Garantir que o jogador não saia dos limites

    def reset(self):
        """Resets the player position."""
        super().reset()
        self.pos_x = self.game_base.width / 2 + 40
        self.rect.x = self.pos_x  # Sincroniza retângulo com posição
