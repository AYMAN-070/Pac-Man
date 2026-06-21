# Project Timeline (Kanban Approach)

### Phase 1: Architecture & Parsing
- [x] Set up the `GameEngine` skeleton.
- [x] Create a robust `config.json` parser.
- [x] Set up CI/CD tools (Makefile, Mypy, Linters).

### Phase 2: Algorithms & Mazes (Ayman)
- [x] Connect the external `A-Maze-ing` generator.
- [x] Create the fallback `dummy_grid` system for crash prevention.
- [x] Implement the BFS pathfinding algorithm.
- [x] Write the logic to break walls and connect isolated corners.

### Phase 3: Interface, Graphics & Gameplay (Partner)
- [x] Integrate SDL2 for graphics and events.
- [x] Implement Pac-Man movement and Ghost AI behavior.
- [x] Design the UI (Main Menu, Pause, Game Over).
- [x] Create the persistent Highscore saving system.

### Phase 4: Debugging & Polish
- [x] Fix the infinite loop bug in Cheat Mode.
- [x] Adjust dynamic difficulty timers.
- [x] Finalize packaging (PyInstaller) and create deployment scripts.