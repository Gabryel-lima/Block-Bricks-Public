from abc import ABC, abstractmethod
from src.imports import pygame

class PlayerBase(ABC):
    """
    Base class for a player in the game.
    
    Attributes:
        game: Reference to the game core.
        pos_x: Player's horizontal position.
        pos_y: Player's vertical position.
        width: Width of the player's drawable area.
        height: Height of the player's drawable area.
        rect: Pygame Rect representing the player's position and size.
        border: The screen's boundary for collision detection.
    """
    def __init__(self, game):
        """Obs ¬ Estou definindo como valores int, mas poderia ser float como é o padrão da classe pygame.rect.Rect"""
        self.game = game
        self._pos_x = 280
        self._pos_y = 402
        self._width = 42
        self._height = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.border = self.game.rect_manager.enum_rects.SCREEN_BORDER.value

    @property
    def width(self):
        """Retuerns the width draw of player Rect."""
        return self._width
    
    @width.setter
    def width(self, value: int):
        self.rect.width = value

    @property
    def height(self):
        """Retuerns the height draw of player Rect."""
        return self._height
    
    @height.setter
    def height(self, value: int):
        self.rect.height = value

    @property
    def center_x(self) -> int:
        """Returns the horizontal center of the player."""
        return self.rect.centerx
    
    @center_x.setter
    def center_x(self, value: int):
        self.rect.centerx = value

    @property
    def x(self) -> int:
        """Returns the player's horizontal position."""
        return self._pos_x

    @x.setter
    def x(self, value: int):
        self.rect.x = value

    @property
    def y(self) -> int:
        """Returns the player's vertical position."""
        return self._pos_y

    @y.setter
    def y(self, value: int):
        self.rect.y = value

    def _ball_collision(self):
        if self.game.ball.rect.colliderect(self.rect):
            self.game.ball._invert_direction(player=self.rect)

    @abstractmethod
    def _player_collision(self):
        """Handles player collision with screen borders."""
        if self.x - 5 <= self.border.left:
            self.x = self.border.left + 5

        if self.x + self.width >= self.border.right:
            self.x = self.border.right - self.width

        self.rect.x = self.x
        self._ball_collision()

    def reset(self):
        """Resets the player's position to the center."""
        self.x = (self.border.width / 2) - (self.width / 2)
