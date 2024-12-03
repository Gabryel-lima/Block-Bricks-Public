import json


class Points:
    def __init__(self, blocks):
        """
        Gerenciador de pontos e níveis para o jogador.

        :param blocks: Referência aos blocos do jogo (para resetar níveis, se necessário).
        """
        self.points = 0  # Pontuação inicial
        self.loading_points = self._load_best_pontuation('src/json/best_score.json')  # Melhor pontuação do jogador 1
        self.loading_lp2 = self._load_best_pontuation('src/json/best_score2.json')  # Melhor pontuação do jogador 2
        self.blocks = blocks  # Blocos do jogo, usado para gerenciar níveis
        self.level = 0  # Nível inicial
        self.is_game_over = False  # Flag para exibir mensagens de fim de nível

        # Mensagens padrão
        self.mens_points_1_2 = f'Points: {self.points}'
        self.mens_bp = f'Best points: {self.loading_points}'
        self.mens_bp2 = f'Best pontuation: {self.loading_lp2}'
        self.mesg_nivel = f'Level: {self.level}'

    # ------------------ Gerenciamento de Pontuações ------------------

    def update_points(self):
        """Atualiza a pontuação do jogador."""
        self.points += 1
        self.mens_points_1_2 = f'Points: {self.points}'

    def reset_points(self):
        """Reseta a pontuação atual do jogador."""
        self.points = 0
        self.mens_points_1_2 = f'Points: {self.points}'

    def reset_points_and_levels(self):
        """
        Reseta os pontos e o nível do jogador, dependendo da mensagem de fim de nível.
        """
        if self.is_game_over:
            self.mens_points_1_2 = f'Points: {self.points}'
            self.mesg_nivel = f'Level: {self.level}'
        else:
            self.points = 0
            self.mens_points_1_2 = f'Points: {self.points}'
            self.blocks.level_blocks = 0
            self.mesg_nivel = f'Level: {self.blocks.level_blocks}'

    # ------------------ Melhor Pontuação (Player 1 e Player 2) ------------------

    def update_best_pontuation_player1(self):
        """Atualiza a melhor pontuação do jogador 1."""
        if self.points > self.loading_points:
            self.loading_points = self.points
            self._save_best_pontuation('src/json/best_score.json', self.loading_points)
            self.mens_bp = f'Best points: {self.loading_points}'

    def update_best_pontuation_player2(self):
        """Atualiza a melhor pontuação do jogador 2."""
        if self.points > self.loading_lp2:
            self.loading_lp2 = self.points
            self._save_best_pontuation('src/json/best_score2.json', self.loading_lp2)
            self.mens_bp2 = f'Best pontuation: {self.loading_lp2}'

    # ------------------ Gerenciamento de Níveis ------------------

    def update_level(self):
        """Atualiza o nível do jogador."""
        self.level += 1
        self.mesg_nivel = f'Level: {self.level}'

    def reset_level(self):
        """Reseta o nível do jogador."""
        self.level = 0
        self.mesg_nivel = f'Level: {self.level}'

    # ------------------ Operações de Carregamento e Salvamento ------------------

    @staticmethod
    def _load_best_pontuation(file_path):
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
    def _save_best_pontuation(file_path, best_score):
        """
        Salva a melhor pontuação em um arquivo JSON.

        :param file_path: Caminho para o arquivo JSON.
        :param best_score: Melhor pontuação a ser salva.
        """
        data = {'best_score': best_score}
        with open(file_path, 'w') as file:
            json.dump(data, file)

