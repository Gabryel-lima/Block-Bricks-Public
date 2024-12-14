from .imports import pygame

class CustomString: # TODO: Mais a frente vou me aprofundar meelhor nestes conceitos.
    def __init__(self, value: str):
        self.value = value

    def __format__(self, format_spec):
        if format_spec == "upper":
            return self.value.upper()
        return self.value

class Texts(CustomString):
    def __init__(self, game_base, fonts):
        super().__init__(value="")
        self.game_base = game_base
        self.fonts = fonts
        self.text_dict: dict = {}
        self.over: str = 'Game Over'
        self.win: str = 'You win!'
        self.player_1_2: str = 'Player'
        self.str_points: str = 'Points'
        self.str_best_points: str = 'Best Pontuation'
        self.str_level: str = 'Level'
        self.modo_bot: str = 'Bot'
        self.back: str = 'Back'
        self.button_iter: str = f'Pressione a tecla {"Enter"} para iniciar'

    def _to_list(self, /) -> list[tuple[str]]:
        """Vai alocar todos os atributos e valores em uma lista de tupla."""
        return [(key, value) for key, value in self.__dict__.items() if isinstance(value, str)]
    
    # def _format_all_texts(self, format_spec: str, /) -> dict: # TODO: Mais a frente vou me aprofundar meelhor nestes conceitos.
    #     """
    #     Formata todos os atributos em um formato específcio de str.

    #     param: format_spec Definição de qual tipo de formatação. Exemplo: format_spec="upper"
    #     """
    #     return {key: format(value, format_spec) for key, value in self.__dict__.items() if isinstance(value, str)}
    
    # def _format_text(self, key: str, format_spec: str, /) -> str:
    #     text = getattr(self, key, None)
    #     if text:
    #         return format(text, format_spec)
    #     raise KeyError(f"Texto com chave '{key}' não encontrado.")

    # def __format__(self, format_spec):
    #     return getattr(self, format_spec, "Unknown text key")

