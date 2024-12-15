from .imports import pygame, random
import numpy as np

class Ball:
    def __init__(self, game, start_x=300, start_y=150, raio=5):
        self.game = game
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

    def _verify_height_ball(self):
        # pos_y lim 420.0
        if self.y + self.raio >= self.game.rect_manager.screen.get_height() - self.relative_ball_pos:
            self.game.rect_manager.screen.blit(self.game.fonts.font_arial.render('Game Over!', False, (127, 127, 127)), 
                                          self.game.rect_manager.enum_rects.BLIT_TEXT_GAME_OVER.value)
            self.reset()
            # TODO: Tálvez perguntar para continuar jogando 
            # TODO: Ainda vai ser necessário definir o texto corretamente na tela com uma nova classe

    def start_movement(self, min_speed: float = 2.0, max_speed: float = 3.0):
        self.VPos_x = np.random.uniform(-float(max_speed), float(max_speed))
        self.VPos_y = np.random.uniform(float(min_speed), float(max_speed))

    def _check_collision(self):
        border = self.game.rect_manager.enum_rects.SCREEN_BORDER.value
        if self.x - self.raio <= 0 or self.x + self.raio >= border.width:
            self.VPos_x *= -1
        if self.y - self.raio <= 0 or self.y + self.raio >= border.height:
            self.VPos_y *= -1

    def _border_collide(self) -> tuple[float, float]:
        self._check_collision()
        return self.VPos_x, self.VPos_y

    def _invert_direction(self, player: pygame.Rect):
        self.VPos_x += -1 if self.rect.centerx <= player.centerx else 1
        self.VPos_y *= -1

    def reset(self):
        self.x = 300
        self.y = 150
        self.VPos_x = 0
        self.VPos_y = 0
        self.rect.center = (self.x, self.y)
        self._movement_started = False

    def draw(self, color=None, raio: int = 5):
        color = color or self.rand_color
        raio = raio or self.raio
        pygame.draw.circle(self.game.rect_manager.screen, color, self.rect.center, raio)

    def _limit_velocity(self, max_velocity: float):
        velocity_magnitude = (self.VPos_x**2 + self.VPos_y**2)**0.5
        if velocity_magnitude > max_velocity:
            scale = max_velocity / velocity_magnitude
            self.VPos_x *= scale

    def _handle_state(self, is_menu: bool):
        """Executa ações específicas dependendo do estado."""
        if is_menu:
            self.game.blocks.draw()
        else:
            self._verify_height_ball()

    def update(self, max_velocity=4.8, *, is_menu: bool = True):
        self._limit_velocity(max_velocity)
        self.x += int(self.VPos_x)
        self.y += int(self.VPos_y)
        self._border_collide()
        self._handle_state(is_menu)

    def menu_animation(self): # TODO: Ainda devo configurar uma bolinha um pouco diferente e mais divertida
        if not self._movement_started:
            self.start_movement(min_speed=-3.0, max_speed=4.8)
            self._movement_started = True
        self.update(is_menu=True)
        self.draw()

