# Acceptance Testing Plan

The following table summarizes the key scenarios we tested to validate the project requirements:

| Feature | Testing Method | Expected Result | Status |
| :--- | :--- | :--- | :--- |
| **JSON Robustness** | Launching the game with a corrupted `config.json` (missing keys or wrong types). | The game applies default values and does not crash (No Python traceback). | Passed |

| **Maze Generation** | Generating 50 consecutive random levels. | Zero crashes. The 4 corners are always accessible and items spawn correctly. | Passed |

| **Win Condition** | Spamming the *Cheat Mode* (Next Level key) up to level 10. | Reaching level 11 triggers the victory screen and stops the game. No infinite loops. | Passed |

| **Highscore Persistence** | Winning a game, entering a name, and restarting 
the application. | The Top 10 displays on the Main Menu with the new score loaded from the local file. | Passed |