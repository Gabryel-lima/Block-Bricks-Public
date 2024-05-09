

import pygame



class Fonts:
    def __init__(self):
        self.__font_cache = {}
        self.font_impact = self.get_fonts_system('impact', 28)
        self.font_candara = self.get_fonts_system('Candara', 30, True, False)
        self.font_arial = self.get_fonts_system('arial', 32, True, False)
        self.font_times_new_roman = self.get_fonts_system('times new roman', 25, True, False)
        self.font_colibri = self.get_fonts_system('calibri', 30, False, False)

    def get_fonts_system(self, name: str = 'consolas', size: int = 12, 
                         bold: bool = False, italic: bool = False) -> pygame.font.Font:

        key = (name, size, bold, italic)

        if key not in self.__font_cache:
            self.__font_cache[key] = pygame.font.SysFont(name, size, bold, italic)

        return self.__font_cache[key]