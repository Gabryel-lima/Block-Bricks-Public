

import pygame


from src.core.player_base import PlayerBase


class Player2(PlayerBase):
    def __init__(self, game_base):
        super().__init__(game_base)

    def desenho_player(self):
        pygame.draw.rect(self.game_base.screen, (255, 150, 60),
                         ((self.pos_x), (self.pos_y), self.width_draw_x, 5))

    def input_player2(self):
        novo_x = self.pos_x
        if pygame.key.get_pressed()[pygame.constants.K_LEFT]:
            novo_x -= 3.5

            if pygame.key.get_pressed()[pygame.constants.K_RSHIFT]:
                novo_x -= 4.5

        if pygame.key.get_pressed()[pygame.constants.K_RIGHT]:
            novo_x += 3.5

            if pygame.key.get_pressed()[pygame.constants.K_RSHIFT]:
                novo_x += 4.5

        # if self.colisao.left <= novo_x <= self.colisao.right - 40:
        #     self._pos_x = novo_x

        self.pos_x = novo_x

    def reset(self):
        self.pos_x = self.game_base.width // 2 + 40
        

    