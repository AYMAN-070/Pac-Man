
import sys
from input_process import InputEngine

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error. Usage : python3 pac-man.py config.json")
        sys.exit(1)
    app = InputEngine(sys.argv[1])
