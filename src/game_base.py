import pygame

class GameBase:
    """Classe base para gerenciamento do ciclo principal e estados do jogo."""
    def __init__(self):
        self.running = False
        self.current_state = "menu"  # Estados: menu, pre_runing, playing
        # As entidades do jogo (player, ball, blocks, etc.) serão injetadas depois
        self.entities = {}

    def set_entities(self, **entities):
        """Permite injetar as entidades do jogo (player, ball, blocks, etc.)."""
        self.entities = entities

    def run(self):
        """Loop principal do jogo, gerencia os estados e eventos."""
        self.running = True
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_event(event)
            self.update()
            self.render()
            pygame.display.update()
        pygame.quit()

    def handle_event(self, event):
        """Gerencia eventos de acordo com o estado atual."""
        # Implementação base - pode ser sobrescrita na subclasse
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.current_state == "playing":
                    self.current_state = "menu"
                elif self.current_state == "pre_runing":
                    self.current_state = "menu"

    def update(self):
        """Atualiza o estado do jogo (override na subclasse)."""
        # Implementação base - pode ser sobrescrita na subclasse
        pass

    def render(self):
        """Renderiza a tela do jogo (override na subclasse)."""
        # Implementação base - pode ser sobrescrita na subclasse
        pass

    def change_state(self, new_state):
        """Método auxiliar para mudar o estado do jogo."""
        self.current_state = new_state

    def get_entity(self, name):
        """Método auxiliar para obter uma entidade do jogo."""
        return self.entities.get(name) 
