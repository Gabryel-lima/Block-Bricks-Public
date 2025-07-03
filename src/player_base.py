from abc import ABC, abstractmethod
import pygame

class PlayerBase(ABC):
    """
    Classe base para jogadores (Player, Player2, Bot).
    """
    def __init__(self, rect_manager):
        self.rect_manager = rect_manager
        self._x = 280
        self._y = 402
        self._width = 42
        self._height = 5
        self.rect = pygame.Rect(self._x, self._y, self._width, self._height)
        self.border = self.rect_manager.enum_rects.SCREEN_BORDER.value

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.rect.x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.rect.y = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
        self.rect.width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        self.rect.height = value

    def _player_collision(self):
        # Garante que o jogador não saia dos limites da tela
        if self.rect.left < self.border.left:
            self.rect.left = self.border.left
            self._x = self.rect.x
        if self.rect.right > self.border.right:
            self.rect.right = self.border.right
            self._x = self.rect.x

    def reset(self):
        self._x = 280
        self._y = 402
        self.rect.x = self._x
        self.rect.y = self._y

    @abstractmethod
    def draw(self):
        pass 