

from typing import Union

import pygame


class ConfigButton:
    def __init__(self, game_base):
        self.game_base = game_base
        self.img_config_load = pygame.image.load('assets/gear_config.png').convert_alpha()
        self.img_config = pygame.transform.scale(self.img_config_load, (50, 50)).convert_alpha()
        self.resolution_text1 = f'600x600'
        self.resolution_text2 = f'750x720'
        self.resolution_text3 = f'Fullscreen'
        self.copy_surface = pygame.SurfaceType((50, 50), pygame.SRCALPHA).convert_alpha()
        self.func_vars_tela = self.game_base.vars_tela_config()
        self.func_vars_config = self.game_base.vars_tela_config()
        
    def button_config(self) -> pygame.Rect:
        self.draw_button_config()
        pos_mouse = pygame.mouse.get_pos()

        if self.func_vars_tela.rect_botao_config.collidepoint(pos_mouse):
            scaled_copy = pygame.transform.scale_by(self.img_config, (1.1, 1.1))
            self.func_vars_tela.screen.blit(scaled_copy, self.func_vars_tela.img_xy)
            return self.func_vars_tela.rect_botao_config
        
    def draw_button_config(self, show=True) -> pygame.Rect:
        if show:
            self.copy_surface.blit(self.img_config, (0, 0))
            self.func_vars_tela.screen.blit(self.copy_surface, self.func_vars_tela.img_xy)
            return self.func_vars_tela.rect_botao_config

    @staticmethod
    def get_value_list(list_name: list[pygame.Rect], index: int):
        return list_name[index]

    def partition_draw_buttons_resolutions(self) -> Union[pygame.Rect, int, list, int]:
        pos_mouse = pygame.mouse.get_pos()
        resolution1 = self.resolution_text1
        resolution2 = self.resolution_text2
        resolution3 = self.resolution_text3
        
        rect1 = self.get_value_list(list_name=self.func_vars_tela.list_tela_config, index=0)
        rect2 = self.get_value_list(list_name=self.func_vars_tela.list_tela_config, index=1)
        rect3 = self.get_value_list(list_name=self.func_vars_tela.list_tela_config, index=2)

        color_rect_resolution1 = (170, 170, 170) if rect1.collidepoint(pos_mouse) else (255, 255, 255)
        color_rect_resolution2 = (170, 170, 170) if rect2.collidepoint(pos_mouse) else (255, 255, 255)
        color_rect_resolution3 = (170, 170, 170) if rect3.collidepoint(pos_mouse) else (255, 255, 255)

        text1 = self.func_vars_tela.fonte_config.render(resolution1, False, color_rect_resolution1)
        self.func_vars_tela.screen.blit(text1, self.func_vars_config.blit_xy_resolucao_texto1)
        text2 = self.func_vars_tela.fonte_config.render(resolution2, False, color_rect_resolution2)
        self.func_vars_tela.screen.blit(text2, self.func_vars_config.blit_xy_resolucao_texto2)
        text3 = self.func_vars_tela.fonte_config.render(resolution3, False, color_rect_resolution3)
        self.func_vars_tela.screen.blit(text3, self.func_vars_config.blit_xy_resolucao_texto3)

        return rect1, rect2, rect3


