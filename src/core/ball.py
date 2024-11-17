from src.core.imports import pygame, random
import numpy as np

class Ball:
    def __init__(self, game_base, start_x=300, start_y=150, raio=5):
        self.game_base = game_base
        self._x = start_x
        self._y = start_y
        self.raio = raio
        self.rect = pygame.Rect(self._x - self.raio, self._y - self.raio, self.raio * 2, self.raio * 2)
        self.rand_color = np.random.randint(50, 255, size=3)
        self.relative_ball_pos = 180
        self.VPos_x = 0
        self.VPos_y = 0

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int):
        self._x = value
        self.rect.x = value

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int):
        self._y = value
        self.rect.y = value

    def start_movement(self):
        self.VPos_x = random.uniform(-3.0, 3.0)
        self.VPos_y = random.uniform(2.0, 2.0)

    def check_collision(self):
        if self.x - self.raio <= 0 or self.x + self.raio >= self.game_base.border.width:
            self.VPos_x *= -1
        if self.y - self.raio <= 0 or self.y + self.raio >= self.game_base.border.height:
            self.VPos_y *= -1

    def border_collide(self) -> tuple[float, float]:
        self.check_collision()
        return self.VPos_x, self.VPos_y

    def invert_direction(self, player: pygame.Rect):
        self.VPos_x += -1 if self.rect.centerx <= player.centerx else 1
        self.VPos_y *= -1

    def reset(self):
        self.x = self._x
        self.y = self._y
        self.VPos_x = 0
        self.VPos_y = 0
        self.rect.center = (self.x, self.y)

    def draw(self, color=None, raio=None):
        color = color or self.rand_color
        raio = raio or self.raio
        pygame.draw.circle(self.game_base.screen, color, self.rect.center, raio)

    def update(self):
        self.x += int(self.VPos_x)
        self.y += int(self.VPos_y)
        self.border_collide()

    def menu_animation(self):
        self.draw()
        self.update()
