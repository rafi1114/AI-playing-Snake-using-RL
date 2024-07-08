# AI Playing Snake using Reinforcement Learning

[![AI plays Snake!](https://img.youtube.com/vi/HTxfdf0rBZs/0.jpg)](https://www.youtube.com/watch?v=HTxfdf0rBZs&t=13s)


This project demonstrates a reinforcement learning agent that plays the classic Snake game. The agent is trained using Q-learning to optimize its performance in the game.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How it Works](#how-it-works)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/rafi1114/AI-playing-Snake-using-RL.git
   cd AI-playing-Snake-using-RL
   ```

2. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

To train the agent:
```sh
python main.py
```

To test the trained agent:
```sh
python main.py
```

Change the `MODE` variable in `main.py` to switch between training and testing:
```python
MODE = 0 # Training
# or
MODE = 1 # Testing
```

## Project Structure

- `main.py`: Main script to train and test the agent.
- `game.py`: Contains the implementation of the Snake game.
- `plotter.py`: Utility to plot the results of training/testing.
- `qmodel.py`: Contains the Q-learning model.
- `requirements.txt`: List of dependencies.

## How it Works

### Q-Learning

The agent is trained using Q-learning, a type of reinforcement learning where the agent learns to map states to actions in order to maximize cumulative reward. The state of the game includes the snake's position, direction, and the location of the food. The actions include moving left, right, up, and down.

### State Representation

The state is represented by the following features:
- Danger in each direction (left, right, up, down)
- Current direction of the snake
- Relative position of the food (left, right, up, down)

### Training

During training, the agent explores different actions with a probability that decreases as the number of games increases. The agent updates its Q-table based on the rewards received from the game environment.

### Testing

During testing, the agent uses the learned Q-table to make decisions, aiming to achieve the highest score possible without exploration.

## Results

The agent's performance is tracked by the scores achieved in the game. The training and testing results can be visualized using the `plotter.py` utility.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to modify this template as per your project's specifics and needs.
