import numpy as np
import random
import pygame
import os
import tensorflow as tf
import imageio as iio

from tf_agents.specs import BoundedArraySpec
from tf_agents.environments.py_environment import PyEnvironment
from tf_agents.trajectories import time_step as ts

from ..Block_Bricks import Game

class CustomPyEnvironment(PyEnvironment):
    """
    Custom PyEnvironment para ser utilizado com agentes de aprendizado por reforço, onde um jogador deve interagir com uma bola e blocos.
    Esta classe implementa a lógica do jogo, observações, espaço de ações e recompensas.

    Attributes:
        render_mode (str): Modo de renderização do ambiente ('human' ou 'rgb_array').
        game (Game): Instância do jogo que contém a lógica principal.
    """
    __metadata__ = {"render_modes": ["human", "rgb_array"], "render_fps": 60} #TODO: Ainda não utilizado

    def __init__(self, render_mode: str = None, seed: int = None):
        """
        Inicializa o ambiente personalizado.

        Args:
            render_mode (str, opcional): Define como o jogo deve ser renderizado ('human' ou 'rgb_array').
            seed (int, opcional): Define a semente para gerar resultados reprodutíveis.
        """
        super().__init__()
        self.game = Game()  # Inicializa o jogo
        self.render_mode = render_mode
        # Define as especificações do espaço de ações (movimento do jogador)
        self._action_spec = BoundedArraySpec(shape=(), dtype=np.int32, minimum=0, maximum=2, name="action")
        # Define as especificações do espaço de observação (janela do jogo)
        self._observation_spec = BoundedArraySpec(
            shape=(self.game.window_size[0], self.game.window_size[1], self.game.channels),
            dtype=np.float32, minimum=0.0, maximum=1.0, name="observation"
        )

        self.seed(seed) if seed is not None else np.random.randint(1, 1e+6)
            
    def seed(self, seed: int) -> None:
        """
        Define a semente para todos os geradores de números aleatórios utilizados (random, numpy, tensorflow).

        Args:
            seed (int): Valor da semente.
        """
        random.seed(seed)
        np.random.seed(seed)
        tf.random.set_seed(seed)

    def action_spec(self) -> BoundedArraySpec:
        """ Retorna as especificações do espaço de ações. """
        return self._action_spec

    def observation_spec(self) -> BoundedArraySpec:
        """ Retorna as especificações do espaço de observação. """
        return self._observation_spec

    def _reset(self) -> ts.TimeStep:
        """
        Reinicia o ambiente para o estado inicial.

        Returns:
            ts.TimeStep: O estado inicial do ambiente após o reset.
        """
        self.game.reset_env()  # Reseta o estado do jogo
        obs = self.get_obs()  # Obtém a observação atual
        return self._create_timestep(obs, ts.StepType.FIRST, 0.0, 1.0)

    def _step(self, action: int) -> ts.TimeStep:
        """
        Executa uma ação no ambiente.

        Args:
            action (int): Ação a ser tomada (0, 1 ou 2).

        Returns:
            ts.TimeStep: O próximo estado do ambiente após a execução da ação.
        """
        self._apply_action(action)  # Aplica a ação ao jogador
        reward, done = self.calculate_reward(action)  # Calcula a recompensa
        obs = self.get_obs()  # Obtém a nova observação

        step_type = ts.StepType.MID if not done else ts.StepType.LAST
        discount = 1.0 if not done else 0.0

        return self._create_timestep(obs, step_type, reward, discount)

    def _create_timestep(self, obs, step_type, reward, discount) -> ts.TimeStep:
        """
        Cria um objeto TimeStep com os parâmetros fornecidos.

        Args:
            obs (np.ndarray): Observação do ambiente.
            step_type (ts.StepType): Tipo do passo (inicial, intermediário ou final).
            reward (float): Recompensa obtida.
            discount (float): Fator de desconto.

        Returns:
            ts.TimeStep: Estado representado como um TimeStep.
        """
        return ts.TimeStep(
            step_type=np.array(step_type, dtype=np.int32),
            reward=np.array(reward, dtype=np.float32),
            discount=np.array(discount, dtype=np.float32),
            observation=obs
        )

    def _apply_action(self, action: int) -> None:
        """
        Aplica a ação especificada ao jogador.

        Args:
            action (int): Ação a ser aplicada (0 - mover à direita, 1 - mover à esquerda, 2 - ajuste fino).
        """
        distance_to_ball = (self.game.ball.rect.centerx - self.game.bot.rect.centerx)
        if action == 0:  # Move para direita
            self.game.bot.move_right()
        elif action == 1:  # Move para esquerda
            self.game.bot.move_left()
        elif action == 2:  # Ajuste fino ou parar
            self.game.bot.fine_adjustment(distance_to_ball)
            # self.game.bot.stop()

    def calculate_reward(self, action: int) -> tuple[float, bool]:
        """
        Calcula a recompensa para o jogador com base na posição da bola e do jogador.

        Args:
            action (int): Ação tomada pelo jogador.

        Returns:
            tuple[float, bool]: Recompensa obtida e se o episódio terminou.
        """
        reward = 0.0
        done = False

        # Posicionamento da bola e do jogador
        ball_center = self.game.ball.rect.centerx
        player_center = self.game.bot.rect.centerx
        distance_to_ball = ball_center - player_center  # Pode ser positivo (direita) ou negativo (esquerda)
        tolerance = 10  # Tolerância para considerar o alinhamento como "perfeito"

        # Recompensa por manter a bola centralizada
        if abs(distance_to_ball) <= tolerance:
            reward += 1.0  # Alta recompensa por manter a bola alinhada ao centro
        else:
            # Penalidade proporcional à distância, menor para evitar desmotivação
            reward -= 0.0003 * abs(distance_to_ball)

        counter = 0 # TODO Tá meio estranho isso aqui ainda
        previous_len = len(self.game.blocks.lis_blocks)
        if len(self.game.blocks.lis_blocks) == previous_len:
            counter += 1
        else:
            counter = 0

        if counter > 600:
            reward -= 5.0
            counter = 0
            self.game.reset_env()
            pygame.time.wait(200)
            done = True

        # Recompensa por destruir todos os blocos
        if len(self.game.blocks.lis_blocks) == 0:
            reward += 15
            self.game.reset_env()
            pygame.time.wait(200)
            done = True

        # Recompensa por colidir com a bola (indica sucesso em manter a bola)
        if self.game.bot.rect.colliderect(self.game.ball.rect):
            reward += 10.0

        # Recompensa adicional por destruir blocos
        for block in self.game.blocks.lis_blocks:
            if self.game.ball.rect.colliderect(block):
                reward += 0.5 + (5 - len(self.game.blocks.lis_blocks)) * 0.2  # Quanto menos blocos, mais recompensa

        # Penalidade e finalização do jogo se a bola cair no chão
        if self.game.ball.y + self.game.ball.raio >= self.game.rect_manager.screen.get_height() - self.game.ball.relative_ball_pos:
            reward -= 10.0
            self.game.reset_env()
            pygame.time.wait(200)
            done = True

        return reward, done

    def get_obs(self) -> np.ndarray:
        """
        Obtém a observação atual do ambiente (frame renderizado).

        Returns:
            np.ndarray: Frame do jogo normalizado (valores entre 0 e 1).
        """
        obs = self.game.render_frame() / 255.0
        return obs

    def render(self, mode="human") -> np.ndarray: #TODO: Ainda não tem garantia dde funcionar corretamente. Apenas nas próximas versões
        """
        Renderiza o estado atual do ambiente.

        Args:
            mode (str): Modo de renderização ('human' ou 'rgb_array').
        """
        if mode == "rgb_array":
            return np.array(pygame.surfarray.array3d(self.game.screen), dtype=np.float32)
        elif mode == "human":
            self.game.render_frame()
            pygame.display.flip()

    def _create_video(self, frame_dir="./video/temp/", output_video_path="./video/agent_run.mp4") -> None:
        """
        Cria um vídeo da execução do agente salvando frames do jogo.

        Args:
            frame_dir (str): Diretório para salvar os frames temporários.
            output_video_path (str): Caminho para salvar o vídeo gerado.
        """
        os.makedirs(frame_dir, exist_ok=True)
        pygame.image.save(self.game.screen, f"{frame_dir}/frame_{self.game.current_game}.png")
        self.game.current_game += 1

        images = [pygame.image.load(os.path.join(frame_dir, f)).convert() 
                  for f in os.listdir(frame_dir) if f.endswith(".png")]

        with iio.get_writer(output_video_path, mode="I", fps=60) as writer:
            for img in images:
                writer.append_data(pygame.surfarray.pixels3d(img))

    def close(self) -> None:
        """
        Fecha o ambiente e limpa todos os recursos.
        """
        pygame.quit()
