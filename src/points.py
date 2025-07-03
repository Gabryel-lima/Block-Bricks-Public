import json
import pygame

class Points:
    def __init__(self, blocks, file_best_score='src/json/best_score.json'):
        self.blocks = blocks
        self._counter_points = 0
        self._init_level = 0
        self.loading_points = self._load_best_pontuation(file_best_score)
        self.file_best_score = file_best_score

    def update_points(self, value=1):
        self._counter_points += value

    def update_best_pontuation(self):
        if self._counter_points > self.loading_points:
            self.loading_points = self._counter_points
            self._save_best_pontuation(self.file_best_score, self.loading_points)

    def update_level(self):
        self._init_level += 1

    def reset_level(self):
        self._init_level = 0

    def reset_points_and_levels(self):
        self._counter_points = 0
        self._init_level = 0

    @staticmethod
    def _load_best_pontuation(file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                return data.get('best_score', 0)
        except (FileNotFoundError, KeyError, json.JSONDecodeError):
            return 0

    @staticmethod
    def _save_best_pontuation(file_path, best_score=0):
        data = {'best_score': best_score}
        with open(file_path, 'w') as file:
            json.dump(data, file)

    def draw_level(self, rect_manager, font=None):
        font = font or pygame.font.SysFont('arial', 24, bold=True)
        text = font.render(f'Nível: {self._init_level+1}', True, (255, 255, 255))
        rect_manager.screen.blit(text, rect_manager.rects[rect_manager.enum_rects.BLIT_TEXT_LEVEL])

    def draw_pontuation(self, rect_manager, font=None):
        font = font or pygame.font.SysFont('arial', 24, bold=True)
        text = font.render(f'Pontos: {self._counter_points}', True, (255, 255, 255))
        rect_manager.screen.blit(text, rect_manager.rects[rect_manager.enum_rects.BLIT_TEXT_POINTS])

    def draw_best_pontuation(self, rect_manager, font=None):
        font = font or pygame.font.SysFont('arial', 24, bold=True)
        text = font.render(f'Melhor: {self.loading_points}', True, (255, 255, 0))
        rect_manager.screen.blit(text, rect_manager.rects[rect_manager.enum_rects.BLIT_TEXT_BEST_POINTS]) 
