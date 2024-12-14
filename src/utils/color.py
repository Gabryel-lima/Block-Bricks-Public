from enum import Enum

class Color(Enum):

    def __call__(self):
        return self.to_rgba()
    
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

    def to_rgba(self, alpha: float = 1.0, /):
        """
        Convert the HEX color to RGBA format.

        param:
            alpha (float): Opacity value (0.0 to 1.0).

        return:
            tuple: (R, G, B, A) Where R, G, B are integers (0-255) and A is float (0.0-1.0).
        """
        hex_color = self.value.lstrip("#")
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return (r, g, b, alpha)
