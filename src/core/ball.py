from src.core.imports import pygame, random
import numpy as np

class Ball:
    def __init__(self, game_base):
        self.game_base = game_base
        self._x = 300
        self._y = 150
        self.VPos_x = 0
        self.VPos_y = 0
        self.raio = 5
        self.rect = pygame.Rect(self._x - self.raio, self._y - self.raio, self.raio * 2, self.raio * 2)
        self.rand_color = np.random.randint(50, 255, size=3)

    @property
    def center(self) -> np.ndarray:
        return np.array(self.rect.center, dtype=np.float32)

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, novo_valor: int):
        self._x = novo_valor
        self.rect.x = novo_valor

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, novo_valor: int):
        self._y = novo_valor
        self.rect.y = novo_valor

    def border_collide(self) -> tuple[float, float]:
        if self.x - self.raio <= 0 or self.x + self.raio >= self.game_base.border.width:
            self.VPos_x *= -1

        if self.y - self.raio <= 0 or self.y + self.raio >= self.game_base.border.height:
            self.VPos_y *= -1

        return self.VPos_x, self.VPos_y

    def draw(self):
        pygame.draw.circle(self.game_base.screen, self.rand_color, self.rect.center, self.raio)

    def start_movement(self):
        self.VPos_x = random.uniform(-3.0, 3.0)
        self.VPos_y = random.uniform(2.0, 2.0)

    def update(self):
        self.x += int(self.VPos_x)
        self.y += int(self.VPos_y)
        self.border_collide()

    def invert_direction(self, player: pygame.Rect):
        if self.rect.centerx <= player.centerx:
            self.VPos_x -= 1
            self.VPos_y *= -1
        elif self.rect.centerx >= player.centerx:
            self.VPos_x += 1
            self.VPos_y *= -1
        else:
            self.VPos_x *= 1
            self.VPos_y *= -1

    def reset(self):
        self.x = 300
        self.y = 150
        self.VPos_x = 0
        self.VPos_y = 0
        self.rect.center = (self.x, self.y)

    def menu_animation(self):
        self.draw()
        self.update()
