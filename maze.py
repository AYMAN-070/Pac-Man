from typing import List, Any
try:
    import mazegenerator
    MAZE_GENERATOR_AVAILABLE = True
except ImportError:
    MAZE_GENERATOR_AVAILABLE = False


class Maze:
    """
    Manages the maze structure, walls, pacgums, and super-pacgums.
    """

    def __init__(self, width: int, height: int, seed: int) -> None:
        """
        Initializes the maze properties and generates the grid.
        """
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
            generator = mazegenerator.MazeGenerator(
                size=(self.width, self.height),
                perfect=False,
                seed=self.seed
            )
            generator.generate()
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
        else:
            raise ValueError(f"Unreadable external format: {type(raw_maze)}")
        # CHECK DIMENSIONS
        self.height = len(temp_grid)
        self.width = len(temp_grid[0]) if self.height > 0 else 0
        if self.height < 5 or self.width < 5:
            raise ValueError("External maze is too small.")
        # ADAPT THE CONTENT
        self.grid = [[0 for _ in range(self.width)]
                     for _ in range(self.height)]
        # TRICK: The top-left corner [0][0] is always part of a wall
        wall_symbol = temp_grid[0][0]
        for y in range(self.height):
            for x in range(self.width):
                if temp_grid[y][x] == wall_symbol:
                    self.grid[y][x] = 1
                else:
                    self.grid[y][x] = 0

    def _create_dummy_grid(self) -> None:
        """
        Creates a basic fallback maze if the external generator fails.
        1 = Wall, 0 = Corridor
        """
        self.grid = [[0 for _ in range(self.width)]
                     for _ in range(self.height)]
        for x in range(self.width):
            self.grid[0][x] = 1
            self.grid[self.height - 1][x] = 1
        for y in range(self.height):
            self.grid[y][0] = 1
            self.grid[y][self.width - 1] = 1

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

    def is_wall(self, x: int, y: int) -> bool:
        """
        Allows the Game Engine to know if a coordinate is a wall.
        """
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        return self.grid[y][x] == 1
