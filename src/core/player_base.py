
import pygame


class PlayerBase:
    def __init__(self, game_base: object):
        self.game_base = game_base
        self.pos_x: int = 280
        self.pos_y: int = 402
        self.width_draw_x = 40
        self.height_draw_y = 1
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.get_width_draw_x, self.height_draw_y)

    @property
    def get_pos_x(self) -> int:
        return self.pos_x

    @get_pos_x.setter
    def set_pos_x(self, novo_valor: int):
        self.pos_x = novo_valor
        self.rect.x = novo_valor

    @property
    def get_pos_y(self) -> int:
        return self.pos_y

    @get_pos_y.setter
    def set_pos_y(self, novo_valor: int):
        self.pos_y = novo_valor
        self.rect.y = novo_valor

    @property
    def get_width_draw_x(self) -> int:
        return self.width_draw_x

    @get_width_draw_x.setter
    def set_width_draw_x(self, novo_valor: int):
        self.width_draw_x = novo_valor

    @property
    def get_height_draw_y(self) -> int:
        return self.height_draw_y

    @get_height_draw_y.setter
    def set_height_draw_y(self, novo_valor: int):
        self.height_draw_y = novo_valor

    def player_collision(self):
        if self.pos_x - 5 <= self.game_base.border.left:
            self.pos_x = self.game_base.border.left + 5

        if self.pos_x + 45 >= self.game_base.border.right:
            self.pos_x = self.game_base.border.right - 45

        self.rect.x = self.pos_x

    def reset(self):
        self.pos_x = self.game_base.width / 2 - self.get_width_draw_x / 2
        self.rect.x = self.pos_x
