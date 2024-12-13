import pygame


class EventHandler:
    def __init__(self):
        self.mode = None

    @staticmethod
    def for_event() -> list[pygame.event.Event]:
        """Itera por todos os eventos do Pygame."""
        events = list(pygame.event.get())
        for event in events:
            if event.type == pygame.constants.QUIT:
                pygame.quit()
        return events

    @classmethod
    def click_mouse(cls):
        """Verifica se um clique do mouse foi detectado."""
        for event in cls.for_event():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return True
        return False
    