# Python Game

## Overview
This project is a small game where players progress through levels by connecting numbered grids. Each level generates a grid of squares based on the level number, and players must click on the grids to display numbers sequentially until they connect all numbers from 1 to n.

## Project Structure
```
python-game
├── src
│   ├── game.py        # Main entry point of the game
│   ├── level.py       # Level class for grid generation and logic
│   ├── grid.py        # Grid class for individual grid management
│   └── utils.py       # Utility functions for the game
├── requirements.txt    # List of dependencies
└── README.md           # Project documentation
```

## Installation
To run the game, you need to install the required dependencies. You can do this by running the following command in your terminal:

```
pip install -r requirements.txt
```

## Running the Game
After installing the dependencies, you can start the game by executing the following command:

```
python src/game.py
```

## How To Play

Press F1 is save level
press F5 is refresh current level


## Game Mechanics
- Each level consists of a grid of squares, with the number of squares equal to the level number.
- Players must click on the grids to reveal numbers sequentially.
- Numbers can only connect adjacently at right angles.
- Once all grids are connected from 1 to n, the player advances to the next level.
- Clicked grids cannot be clicked again.

Enjoy the game and challenge yourself to connect all the numbers!