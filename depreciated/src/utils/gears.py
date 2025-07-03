import numpy as np
import math
import pandas as pd
import os
import matplotlib.pyplot as plt
import pygame
from typing import Any

plt.rc('font', size=14)
plt.rc('axes', labelsize=14, titlesize=14)
plt.rc('legend', fontsize=14)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)

from typing import Union, Tuple, Optional, Dict

def scaled_surface_percent(surf, percentage):
    width, height = surf.get_size()
    new_width = int(width * percentage / 100)
    new_height = int(height * percentage / 100)
    return pygame.transform.scale(surf, (new_width, new_height))

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t

def get_intersection(A: Union[Tuple[float, float], Point],
                     B: Union[Tuple[float, float], Point],
                     C: Union[Tuple[float, float], Point],
                     D: Union[Tuple[float, float], Point]) -> Optional[Dict[str, Union[Point, float]]]:
    """Determina o ponto de interseção entre dois segmentos de reta."""
    
    Ax, Ay = (A.x, A.y) if hasattr(A, "x") else A
    Bx, By = (B.x, B.y) if hasattr(B, "x") else B
    Cx, Cy = (C.x, C.y) if hasattr(C, "x") else C
    Dx, Dy = (D.x, D.y) if hasattr(D, "x") else D

    t_top = (Dx - Cx) * (Ay - Cy) - (Dy - Cy) * (Ax - Cx)
    u_top = (Cy - Ay) * (Ax - Bx) - (Cx - Ax) * (Ay - By)
    bottom = (Dy - Cy) * (Bx - Ax) - (Dx - Cx) * (By - Ay)

    if bottom != 0:
        t = t_top / bottom
        u = u_top / bottom
        if 0 <= t <= 1 and 0 <= u <= 1:
            return {"point": Point(lerp(Ax, Bx, t), lerp(Ay, By, t)), "offset": t}

    return None

def polys_intersect(poly_1, poly_2):
    """Descrição: Verifica se dois polígonos se intersectam. \n
        Método: Verifica se algum par de arestas dos dois polígonos se intersecta usando a função get_intersection.
        Retorno: True se houver interseção, False caso contrário."""
    for i in range(len(poly_1)):
        for j in range(len(poly_2)):
            touch = Point.get_intersection(
                poly_1[i],
                poly_1[(i+1) % len(poly_1)],
                poly_2[j],
                poly_2[(i+j) % len(poly_2)]
            )
            if touch: 
                return True
    return False


def get_rgba(value):
    """Descrição: Converte um valor numérico em uma cor RGBA (Red, Green, Blue, Alpha). \n
        Lógica:
            Normaliza o valor para o intervalo [0, 1].
            Calcula o valor alpha baseado no valor normalizado.
                Define os valores RGB com base no valor normalizado e se o valor é positivo ou negativo."""
    normalized_value = (value + 1) / 2
    alpha = int(normalized_value * 255)

    if value >= 0:
        r = int(normalized_value * 255)
        g = int(normalized_value * 250)
        b = 55
    else:
        r = 0
        g = 50
        b = int((1 - normalized_value) * 255)

    return (r, g, b, alpha)


def draw_dashed_line(surface, color, start_pos, end_pos, width=1, dash_length=10, offset=0):
    """Descrição: Desenha uma linha pontilhada na superfície do pygame.
        Lógica:
            Calcula o número de traços com base no comprimento da linha e no comprimento do traço.
                Desenha cada traço como uma linha sólida.

        Observações Gerais:

                As funções lerp e get_intersection são fundamentais para cálculos geométricos, como determinar pontos intermediários e interseções de segmentos de reta.
                A função polys_intersect é útil para verificar colisões entre polígonos.
                    A função get_rgba é uma forma de mapear valores numéricos para cores.
                A função draw_dashed_line é uma função auxiliar para visualização."""
    x1, y1 = start_pos
    x2, y2 = end_pos
    dl = dash_length

    length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    dash_count = int(length / dl)
    for i in range(dash_count):
        start = (x1 + (x2 - x1) * (i + offset) / dash_count,
                y1 + (y2 - y1) * (i + offset) / dash_count)
        end = (x1 + (x2 - x1) * (i + 0.5 + offset) / dash_count,
            y1 + (y2 - y1) * (i + 0.5 + offset) / dash_count)
        pygame.draw.line(surface, color, start, end, width)


def create_dir(dir_name:str, dir_path:str="."):
    dir_full_path = os.path.join(dir_path, dir_name)
    os.makedirs(dir_full_path, exist_ok=True)


