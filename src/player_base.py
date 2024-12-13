from abc import ABC, abstractmethod
from .imports import pygame

class PlayerBase(ABC):
    """
    Base class for a player in the game.
    
    Attributes:
        game_base: Reference to the game core.
        pos_x: Player's horizontal position.
        pos_y: Player's vertical position.
        width_draw_x: Width of the player's drawable area.
        height_draw_y: Height of the player's drawable area.
        rect: Pygame Rect representing the player's position and size.
        border: The screen's boundary for collision detection.
    """
    def __init__(self, game_base):
        self.game_base = game_base
        self.pos_x = 280
        self.pos_y = 402
        self.width_draw_x = 40
        self.height_draw_y = 1
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.width_draw_x, self.height_draw_y)
        self.border = self.game_base.rect_manager.enum_rects.SCREEN_BORDER

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
        return self.pos_x

    @x.setter
    def x(self, value: int):
        self.pos_x = value
        self.rect.x = value

    @property
    def y(self) -> int:
        """Returns the player's vertical position."""
        return self.pos_y

    @y.setter
    def y(self, value: int):
        self.pos_y = value
        self.rect.y = value

    @abstractmethod
    def _player_collision(self):
        """Handles player collision with screen borders."""
        if self.pos_x - 5 <= self.border.left:
            self.pos_x = self.border.left + 5

        if self.pos_x + self.width_draw_x >= self.border.right:
            self.pos_x = self.border.right - self.width_draw_x

        self.rect.x = self.pos_x

    def reset(self):
        """Resets the player's position to the center."""
        self.pos_x = (self.border.width / 2) - (self.width_draw_x / 2)
        self.rect.x = self.pos_x
