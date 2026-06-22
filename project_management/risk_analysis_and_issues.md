# Risk Analysis & Issue Tracking

During the development phase, we encountered and solved several major technical challenges.

### Risk 1: Procedural Maze Generation Blocking Areas
**Issue:** The external `A-Maze-ing` package sometimes generated walls that completely blocked the 4 corners, making it impossible for the ghosts to spawn or the player to reach the super-pacgums.
**Solution:** We developed a custom BFS algorithm to scan the maze. If a corner is isolated, the engine destroys the minimum amount of walls to reconnect it to the main playable path.

### Risk 2: Gameplay Balancing
**Issue:** A static time limit of 90 seconds made large mazes (e.g., 31x31) mathematically impossible to finish.
**Solution:** We replaced the static timer with a dynamic calculation (`time = accessible_cells / 2.5`), ensuring perfectly balanced difficulty for any randomly generated maze.

### Risk 3: Game Logic & Cheat Mode Exploits
**Issue:** The initial implementation of the "Next Level" cheat mode inadvertently created an infinite loop. By spamming the cheat key, the player could bypass the strict 10-level limit required by the project guidelines, preventing the game from ever reaching the victory screen.
**Solution:** We refactored the cheat mode to align perfectly with the standard win condition. The function now strictly evaluates the level cap and safely triggers the victory state once level 10 is completed.

### Risk 4: SDL2 Resource Management
**Issue:** SDL2 requires explicit destruction of every resource (windows, renderers, textures, fonts, sounds). Any early exit caused by an error risked leaving resources unfreed, leading to crashes or memory leaks.
**Solution:** abenabde designed a structured initialization sequence using try/except blocks with systematic destroy and free calls at every failure point, ensuring safe cleanup regardless of where an error occurs.
