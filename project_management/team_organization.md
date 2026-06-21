# Team Organization & Responsibilities

Our team divided the work based on our individual strengths while maintaining constant communication to successfully integrate the different modules.

**ayhammou (Core Engine & Algorithms):**
* Designed the main game loop (`GameEngine`) and state management.
* Integrated the external `A-Maze-ing` procedural generator.
* Implemented the BFS (Flood-Fill) algorithm to map reachable areas.and developed the procedural correction logic (`_ensure_corners_accessible`).
* Secured the `config.json` parsing system.

**abenabde (Graphics, UI & Systems):**
* Implemented the graphics rendering using SDL2.
* Managed user inputs and the audio engine.
* Balanced the gameplay by calculating dynamic time limits based on maze size
* Developed the persistent Highscore system and handled the final `.exe` packaging.

**Decision Making Process:**
We communicated daily using Discord. Major technical decisions, such as removing static time limits and handling errors, were made collaboratively after testing the gameplay.