def save_fig(name:str="file", path:str=r".", tight_layout=True, fig_extension="png", resolution=250):
    """Salva os plots em png.

    Parâmetros:
        >>> def save_fig(name='name_file', path='name_path')"""
    # Garante que o diretório existe
    os.makedirs(path, exist_ok=True)
    # Corrige a forma de criar o caminho completo
    p = os.path.join(path, name + "." + fig_extension)
    if tight_layout:
        plt.tight_layout()
    print("\nSaving figure", name)
    plt.savefig(p, format=fig_extension, dpi=resolution)


def create_backup_pkl(path:str=r"./", df=None, name:str="file", pkl_extension="pkl"):
    """Salva um DataFrame em formato pickle no caminho especificado.

    Parâmetros:
       >>> def create_backup_pkl(path='file_path', name='name_file')"""
    os.makedirs(path, exist_ok=True)
    file = os.path.join(path, name + "." + pkl_extension)
    if df is not None:
        pd.to_pickle(obj=df, filepath_or_buffer=file)


def describe_pkl_read(file_path_pkl:str=None):
    """Uma descrição dos dados em .pkl"""
    if file_path_pkl is not None:
        file = pd.read_pickle(file_path_pkl)
        print(file.describe())
    else:
        print("\nCaminho de arquivo não encontrado...\n".title())


def transform_pkl_to_csv(file_path_pkl:str=None, output_file_name:str=None, csv_extension="csv"):
    """Transforma o arquivo .pkl em .csv
    
    Parâmetros:
        >>> def transform_pkl_to_csv('file_path_pkl', 'output_path_name')"""
    if file_path_pkl is None:
        print("\nArquivo pickle não encontrado.\n")
        return  # Garante que o código pare aqui se o caminho não for fornecido
    df = pd.read_pickle(file_path_pkl)
    if output_file_name is not None:
        df.to_csv(output_file_name + "." + csv_extension, index=False)
        print(f"\nArquivo CSV criado com sucesso: {output_file_name}\n")
    else:
        print("\nÉ necessário fornecer um nome de arquivo de saída para salvar o CSV.\n")


YELLOW = (210, 255, 0, 65)
GREY = (127, 127, 127)
GREEN = (0, 255, 0, 0)
RED = (255, 0, 0, 0)
BLACK = (0, 0, 0, 0)

import math
import numpy as np
import pygame
from typing import Union, Tuple, Dict, Optional

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t

def get_intersection(A: Union[Tuple[float, float], Point],
                     B: Union[Tuple[float, float], Point],
                     C: Union[Tuple[float, float], Point],
                     D: Union[Tuple[float, float], Point]) -> Optional[Dict[str, Union[Point, float]]]:
    
    Ax, Ay = (A.x, A.y) if hasattr(A, "x") else A
    Bx, By = (B.x, B.y) if hasattr(B, "x") else B
    Cx, Cy = (C.x, C.y) if hasattr(C, "x") else C
    Dx, Dy = (D.x, D.y) if hasattr(D, "x") else D

    t_top = (Dx - Cx) * (Ay - Cy) - (Dy - Cy) * (Ax - Cx)
    u_top = (Cy - Ay) * (Ax - Bx) - (Cx - Ax) * (Ay - By)
    bottom = (Dy - Cy) * (Bx - Ax) - (Dx - Cx) * (By - Ay)

    if bottom != 0:
        t = t_top / bottom
        u = u_top / bottom
        if 0 <= t <= 1 and 0 <= u <= 1:
            return {"point": Point(lerp(Ax, Bx, t), lerp(Ay, By, t)), "offset": t}

    return None

