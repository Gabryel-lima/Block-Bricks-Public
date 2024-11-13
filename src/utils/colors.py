from enum import Enum

class Colors(Enum): # TODO: Depois vou dar uma olhada melhor nisto, é bem interessante!
    """Define as cores usadas no programa. Bem bacana este enum"""
    RED = (255, 0, 0, 0)
    GREEN = (0, 255, 0, 0)
    BLUE = (0, 0, 255, 0)
    WHITE = (255, 255, 255, 0)

class Players(Enum):
    pass

class Blocks(Enum):
    pass

class Layout(Enum):
    pass

class Texts(Enum):
    pass