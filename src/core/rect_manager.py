from src.core.imports import pygame


class RectManager:
    def __init__(self):  
        self.rects = {}             # Dicionário para armazenar os rects por nome
        self.groups = {}            # Dicionário para agrupar rects por tela/propósito
        self.screen_config = {}     # Configurações da tela (largura, altura, cor de fundo)
        self.screen = None          # Atributo para armazenar a tela do PyGame
        
        # Chama o método para configurar a tela ao inicializar
        self.set_screen_dimensions(width=608, height=608, bg_color=(0, 0, 0))
        self.setup_initial_screen()
        self.setup_pre_game_screen()
        self.setup_config_screen()

    # ------------------ Configuração da Tela ------------------

    def set_screen_dimensions(self, width: int = 720, height: int = 800, bg_color=(0, 0, 0)):
        """
        Configura as dimensões da tela e atualiza o rect de borda.
        """
        if width <= 0 or height <= 0:
            raise ValueError("A largura e altura devem ser maiores que 0.")

        # Configura a tela do PyGame
        self.screen = pygame.display.set_mode(size=(width, height))

        # Atualiza as configurações da tela
        self.screen_config = {
            "width": width,
            "height": height,
            "bg_color": bg_color,
        }

        # Atualiza ou cria o rect de borda
        if 'screen_border' not in self.rects:
            self.add_rect('screen_border', 0, 0, width, height)
        else:
            border = self.get_rect('screen_border')
            border.width = width
            border.height = height

    def get_screen_config(self):
        """Retorna as configurações atuais da tela."""
        return self.screen_config

    def clear_screen(self):
        """Limpa a tela com a cor de fundo configurada."""
        if self.screen is not None:
            self.screen.fill(self.screen_config.get("bg_color", (0, 0, 0)))

    # ------------------ Gerenciamento de Rects ------------------

    def add_rect(self, name, x, y, width, height, group=None):
        """Adiciona um rect ao gerenciador e opcionalmente a um grupo."""
        if name in self.rects:
            raise ValueError(f"Já existe um rect com o nome '{name}'.")
        
        # Cria o rect
        rect = pygame.Rect(x, y, width, height)
        self.rects[name] = rect

        # Adiciona ao grupo, se especificado
        if group:
            if group not in self.groups:
                self.groups[group] = []
            self.groups[group].append(name)

    def get_rect(self, name):
        """Retorna um rect pelo nome."""
        return self.rects.get(name)

    def get_group(self, group):
        """Retorna todos os rects pertencentes a um grupo."""
        if group in self.groups:
            return [self.rects[name] for name in self.groups[group]]
        return []

    def move_all(self, dx, dy, group=None):
        """
        Move todos os rects por um deslocamento (dx, dy).
        Se um grupo for especificado, move apenas os rects desse grupo.
        """
        rects = self.get_group(group) if group else self.rects.values()
        for rect in rects:
            rect.x += dx
            rect.y += dy

    def move_rect(self, name, dx, dy):
        """
        Move um único rect por um deslocamento (dx, dy).
        """
        rect = self.get_rect(name)
        if rect:
            rect.x += dx
            rect.y += dy

    # ------------------ Configuração de Telas Específicas ------------------

    def setup_initial_screen(self):
        """Cria os rects específicos para a tela inicial."""
        self.add_rect('blit_text_player1', 245, 170, 170, 0, group='initial_screen')
        self.add_rect('blit_text_player2', 245, 230, 230, 0, group='initial_screen')
        self.add_rect('blit_text_bot', 245, 290, 120, 0, group='initial_screen')

        self.add_rect('button_player1', 240, 170, 120, 40, group='initial_screen')
        self.add_rect('button_player2', 240, 230, 120, 40, group='initial_screen')
        self.add_rect('button_bot', 240, 290, 120, 40, group='initial_screen')

        self.add_rect('underline_button_player1', 245, 210, 0, 5, group='initial_screen')
        self.add_rect('underline_button_player2', 245, 270, 0, 5, group='initial_screen')
        self.add_rect('underline_button_bot', 245, 330, 0, 5, group='initial_screen')

        self.add_rect('blit_text_creator', 40, 520, 0, 0, group='initial_screen')
        self.add_rect('button_creator_link', 40, 522, 280, 30, group='initial_screen')
        self.add_rect('underline_creator_link', 40, 558, 0, 3, group='initial_screen')

    def setup_pre_game_screen(self):
        """Cria os rects específicos para a tela pré-jogo."""
        self.add_rect('button_back', 40, 300, 85, 30, group='pre_game_screen')
        self.add_rect('underline_back', 40, 340, 0, 3, group='pre_game_screen')

        self.add_rect('blit_text_game_over', 215, 225, 0, 0, group='pre_game_screen')
        self.add_rect('blit_text_back', 40, 300, 0, 0, group='pre_game_screen')
        self.add_rect('blit_text_points_player1', 40, 430, 0, 0, group='pre_game_screen')
        self.add_rect('blit_text_best_points_player1', 40, 530, 0, 0, group='pre_game_screen')
        self.add_rect('blit_text_level', 40, 480, 0, 0, group='pre_game_screen')
        self.add_rect('blit_text_points_player2', 40, 430, 0, 0, group='pre_game_screen')
        self.add_rect('blit_text_best_points_player2', 40, 530, 0, 0, group='pre_game_screen')

    def setup_config_screen(self):
        """Cria os rects específicos para a tela de configurações."""
        self.add_rect('blit_resolution_option1', 0, 0, 0, 0, group='config_screen')
        self.add_rect('blit_resolution_option2', 240, 230, 120, 40, group='config_screen')
        self.add_rect('blit_resolution_option3', 240, 290, 120, 40, group='config_screen')

        self.add_rect('blit_image_config_icon', 475, 495, 0, 0, group='config_screen')
        self.add_rect('button_config', 474, 494, 53, 53, group='config_screen')

        self.add_rect('blit_text_resolution_option1', 245, 170, 0, 0, group='config_screen')
        self.add_rect('blit_text_resolution_option2', 245, 230, 0, 0, group='config_screen')
        self.add_rect('blit_text_resolution_option3', 232, 290, 0, 0, group='config_screen')

    def draw_group(self, group, color=(255, 255, 255), px=2):
        """Desenha todos os rects pertencentes a um grupo."""
        if self.screen is not None and group in self.groups:
            rects = self.get_group(group)
            for rect in rects:
                pygame.draw.rect(self.screen, color, rect, px)
