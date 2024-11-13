# Machine Learning Study Applied to a Custom Game

This document presents a study that integrates my game Block-Bricks (Almost an Arkanoid), where I use reinforcement learning and evolutionary learning techniques. In this study, three main components stand out: modifying the game's backend, developing a custom `PyEnvironment`, and implementing an evolutionary agent to optimize interaction in the game. This project was heavily influenced by the book **"Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow" by Aurélien Géron**, which guided many of the approaches and techniques employed here.

## Modification of the Game Backend

The game that served as the basis for this study is a recreated version in Python of the Arkanoid game, where a player must interact with a ball and blocks. This game was adapted to allow the application of reinforcement learning techniques, which included modifications to the backend to support reward calculation, detailed observations of the game state, and defining possible actions for the player. This was the most challenging part, by the way, haha.

The game logic, which includes interaction between the player, ball, and blocks, was encapsulated in a class called `Game`. This class offers methods to control the player, detect collisions, and maintain the game state. This architecture allowed easy integration of the game with reinforcement learning techniques, as each action of the agent could be translated into an explicit change in the game state. Essentially, I compressed the game information to a smaller resolution scale and normalized the game pixels to a range of 0 to 1.

## `CustomPyEnvironment`

The next step was to create a custom environment that could be used by reinforcement learning algorithms. The `CustomPyEnvironment` is a customized implementation of `PyEnvironment`, a component of the `TF-Agents` library. This environment provides an interface that allows an agent to interact with the game, defining possible actions and specifying available observations.

This custom environment defines the specifications for the action and observation spaces, as well as the rules for calculating rewards based on the player's performance in keeping the ball moving and destroying blocks. The reward logic was carefully designed to encourage the agent to align the player with the ball, destroy blocks, and prevent the ball from passing the player. With the `CustomPyEnvironment`, the game is transformed into a reinforcement learning problem, where the agent learns to optimize its actions to maximize rewards.

### Structure of `CustomPyEnvironment`

- **Action and Observation Specification**: The environment defines a set of three possible actions for the player: move right, move left, and fine adjustment (or stop). The observation is the current game frame, normalized to values between 0 and 1, representing the state of the environment, as mentioned earlier.
- **Reward and Penalty**: The reward system encourages the alignment of the paddle with the ball, rewarding block destruction and penalizing failures such as letting the ball "fall".
- **Reset and Step**: Methods to reset the environment and advance a step in the game were implemented, providing a structure to simulate game episodes that can be easily used by any reinforcement learning algorithm.

## Evolutionary Agent (`EvolutionaryAgent`)

One of the most interesting innovations of this study was the implementation of an evolutionary agent (`EvolutionaryAgent`) to train a model that interacts with the `CustomPyEnvironment`. This agent uses concepts from genetic algorithms to find the best policy for playing the game. Each individual in the population is represented by a neural network that tries to maximize rewards in each episode, as until then, I had tried to apply a DQN (Deep Q-Network) model.

### Functioning of the Evolutionary Agent

The evolutionary agent was directly inspired by the study of evolutionary algorithms mentioned in the book **"Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow" by Aurélien Géron**. Initially, I studied the DQN model presented in the book, but due to the hardware limitations of my computer and the desire to delve deeper into the concepts, I chose to develop my own strategy based on evolutionary algorithms. The evolutionary approach was chosen for its simplicity and ability to explore different parameter combinations without the need to derive gradients, as is the case with traditional neural network training. Since my computer has limitations in exploring a more complex CNN model, I sought to delve deeper into each concept presented in the book.

#### Main Components of `EvolutionaryAgent`

- **Initial Population**: The population consists of simple neural networks initialized with random weights. Each network tries to play the game and accumulate rewards.
- **Evaluation and Selection**: Each individual is evaluated based on their performance in the game. The performance is measured by the total reward accumulated over an episode. The best individuals are selected to form the elite, which will be used to generate the next generation.
- **Crossover and Mutation**: To generate new individuals, a crossover is performed between two parents chosen from the elite, combining their weights to create a new network. A mutation is applied randomly to introduce variation and help avoid stagnation in fitness values.
- **Fitness History**: The performance of the population over the generations is recorded, and the best-performing model is saved for later evaluation and use.

## Results and Reflections

The implementation of the `EvolutionaryAgent` proved to be a good use of the study of genetic algorithms described in Aurélien Géron's book. The evolutionary agent was able to gradually improve its performance over the generations, learning to keep the ball in play longer and destroy blocks more efficiently.

Although evolutionary learning can be computationally intensive, its conceptual simplicity and ability to find good solutions even without derivatives made it ideal for this project. The experience provided a practical understanding of the challenges involved in reinforcement learning and demonstrated the effectiveness of evolutionary techniques in complex optimization problems.

## Conclusion

This study explored the integration of machine learning and evolutionary algorithms in a custom game. Modifying the game's backend, developing the `CustomPyEnvironment`, and implementing the `EvolutionaryAgent` proved to be fundamental steps in transforming the game control problem into a reinforcement learning challenge. Using concepts from the book **"Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow" by Aurélien Géron**, it was possible to develop a practical and efficient approach to train an agent to continuously improve its performance.

The success of the evolutionary agent in this context reinforces the potential of evolutionary algorithms as a viable alternative for training agents, especially in scenarios where traditional gradient-based methods can be difficult to apply or ineffective.

## Back to Main Project

To learn more about the broader context of this project, including other components such as the game backend and reinforcement learning environment setup, please visit the [Main README](./README.md).
