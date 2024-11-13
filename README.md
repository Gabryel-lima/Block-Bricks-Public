# Block-Bricks (Almost an Arkanoid)

Welcome to Block-Bricks, a Python recreation of the classic game Arkanoid, where a player must interact with a ball and blocks to complete levels. This project explores the integration of machine learning techniques, particularly reinforcement learning and evolutionary strategies, to optimize gameplay.

## Features

- Recreated game in Python.
- Custom reinforcement learning environment (`CustomPyEnvironment`).
- Evolutionary agent (`EvolutionaryAgent`) for learning and optimizing game interactions.

## Game Backend

The game backend includes logic for controlling the paddle, ball dynamics, collision detection, and interaction with blocks. This was customized to support the application of reinforcement learning, allowing an agent to learn how to play the game autonomously. The game state is represented as normalized frames, allowing easy use for ML models.

## Documentation and Related Projects

For more detailed information about specific components of the project, check out the following:

- [Block-Bricks Detailed Documentation](./Block-Bricks.md): This document provides an in-depth explanation of the game's backend, its mechanics, and the different strategies used to enhance gameplay.
- [Evolutionary Agent Documentation](./EvolutionaryAgent.md): Detailed information about the implementation of the Evolutionary Agent used in this project, including how it enhances reinforcement learning performance.

## Custom Reinforcement Learning Environment

The `CustomPyEnvironment` is a custom implementation of the `PyEnvironment` provided by `TF-Agents`. This environment defines the:
- **Action Space**: Move left, move right, or fine adjustment.
- **Observation Space**: A normalized frame of the game screen.
- **Reward System**: Rewards for aligning the paddle with the ball, destroying blocks, and avoiding the ball falling.

## Evolutionary Agent

For more detailed information on the implementation of the Evolutionary Agent used in this project, including how it applies evolutionary algorithms to enhance the performance in reinforcement learning scenarios, please refer to the [Evolutionary Agent Documentation](./EvolutionaryAgent.md).

The Evolutionary Agent was a major step in improving the efficiency of reinforcement learning for the Block-Bricks game. The detailed documentation covers:
- **Population Initialization**
- **Evaluation and Selection Process**
- **Crossover and Mutation Mechanics**
- **Fitness Tracking Over Generations**

Feel free to explore the complete document for insights into how these concepts were implemented and how they contributed to the success of this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributions

Contributions are welcome! Feel free to open issues or pull requests with improvements and suggestions.

## Contact

For any questions or collaboration opportunities, please contact me:

- **Email**: [gabbryellimasi@gmail.com](mailto:gabbryellimasi@gmail.com)

