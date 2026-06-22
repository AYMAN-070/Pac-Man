# Project Timeline (Kanban Approach)

### Phase 1: Architecture & Parsing
- [x] Set up the `GameEngine` skeleton.
- [x] Create a robust `config.json` parser.
- [x] Set up CI/CD tools (Makefile, Mypy, Linters).

### Phase 2: Algorithms & Mazes (ayhammou)
- [x] Connect the external `A-Maze-ing` generator.
- [x] Create the fallback `dummy_grid` system for crash prevention.
- [x] Implement the BFS pathfinding algorithm.
- [x] Write the logic to break walls and connect isolated corners.

### Phase 3: Interface, Graphics, Audio & Gameplay (abenabde)
- [x] Organize a safe SDL2 initialization sequence with structured resource management (try/destroy/free chains).
- [x] Design and implement the SDL2 game loop: event polling, framerate capping, and state routing.
- [x] Implement Pac-Man movement (`update_pos`, `rail_movements`) and Ghost AI behavior.
- [x] Build the full rendering layer using SDL2 and the `GameEngine` state (maze, entities, HUD).
- [x] Design the UI: Main Menu, Pause Screen, Instructions, Scores, Game Over, and Victory screens.
- [x] Integrate the audio engine (SDL2_mixer): background music, sound effects, and music toggle.
- [x] Create all game assets (sprites, backgrounds, fonts, sounds) using GIMP and Audacity.

### Phase 4: Debugging & Polish
- [x] Fix the infinite loop bug in Cheat Mode.
- [x] Adjust dynamic difficulty timers.
- [x] Finalize packaging (PyInstaller) and create deployment scripts.
