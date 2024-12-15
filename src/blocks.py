from .imports import pygame


class Blocks:
    def __init__(self, game):
        self.game = game
        self._width = 57
        self._heigth = 20
        self.color = (150, 80, 35)
        self.color_animated = (255, 255, 255)
        self.color_animated_none = (127, 127, 127)
        #self.rand_color = np.random.randint(10, 255, size=3)
        self.level_blocks = 0
        self._padding = 17
        self.lis_blocks = []
        self.row = 0 # TODO: Estas inicializações ainda possuem muitas redundâncias.
        self.column = 0
        self.fileira_init = 0
        self.coluna_init = 0
        self.niveis = {
            0: (8,3),  # nível 1: (n_row, n_columns)
            1: (8,4),  # nível 2
            2: (8,4),  # nível 3
            3: (8,5),  # nível 4
            4: (8,5),  # nível 5
            5: (8,6),  # nível 6
            6: (8,6),  # nível 7
            7: (8,7),  # nível 8 
            8: (8,7),  # nível 9
            9: (8,8)  # nível 10
        }
        self.create_blocks()

    def __len__(self):
        return len(self.lis_blocks) if self.lis_blocks else 0

    @property
    def padding(self) -> int:
        return self._padding
    
    @property
    def largura_bloco(self) -> int:
        return self._width
    
    @property
    def altura_bloco(self) -> int:
        return self._heigth

    @padding.setter
    def padding(self, value: int):
        self._padding = value
        self.lis_blocks.clear()
        self.create_blocks()  

    @largura_bloco.setter
    def largura_bloco(self, value: int):
        self._width = value
        self.lis_blocks.clear()
        self.create_blocks()  
    
    @altura_bloco.setter
    def altura_bloco(self, value: int):
        self._heigth = value
        self.lis_blocks.clear()
        self.create_blocks()

    def create_blocks(self):

        row, column = self.niveis[self.level_blocks]

        for i in range(row):
            for j in range(column):
                x = self._padding + i * (self._width + self._padding)
                y = self._padding + j * (self._heigth + self._padding)
                self.bloco_Rect = pygame.Rect(x, y, self._width, self._heigth)
                self.lis_blocks.append(self.bloco_Rect)

    def draw(self):
        #self.rand_color = np.random.randint(10, 255, size=3) # Colocando a instância aqui só para ficar engraçado kkkk
        for bloco in self.lis_blocks:
            pygame.draw.rect(self.game.rect_manager.screen, self.color, bloco, width=0, border_radius=3)
            
    def animated_rect_collision(self, index: int):
        for idx, block in enumerate(self.lis_blocks):
            if idx == index:
                new_block = block.copy()
                new_block.inflate_ip(1.0, 1.3)
                pygame.draw.rect(self.game.rect_manager.screen, self.color_animated, new_block, width=0, border_radius=3)
                pygame.draw.rect(self.game.rect_manager.screen, self.color_animated_none, new_block, width=5, border_radius=2)

    def reset(self):
        self.lis_blocks.clear()
        self.row = self.fileira_init  # Reatribui o estado inicial
        self.column = self.coluna_init  # Reatribui o estado inicial
        self.create_blocks()
