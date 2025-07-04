import pygame
import numpy as np

class Ball:
    def __init__(self, rect_manager, start_x=300, start_y=150, raio=5):
        self.rect_manager = rect_manager
        self.relative_ball_pos = 180
        self._x = start_x
        self._y = start_y
        self.raio = raio
        self.rect = pygame.Rect(self.x - self.raio, self.y - self.raio, self.raio * 2, self.raio * 2)
        self.rand_color = np.random.randint(50, 255, size=3)
        self.VPos_x = 0
        self.VPos_y = 0
        self._movement_started = False

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.rect.x = value - self.raio

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.rect.y = value - self.raio

    def start_movement(self, min_speed=2.0, max_speed=3.0):
        self.VPos_x = np.random.uniform(-float(max_speed), float(max_speed))
        self.VPos_y = np.random.uniform(float(min_speed), float(max_speed))
        self._movement_started = True

    def _check_collision(self):
        border = self.rect_manager.enum_rects.SCREEN_BORDER.value
        if self.x - self.raio <= 0 or self.x + self.raio >= border.width:
            self.VPos_x *= -1
        if self.y - self.raio <= 0 or self.y + self.raio >= border.height:
            self.VPos_y *= -1

    def reset(self):
        self.x = 300
        self.y = 150
        self.VPos_x = 0
        self.VPos_y = 0
        self.rect.center = (self.x, self.y)
        self._movement_started = False

    def draw(self, color=None, raio=None):
        color = color if color is not None else self.rand_color
        raio = raio if raio is not None else self.raio
        pygame.draw.circle(self.rect_manager.screen, color, (self.rect.center), raio)

    def update(self, max_velocity=4.8):
        # Limita a velocidade
        velocity_magnitude = (self.VPos_x**2 + self.VPos_y**2)**0.5
        if velocity_magnitude > max_velocity:
            scale = max_velocity / velocity_magnitude
            self.VPos_x *= scale
            self.VPos_y *= scale
        self.x += int(self.VPos_x)
        self.y += int(self.VPos_y)
        self._check_collision() 