class Sensor:
    def __init__(self, game_base):
        self.game_base = game_base
        self.last_ball_positions = []  # Histórico de posições da bola
        self.velocity = np.array([0.0, 0.0], dtype=np.float32)  # Velocidade da bola

    def update_velocity(self):
        current_ball_position = np.array([self.game_base.ball.bola_Rect.centerx, self.game_base.ball.bola_Rect.centery], dtype=np.float32)
        
        if len(self.last_ball_positions) > 0:
            # Calcular a diferença de posição média para suavização
            diffs = [current_ball_position - pos for pos in self.last_ball_positions]
            self.velocity = np.mean(diffs, axis=0)

        # Atualizar o histórico de posições
        self.last_ball_positions.append(current_ball_position)
        if len(self.last_ball_positions) > 5:  # Manter um histórico limitado de 5 posições
            self.last_ball_positions.pop(0)

    def predict_ball_position(self, time_in_future: float) -> np.ndarray:
        predicted_position = self.last_ball_positions[-1] + self.velocity * time_in_future
        return predicted_position
    
    def _create_lines(self, centerx: int, centery: int, angle: float, length: int) -> list[Tuple[Tuple[int, int], Tuple[int, int]]]:
        # Ajustar o número de raios para melhorar a performance
        angle_step = 4  # Reduzir o número de raios, melhorando o desempenho
        rays = []

        for theta in range(0, int(angle), angle_step):
            angle_rad = math.radians(-theta)
            end_x = centerx + (length * math.cos(angle_rad))
            end_y = centery + (length * math.sin(angle_rad))
            rays.append(((centerx, centery), (end_x, end_y)))

        return rays

    def draw_lines_sensor(self, screen: pygame.SurfaceType):
        self.update_velocity()  # Atualizar a velocidade antes de desenhar as linhas

        player_cx = self.game_base.player.rect.centerx
        player_cy = self.game_base.player.rect.centery
        border_screen = pygame.Rect((0, 0), screen.get_size())

        # Criar linhas de sensor ao redor do jogador
        rays = self._create_lines(centerx=player_cx, centery=player_cy, angle=184.0, length=30**2)  # Definir o comprimento de linha adequado
        colliding_lines = []

        # Iterar sobre os raios e desenhá-los
        for start_pos, end_pos in rays:
            # Clipping da linha para que não ultrapasse os limites da tela
            clipped_start, clipped_end = pygame.rect.Rect.clipline(border_screen, start_pos, end_pos)

            # Verificar colisão com a bola
            intersection_ball = get_intersection(
                clipped_start,
                clipped_end,
                (self.game_base.ball.bola_Rect.left, self.game_base.ball.bola_Rect.top),
                (self.game_base.ball.bola_Rect.right, self.game_base.ball.bola_Rect.bottom)
            )

            if intersection_ball is not None:
                # Se houver interseção, desenhar linha verde até o ponto de colisão
                intersection_point = intersection_ball.get("point")
                pygame.draw.line(screen, GREEN, clipped_start, (intersection_point.x, intersection_point.y), width=2)
                colliding_lines.append((intersection_point.x, intersection_point.y))  # Adicionar ponto de colisão
            else:
                # Se não houver colisão, desenhar linha cinza até o ponto final
                pygame.draw.line(screen, GREY, clipped_start, clipped_end, width=2)

        # Prever posição da bola no futuro (por exemplo, 1 segundo no futuro)
        future_ball_position = self.predict_ball_position(time_in_future=1.0)
        
        # Desenhar a posição prevista da bola na tela
        future_ball_pos_tuple = (int(future_ball_position[0]), int(future_ball_position[1]))
        pygame.draw.circle(screen, YELLOW, future_ball_pos_tuple, 5)  # Círculo amarelo para a posição prevista

        # Retornar as informações no formato necessário para o agente de rede neural
        if colliding_lines:
            colliding_lines_array = np.array(colliding_lines, dtype=np.float32).flatten().reshape(1, -1)
        else:
            colliding_lines_array = np.zeros((1, 2), dtype=np.float32)

        future_ball_position = future_ball_position.flatten().reshape(1, -1)

        combined_array = np.concatenate([colliding_lines_array, future_ball_position], axis=1)
        conv2d_input = combined_array.reshape(1, 1, combined_array.shape[1], 1)

        return conv2d_input
    
def apenda_dot(value):
    import json
    with open("./.holly.json", "w") as file:
        json.dump({"dot_coco": value}, file)
        file.write("\n")

class Han:
    def __init__(self, car):
        self.car = car
        self.ray_count = 5
        self.ray_length = 100
        self.ray_spread = 0.5*math.pi

        self.rays = []
        self.readings = []

    def update(self, road_borders):
        self.ray_cast()
        self.readings = []
        for i in range(len(self.rays)):
            self.readings.append(self.get_reading(self.rays[i], road_borders))

    def get_reading(self, ray, road_borders):
        touches = []
        for i in range(len(road_borders)):
            touch = get_intersection(
                ray[0],
                ray[1],
                road_borders[i][0],
                road_borders[i][1]
            )
            if touch:
                touches.append(touch)
        if len(touches) == 0:
            return None
        else:
            offsets = [e['offset'] for e in touches]
            min_offset = min(offsets)
            return next(e for e in touches if e['offset'] == min_offset)

    def ray_cast(self):
        self.rays = []
        for i in range(self.ray_count):
            ray_angle = lerp(self.ray_spread/2, -
                             self.ray_spread/2, i/(self.ray_count-1))+self.car.angle
            start = Point(self.car.x, self.car.y)
            end = Point(self.car.x - math.sin(ray_angle)*self.ray_length,
                        self.car.y - math.cos(ray_angle)*self.ray_length)

            self.rays.append((start, end))

    def draw(self, screen):
        for i in range(self.ray_count):
            end = self.rays[i][1]
            if self.readings[i] is not None:
                end = self.readings[i]['point']

            if isinstance(end, tuple):
                end = Point(*end)

            pygame.draw.line(
                screen, YELLOW, (self.rays[i][0].x, self.rays[i][0].y),
                (end.x, end.y), 2)

            pygame.draw.line(
                screen, GREY, (self.rays[i][1].x, self.rays[i][1].y),
                (end.x, end.y), 2)

