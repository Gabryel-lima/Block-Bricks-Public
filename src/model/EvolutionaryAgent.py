import numpy as np
import random
import os
import matplotlib.pyplot as plt
import tensorflow as tf
import keras
from CustomPyEnvironment import CustomPyEnvironment
from typing import Any

class EvolutionaryAgent:
    """
    Classe que implementa um agente evolutivo para ser utilizado em um ambiente de aprendizado por reforço.
    Este agente usa uma abordagem de evolução de população para melhorar suas políticas, utilizando
    seleção dos melhores indivíduos (elite), crossover e mutação para evoluir ao longo das gerações.

    Attributes:
        env (CustomPyEnvironment): Ambiente customizado para treino do agente.
        population_size (int): Tamanho da população de agentes.
        num_generations (int): Número de gerações para evolução.
        mutation_rate (float): Taxa de mutação para aplicação em cada indivíduo.
        elite_fraction (float): Fração da população que será considerada elite.
        population (list): Lista contendo os modelos (indivíduos) da população.
        fitness_history (list): Lista contendo o histórico do melhor fitness em cada geração.
        seed_np (int): Semente para a biblioteca numpy.
        seed_random (int): Semente para a biblioteca random.
        seed_tf (int): Semente para o TensorFlow.
        model (keras.Model): Modelo do melhor indivíduo (após o treinamento).
    """
    def __init__(self, env: CustomPyEnvironment, population_size: int = 50, num_generations: int = 100, 
                 mutation_rate: float = 0.1, elite_fraction: float = 0.2, set_seed: bool = True,
                 seed_np: int = None, seed_random: int = None, seed_tf: int = None):
        """
        Inicializa o agente evolutivo com os parâmetros especificados.

        Args:
            env (CustomPyEnvironment): Ambiente personalizado para treino.
            population_size (int): Tamanho da população de agentes.
            num_generations (int): Número de gerações para evolução.
            mutation_rate (float): Taxa de mutação a ser aplicada.
            elite_fraction (float): Fração da população que será mantida como elite.
            set_seed (bool): Se verdadeiro, define as sementes de maneira determinística.
            seed_np (int, opcional): Semente para numpy.
            seed_random (int, opcional): Semente para random.
            seed_tf (int, opcional): Semente para TensorFlow.
        """
        self.env = env
        self.population_size = population_size
        self.num_generations = num_generations
        self.mutation_rate = mutation_rate
        self.elite_fraction = elite_fraction
        self.input_shape = self.env.observation_spec().shape
        self.num_actions = self.env.action_spec().maximum - self.env.action_spec().minimum + 1
        self.population = []
        self.fitness_history = []
        seeds = self.set_seeds(set_seed, seed_np, seed_random, seed_tf)
        self.seed_np, self.seed_random, self.seed_tf = seeds
        self._initialize_population()
        self.model = None

    @classmethod
    def set_seeds(cls, set_seed=True, seed_np=None, seed_random=None, seed_tf=None) -> tuple[Any | int]:
        """
        Define as sementes para as bibliotecas numpy, random e TensorFlow.

        Args:
            set_seed (bool): Se verdadeiro, define as sementes para reprodutibilidade.
            seed_np (int, opcional): Semente para numpy.
            seed_random (int, opcional): Semente para random.
            seed_tf (int, opcional): Semente para TensorFlow.

        Returns:
            tuple: Sementes definidas para numpy, random e TensorFlow.
        """
        if set_seed:
            seed_np = seed_np if seed_np is not None else 42
            seed_random = seed_random if seed_random is not None else 42
            seed_tf = seed_tf if seed_tf is not None else 42
        else:
            seed_np = np.random.randint(1, 1e+6)
            seed_random = np.random.randint(1, 1e+6)
            seed_tf = np.random.randint(1, 1e+6)

        np.random.seed(seed_np)
        random.seed(seed_random)
        tf.random.set_seed(seed_tf)

        return seed_np, seed_random, seed_tf
    
    def _initialize_population(self) -> None:
        """
        Inicializa a população com redes neurais de parâmetros aleatórios.
        """
        for _ in range(self.population_size):
            model = self._create_model()
            self.population.append(model)
    
    def _create_model(self) -> keras.models.Sequential:
        """
        Cria um modelo simples de rede neural.

        Returns:
            keras.models.Sequential: Modelo neural inicializado.
        """
        model = keras.models.Sequential([
            keras.layers.Flatten(input_shape=self.input_shape),
            keras.layers.Dense(3, activation='relu'),
            keras.layers.Dense(self.num_actions, activation='linear')])
        
        return model
    
    def _evaluate_individual(self, model: keras.Model) -> np.ndarray:
        """
        Avalia um indivíduo no ambiente para calcular sua recompensa total.

        Args:
            model (keras.Model): Modelo a ser avaliado.

        Returns:
            np.ndarray: Recompensa total obtida pelo modelo.
        """
        total_reward = 0
        time_step = self.env.reset()

        while not time_step.is_last():
            state = time_step.observation
            action_values = model(np.expand_dims(state, axis=0), training=False)
            action = int(np.argmax(action_values.numpy()[0]))
            time_step = self.env.step(action)
            total_reward += time_step.reward

        return total_reward
    
    def _select_elite(self, fitnesses: np.ndarray) -> list:
        """
        Seleciona os melhores indivíduos (elite) com base nos valores de fitness.

        Args:
            fitnesses (np.ndarray): Lista de valores de fitness para cada indivíduo.

        Returns:
            list: Lista dos indivíduos considerados elite.
        """
        num_elite = max(1, int(self.elite_fraction * self.population_size))
        elite_indices = np.argsort(fitnesses)[-num_elite:]
        elite = [self.population[i] for i in elite_indices]

        return elite
    
    def _crossover(self, parent1: list, parent2: list) -> keras.models.Sequential:
        """
        Realiza o crossover entre dois indivíduos para criar um novo indivíduo.

        Args:
            parent1 (list): Primeiro indivíduo pai.
            parent2 (list): Segundo indivíduo pai.

        Returns:
            keras.models.Sequential: Novo indivíduo criado a partir do crossover.
        """
        child = self._create_model()
        
        for i in range(len(child.layers)):
            weights_parent1 = parent1.layers[i].get_weights()
            weights_parent2 = parent2.layers[i].get_weights()
            new_weights = []
            for w1, w2 in zip(weights_parent1, weights_parent2):
                mask = np.random.rand(*w1.shape) > 0.5
                w = np.where(mask, w1, w2)
                new_weights.append(w)
            child.layers[i].set_weights(new_weights)

        return child
    
    def _mutate(self, model: keras.Model) -> None:
        """
        Aplica mutação ao indivíduo, modificando seus parâmetros de forma aleatória.

        Args:
            model (keras.Model): Modelo a ser mutado.
        """
        for layer in model.layers:
            weights = layer.get_weights()
            new_weights = []
            for w in weights:
                if np.random.rand() < self.mutation_rate:
                    mutation = np.random.normal(0, 0.1, size=w.shape)
                    w += mutation
                new_weights.append(w)
            layer.set_weights(new_weights)
    
    def train(self) -> None:
        """
        Treina o agente evolutivo ao longo de diversas gerações, selecionando os melhores indivíduos e evoluindo a população.
        """
        best_fitness_overall: float = -np.inf 
        for generation in range(self.num_generations):
            fitnesses = []
            for individual in self.population:
                fitness = self._evaluate_individual(individual)
                fitnesses.append(fitness)
            max_fitness = np.max(fitnesses)
            avg_fitness = np.mean(fitnesses)
            self.fitness_history.append(max_fitness)
            print(f"Geração {generation+1}/{self.num_generations} - Melhor Fitness: {max_fitness:.2f} - Fitness Médio: {avg_fitness:.2f}")
            
            # Verificar se o melhor indivíduo desta geração é melhor que o melhor geral
            best_index = np.argmax(fitnesses)
            if fitnesses[best_index] > best_fitness_overall:
                best_fitness_overall = fitnesses[best_index]
                self.model = self.population[best_index]
                print(f"Novo melhor modelo encontrado com fitness: {best_fitness_overall:.2f}")

            # Seleção dos melhores indivíduos
            elite = self._select_elite(fitnesses)
            
            # Reprodução para formar a nova população
            new_population = elite.copy()
            while len(new_population) < self.population_size:
                parents = random.sample(elite, 2)
                child = self._crossover(parents[0], parents[1])
                self._mutate(child)
                new_population.append(child)
            self.population = new_population
    
    def evaluate_best(self) -> None:
        """
        Avalia o melhor indivíduo encontrado após o treinamento e renderiza o ambiente.
        """
        if self.model is None:
            print("Nenhum modelo disponível para avaliação.")
            return

        best_individual = self.model
        fitness = self._evaluate_individual(best_individual)
        print(f"Melhor Fitness: {fitness:.2f}")
        
        time_step = self.env.reset()
        self.env.render()
        while not time_step.is_last():
            state = time_step.observation
            action_values = best_individual(np.expand_dims(state, axis=0), training=False)
            action = int(np.argmax(action_values.numpy()[0]))
            time_step = self.env.step(action)
            self.env.render()
        self.env.close()
    
    def save_best_model(self, filepath: str) -> None:
        """
        Salva o melhor modelo encontrado após o treinamento.

        Args:
            filepath (str): Caminho para salvar o modelo.
        """
        if self.model is not None:
            self.model.save(filepath)
            print(f"Melhor modelo salvo em '{filepath}'")
        else:
            print("Nenhum modelo para salvar.")
    
    def load_model(self, filepath: str) -> None:
        """
        Carrega um modelo salvo a partir de um arquivo.

        Args:
            filepath (str): Caminho do arquivo de modelo a ser carregado.
        """
        self.model = keras.models.load_model(filepath)
        print(f"Modelo carregado de '{filepath}'")
    
    def plot_fitness(self) -> None:
        """
        Plota o histórico do melhor fitness ao longo das gerações.
        """
        plt.plot(self.fitness_history)
        plt.title('Histórico do Melhor Fitness')
        plt.xlabel('Geração')
        plt.ylabel('Fitness')
        plt.grid(True)
        plt.savefig('./train')

if __name__ == "__main__":
    # Inicializar o ambiente personalizado
    custom_pyenv = CustomPyEnvironment()
    
    # Criar uma instância do agente evolutivo
    evolutionary_agent = EvolutionaryAgent(
        env=custom_pyenv,
        population_size=10,
        num_generations=5,
        mutation_rate=0.1, 
        elite_fraction=0.2,
        set_seed=False
    )
    
    # Treinar o agente
    evolutionary_agent.train()
    evolutionary_agent.evaluate_best()
    evolutionary_agent.save_best_model('./hard_model.keras')
    
    # Plotar o histórico de fitness
    evolutionary_agent.plot_fitness()
    
    # Exemplo de como carregar o modelo salvo e usá-lo
    # evolutionary_agent.load_model('best_model.keras')
    # evolutionary_agent.evaluate_best()
    