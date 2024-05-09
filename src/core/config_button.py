

from typing import Union

import pygame

from pygame._sdl2 import Texture

from src.core.setings import PATH, ConfigVars


class ConfigButton:
    def __init__(self, game_base: object):
        self.game_base = game_base
        self.settings = ConfigVars(self.game_base)
        self.fonte_config = pygame.font.SysFont('arial', 32, True, False)
        self.img_config_load = pygame.image.load(PATH + 'assets/gear_config.png')
        self.img_config = pygame.transform.scale(self.img_config_load, (50, 50))
        self.resolution_text1 = f'600x600'
        self.resolution_text2 = f'750x720'
        self.resolution_text3 = f'Fullscreen'
        self.copy_surface = pygame.SurfaceType((50, 50), pygame.SRCALPHA)
        
    def button_config(self):
        self.draw_button_config()
        pos_mouse = pygame.mouse.get_pos()

        if self.settings.rect_botao_config.collidepoint(pos_mouse):
            scaled_copy = pygame.transform.scale_by(self.img_config, (1.1, 1.1))
            self.game_base.screen.blit(scaled_copy, self.settings.img_xy)
        return self.settings.rect_botao_config
        
    def draw_button_config(self, show: bool = True):
        if show:
            self.copy_surface.blit(self.img_config, (0, 0))
            self.game_base.screen.blit(self.copy_surface, self.settings.img_xy)
        return self.settings.rect_botao_config

    @staticmethod
    def _get_value_list(index_list_name: int):
        return index_list_name

    def partition_draw_buttons_resolutions(self) -> pygame.Rect | int | list[any]:
        pos_mouse = pygame.mouse.get_pos()
        resolution1 = self.resolution_text1
        resolution2 = self.resolution_text2
        resolution3 = self.resolution_text3
        
        rect1 = self._get_value_list(index_list_name=self.settings.rect_resolucao_texto1)
        rect2 = self._get_value_list(index_list_name=self.settings.rect_resolucao_texto2)
        rect3 = self._get_value_list(index_list_name=self.settings.rect_resolucao_texto3)

        color_rect_resolution1 = (170, 170, 170) if rect1.collidepoint(pos_mouse) else (255, 255, 255)
        color_rect_resolution2 = (170, 170, 170) if rect2.collidepoint(pos_mouse) else (255, 255, 255)
        color_rect_resolution3 = (170, 170, 170) if rect3.collidepoint(pos_mouse) else (255, 255, 255)

        text1 = self.fonte_config.render(resolution1, False, color_rect_resolution1)
        self.game_base.screen.blit(text1, self.settings.blit_xy_resolucao_texto1)
        text2 = self.fonte_config.render(resolution2, False, color_rect_resolution2)
        self.game_base.screen.blit(text2, self.settings.blit_xy_resolucao_texto2)
        text3 = self.fonte_config.render(resolution3, False, color_rect_resolution3)
        self.game_base.screen.blit(text3, self.settings.blit_xy_resolucao_texto3)

        return rect1, rect2, rect3


