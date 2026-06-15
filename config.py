import json
import sys
from typing import Any, Dict


class GameConfig:
    """
    Manange charging and validation of config game
    """
    def __init__(self, filepath: str) -> None:
        """
        Initialise config with path file and default values.
        """
        self.filepath = filepath
        self.settings: Dict[str, Any] = {
            "highscore_filename": "highscores.json",
            "lives": 3,
            "pacgum": 42,
            "points_per_pacgum": 10,
            "points_per_super_pacgum": 50,
            "points_per_ghost": 200,
            "seed": 42,
            "level_max_time": 90.0,
            "level": [
                {"width": 21, "height": 21},  # Niveau 1
                {"width": 25, "height": 25},  # Niveau 2
                {"width": 31, "height": 31}   # Niveau 3
            ]
        }
        self.load_config()

    def _remove_comments(self, json_string: str) -> str:
        """
       delete lines starting with '#'
        """
        lines = json_string.split('\n')
        cleaned_lines = [line for line in lines
                         if not line.strip().startswith('#')]
        return '\n'.join(cleaned_lines)

    def load_config(self) -> None:
        """
        Charge JSON file, ignore comments & update params.
        handle errors properly
        """
        try:
            with open(self.filepath, 'r', encoding='utf-8') as file:
                raw_content = file.read()
            clean_content = self._remove_comments(raw_content)
            user_settings = json.loads(clean_content)
            for key, value in user_settings.items():
                if key in self.settings:
                    self.settings[key] = value
                else:
                    pass
            print(f"Configuration successfully loaded from {self.filepath}")
        except FileNotFoundError:
            print(f"Warning: The file '{self.filepath}' could not be found. "
                  f"Using default settings.")
        except json.JSONDecodeError:
            print(f"Warning: The file '{self.filepath}' contains invalid "
                  f"formatiting. Using default settings.")
        except Exception:
            print("Unexpected warning while reading the configuration."
                  "Using default settings.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error. Usage : python3 pac-man.py config.json")
    else:
        config = GameConfig(sys.argv[1])
        print("Parameters ready for the game: ", config.settings)
