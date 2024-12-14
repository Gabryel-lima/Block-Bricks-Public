import json

from .Texts import Texts
from .Blocks import Blocks
# TODO: Estas formas de importações devem ser melhoradas 

class Points:
    def __init__(self, text: Texts, blocks: Blocks):
        """
        Gerenciador de pontos e níveis para o jogador.

        :param text: Referência aos textos do jogo.
        :param blocks: Referência aos blocos do jogo (para resetar níveis, se necessário).
        """
        self.text = text
        self.blocks = blocks
        self._counter_points: int = 0  # Pontuação inicial
        self._init_level: int = 0  # Nível inicial
        self.loading_points: int = self._load_best_pontuation('src/json/best_score.json')
        self.loading_points_2: int = self._load_best_pontuation('src/json/best_score2.json')
        self.is_game_over: bool = False  # Flag para exibir mensagens de fim de nível

    # ------------------ Propriedades de Pontos ------------------

    @property
    def init_points(self) -> str:
        return f'{self.text.str_points}{self._counter_points}'

    @init_points.setter
    def init_points(self, value: int):
        if value < 0:
            raise ValueError("A pontuação não pode ser negativa.")
        self._counter_points = value

    @property
    def best_pontuation(self) -> str:
        return f'{self.text.str_best_points}{self.loading_points}'

    @property
    def init_level(self) -> str:
        return f'{self.text.str_level}{self._init_level + 1}'

    # ------------------ Gerenciamento de Pontuações ------------------

    def update_points(self, increment: int = 1) -> None:
        """Atualiza a pontuação do jogador."""
        self.init_points = self._counter_points + increment

    def reset_points(self) -> None:
        """Reseta a pontuação atual do jogador."""
        self._counter_points = 0

    def reset_points_and_levels(self) -> None:
        """Reseta pontos e níveis do jogador."""
        self.reset_points()
        self._init_level = 0

    def update_best_pontuation(self, player: int = 1) -> None:
        """
        Atualiza a melhor pontuação para o jogador especificado.

        :param player: Jogador 1 ou 2.
        """
        if player == 1 and self._counter_points > self.loading_points:
            self.loading_points = self._counter_points
            self._save_best_pontuation('src/json/best_score.json', self.loading_points)
        elif player == 2 and self._counter_points > self.loading_points_2:
            self.loading_points_2 = self._counter_points
            self._save_best_pontuation('src/json/best_score2.json', self.loading_points_2)

    # ------------------ Gerenciamento de Níveis ------------------

    def update_level(self) -> None:
        """Atualiza o nível do jogador."""
        self._init_level += 1

    def reset_level(self) -> None:
        """Reseta o nível do jogador."""
        self._init_level = 0

    # ------------------ Operações de Carregamento e Salvamento ------------------

    @staticmethod
    def _load_best_pontuation(file_path: str) -> int:
        """
        Carrega a melhor pontuação de um arquivo JSON.

        :param file_path: Caminho para o arquivo JSON.
        :return: A melhor pontuação carregada ou 0 se o arquivo não existir.
        """
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                return data.get('best_score', 0)
        except (FileNotFoundError, KeyError, json.JSONDecodeError):
            return 0

    @staticmethod
    def _save_best_pontuation(file_path: str, best_score: int = 0) -> None:
        """
        Salva a melhor pontuação em um arquivo JSON.

        :param file_path: Caminho para o arquivo JSON.
        :param best_score: Melhor pontuação a ser salva.
        """
        data = {'best_score': best_score}
        with open(file_path, 'w') as file:
            json.dump(data, file)

    def draw_pontuation(self, rect_manager, fonts):
        """
        Desenha a pontuação atual na tela.
        """
        texto_formatado = fonts.get_fonts_system('arial', 28).render(
            f"{self.init_points}", False, (127, 127, 127)
        )
        rect_manager.screen.blit(
            texto_formatado, rect_manager.rects["BLIT_TEXT_POINTS"].topleft
        )

    def draw_best_pontuation(self, rect_manager, fonts):
        """
        Desenha a melhor pontuação na tela.
        """
        texto_formatado = fonts.get_fonts_system('arial', 28).render(
            f"{self.best_pontuation}", False, (127, 127, 127)
        )
        rect_manager.screen.blit(
            texto_formatado, rect_manager.rects["BLIT_TEXT_BEST_POINTS"].topleft
        )

    def draw_level(self, rect_manager, fonts):
        """
        Desenha o nível atual na tela.
        """
        texto_formatado = fonts.get_fonts_system('arial', 28).render(
            f"{self.init_level}", False, (127, 127, 127)
        )
        rect_manager.screen.blit(
            texto_formatado, rect_manager.rects["BLIT_TEXT_LEVEL"].topleft
        )



