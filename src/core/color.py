from enum import Enum

class Color(Enum):

    def __call__(self):
        return self.value
    
    RED = "#FF0000"
    GREEN = "#00FF00"
    BLUE = "#0000FF"
    YELLOW = "#FFFF00"
    CYAN = "#00FFFF"
    MAGENTA = "#FF00FF"
    ORANGE = "#FFA500"
    PURPLE = "#800080"
    LIME = "#00FF00"
    PINK = "#FFC0CB"
    TEAL = "#008080"
    OLIVE = "#808000"
    MAROON = "#800000"
    NAVY = "#000080"
    GRAY = "#808080"
    BLACK = "#000000"
    WHITE = "#FFFFFF"
