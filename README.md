*This project has been created as part of the 42 curriculum by ayhammou, abenabde.*

# Pac-Man: Procedural Arcade Clone

## Description
This project is a recreation of the classic arcade game **Pac-Man**, developed in Python using the SDL2 library. It features procedural maze generation, intelligent Ghost AI, and a robust Object-Oriented engine.

## Instructions

### Compilation & Execution
The project uses a standard Makefile for easy deployment. Run the following commands in your terminal:

```bash
# Install dependencies
make install

# Run the game
make run
```

### Controls
* **Arrow Keys**: Move Pac-Man up, down, left, or right.
* **ESC**: Pause / Resume the game / Quit the game..
* **/next**: Cheat Mode (Instantly advance to the next level).
* **/cheat**: Cheat Mode (Invincibility mode).

## Configuration
The game is highly customizable via the `config.json` file. 
* **Robust Parsing**: Our parser safely handles comments starting with `#` (which standard JSON does not support) and automatically applies secure fallback values if keys are missing or invalid.
* **Dynamic Balancing**: Instead of static global timers, the engine calculates the time limit for each level dynamically based on the walkable area (`time = accessible_cells / 2.5`).

## Highscore System
We implemented a persistent highscore system. Upon finishing the game (Victory or Game Over), players can input their name (up to 10 alphanumeric characters). The Top 10 scores are saved locally in a persistent file and displayed on the Main Menu.

## Maze Generation & Pathfinding
The game relies on an external procedural generator (`A-Maze-ing`). To ensure the generated mazes are always playable:
1. **Fallback Grid**: A `dummy_grid` is automatically generated if the external package fails.
2. **BFS Flood-Fill**: We implemented a Breadth-First Search algorithm to map reachable areas.
3. **Procedural Correction**: If any of the 4 corners are isolated by walls, the engine breaks the minimum number of walls needed to reconnect them to the main path, ensuring items and ghosts can spawn safely.

## Software Architecture
The architecture strictly follows Object-Oriented Programming (OOP) principles and is fully type-hinted (`mypy` compliant).
* `GameEngine`: Manages the main game loop, frame rendering, and game states (Menu, Playing, Pause, Game Over).
* `Maze`: Handles the grid instantiation, external package adaptation, and procedural wall correction.
* `Entity (Pac-Man & Ghosts)`: Manages collision detection, movement logic, and AI pathfinding.

## Project Management & Packaging
* **Project Documentation**: All management documents (Kanban timeline, task distribution, acceptance testing, and risk analysis) are available in the `/project_management` directory.
* **Packaging**: A deployment script is provided at the root of the repository to package the game into a standalone executable using PyInstaller, making it ready for distribution on platforms like Itch.io.

## Resources & AI Usage
Artificial Intelligence (Gemini/ChatGPT) was used during this project as a technical assistant to:
* Brainstorm and optimize the BFS (Flood-Fill) logic for corner accessibility.
* Debug hardware-specific compatibility issues (e.g., SDL2 Audio segmentation faults on WSL).
* Generate the Mermaid.js syntax for our project management workflow charts.