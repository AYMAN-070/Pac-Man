from typing import List, Any
try:
    import mazegenerator
    MAZE_GENERATOR_AVAILABLE = True
except ImportError:
    MAZE_GENERATOR_AVAILABLE = False
import random


class Maze:
    """
    Manages the maze structure, walls, pacgums, and super-pacgums.
    """

    def __init__(self, width: int, height: int, seed: int) -> None:
        """
        Initializes the maze properties and generates the grid.
        """
        if width % 2 == 0:
            width += 1
        if height % 2 == 0:
            height += 1
        self.width: int = width
        self.height: int = height
        self.seed: int = seed
        # (0 = path, 1 = wall, 2 = pacgum, 3 = super-pacgum)
        self.grid: List[List[int]] = []
        self.generate_maze()

    def generate_maze(self) -> None:
        """
        Calls the external 'A-Maze-ing' package to create the maze.
        """
        try:
            if not MAZE_GENERATOR_AVAILABLE:
                raise ImportError("Mazegenerator package is not installed.")
            current_seed = self.seed
            random.seed(current_seed)
            generator = mazegenerator.MazeGenerator(
                size=(self.width // 2, self.height // 2),
                perfect=False,
                seed=current_seed
            )
            generator.generate(seed=current_seed)
            raw_maze = generator.maze
            self._parse_external_maze(raw_maze)
            self._place_items()
            print("Maze generated successfully using external package")
        except Exception as e:
            print(f"Warning: External maze generator failed ({e}), "
                  f"creat fallback maze")
            self._create_dummy_grid()
            self._place_items()

    def _parse_external_maze(self, raw_maze: Any) -> None:
        """
        Adapts the size and content of the external maze intelligently,
        """
        temp_grid = []
        if isinstance(raw_maze, list) and len(raw_maze) > 0:
            temp_grid = raw_maze
        elif hasattr(raw_maze, 'grid') and isinstance(raw_maze.grid, list):
            temp_grid = raw_maze.grid
        elif hasattr(raw_maze, 'maze') and isinstance(raw_maze.maze, list):
            temp_grid = raw_maze.maze
        gen_height = len(temp_grid)
        gen_width = len(temp_grid[0])
        self.grid = [[1 for _ in range(self.width)]
                     for _ in range(self.height)]

        for y in range(gen_height):
            for x in range(gen_width):
                cell = temp_grid[y][x]
                px = x * 2 + 1
                py = y * 2 + 1
                if py >= self.height or px >= self.width:
                    continue
                self.grid[py][px] = 0
                if not (cell & 1) and py - 1 >= 0:          # Nord (1)
                    self.grid[py - 1][px] = 0
                if not (cell & 2) and px + 1 < self.width:  # Est (2)
                    self.grid[py][px + 1] = 0
                if not (cell & 4) and py + 1 < self.height:    # Sud (4)
                    self.grid[py + 1][px] = 0
                if not (cell & 8) and px - 1 >= 0:          # Ouest (8)
                    self.grid[py][px - 1] = 0
        self.carve_center()

    def pattern_42(self) -> None:
        """Reserve pattern 42 coordinates so that it is not sculpted."""
        self.pattern = set()
        if self.height < 10 or self.width < 10:
            print("Warning: Maze size too small to draw the 42 pattern")
            return
        cx = self.width // 2
        cy = self.height // 2
        offsets = {
            (-3, -2), (-3, -1), (-3, 0), (-2, 0), (-1, 0), (-1, 1), (-1, 2),
            (1, -2), (2, -2), (3, -2), (3, -1), (3, 0), (2, 0), (1, 0), (1, 1),
            (1, 2), (2, 2), (3, 2)
        }
        self.pattern.update(
            (cx + dx, cy + dy) for dx, dy in offsets
            if 0 <= (cx + dx) < self.width and 0 <= (cy + dy) < self.height
        )

    def carve_center(self) -> None:
        """Creuse le centre et dessine le logo 42"""
        center_x = self.width // 2
        center_y = self.height // 2
        # empty center
        for y in range(center_y - 4, center_y + 5):
            for x in range(center_x - 6, center_x + 7):
                if 0 < y < self.height - 1 and 0 < x < self.width - 1:
                    self.grid[y][x] = 0
        self.pattern_42()
        for x, y in self.pattern:
            self.grid[y][x] = 1

    def _create_dummy_grid(self) -> None:
        """
        Creates a basic fallback maze if the external generator fails.
        1 = Wall, 0 = Corridor
        """
        self.grid = [[0 for _ in range(self.width)]
                     for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                if (x == 0 or x == self.width - 1
                        or y == 0 or y == self.height - 1):
                    self.grid[y][x] = 1
                elif x % 2 == 0 and y % 2 == 0:
                    self.grid[y][x] = 1
        self._carve_center()

    def _place_items(self) -> None:
        """
        Places pacgums and super-pacgums on the grid according to the rules.
        """
        # Super-pacgums in the 4 corners
        self.grid[1][1] = 3   # Top-Left
        self.grid[1][self.width - 2] = 3  # Top-Right
        self.grid[self.height - 2][1] = 3   # Bottom-Left
        self.grid[self.height - 2][self.width - 2] = 3    # Bottom-Right
        # Pacgums in most corridors
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.grid[y][x] == 0:
                    self.grid[y][x] = 2
        self.grid[self.height // 2][self.width // 2] = 0

    def is_wall(self, x: int, y: int) -> bool:
        """
        Allows the Game Engine to know if a coordinate is a wall.
        """
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        return self.grid[y][x] == 1
