# Team Organization & Responsibilities

Our team divided the work based on our individual strengths while maintaining constant communication to successfully integrate the different modules.

**ayhammou (Core Engine & Algorithms):**
* Designed the main game loop (`GameEngine`) and state management.
* Integrated the external `A-Maze-ing` procedural generator.
* Implemented the BFS (Flood-Fill) algorithm to map reachable areas and developed the procedural correction logic (`_ensure_corners_accessible`).
* Secured the `config.json` parsing system.
* Developed the persistent Highscore system.

**abenabde (Graphics, UI, Audio & Systems):**
* Organized a safe SDL2 initialization sequence, including structured resource management (try/destroy/free chains) to prevent memory leaks and crashes.
* Designed and implemented the SDL2 game loop: event polling, framerate capping, and state routing between all game screens.
* Built the full rendering layer using SDL2, leveraging the `GameEngine` state to display the maze, entities, HUD, menus, pause screen, and end screens.
* Created all game assets: sprites, backgrounds, fonts and sounds using GIMP and Audacity.
* Managed user inputs (keyboard and mouse) across all game states.
* Integrated the audio engine (SDL2_mixer): background music, sound effects, and music toggle.
* Balanced the gameplay by calculating dynamic time limits based on maze size.

**Decision Making Process:**
We communicated daily using Discord. Major technical decisions, such as removing static time limits and handling errors, were made collaboratively after testing the gameplay.
