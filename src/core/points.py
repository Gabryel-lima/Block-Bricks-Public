


class Points:
    def __init__(self):
        #self.mens_ite_init = f'Pressione a tecla "Enter" para iniciar'
        self.resolution_base = (600, 600)
        self.resolution_base2 = (745, 690)

        self.level = 1
        self.mens_level = f'Level: {self.level}'
        self.init_points = 0
        self.mens_points_1_2 = f'Points: {self.init_points}'
        self.loading_lp2 = self.load_best_pontuation_player2()

        self.player_mode = None

    def load_best_pontuation_player2(self):
        try:
            with open('src/json/best_score2.json', 'r') as file:
                data = json.load(file)
                return data['best_score2']
        except (FileNotFoundError, KeyError):
            return 0

    def save_best_pontuation_player2(self):
        data = {'best_score2': self.loading_lp2}
        with open('src/json/best_score2.json', 'w') as file:
            json.dump(data, file)

    def update_best_pontuation_player2(self):
        if self.init_points > self.loading_lp2:
            self.loading_lp2 = self.init_points
            self.save_best_pontuation_player2()
            self.mens_bp2 = f'Best pontuation: {self.loading_lp2}'
