from typing import List
import sys
from engine.player import Direction
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

        self.width: int = width
        self.height: int = height
        self.seed: int = seed
        # (0 = path, 1 = wall, 2 = pacgum, 3 = super-pacgum)
        self.grid: List[List[int]] = []
        self.items: List[List[int]] = [[0 for _ in range(width)]
                                       for _ in range(height)]
        self.reachable: set[tuple[int, int]] = set()
        self.generate_maze()

    def generate_maze(self) -> None:
        try:
            if not MAZE_GENERATOR_AVAILABLE:
                raise ImportError("Mazegenerator package is not installed.")
            random.seed(self.seed)
            generator = mazegenerator.MazeGenerator(
                size=(self.width, self.height),
                perfect=False,
                seed=self.seed
            )
            generator.generate(seed=self.seed)
            raw_maze = getattr(generator, 'maze',
                               getattr(generator, 'grid', []))

            self.grid = [[raw_maze[y][x] for x in range(self.width)]
                         for y in range(self.height)]
            print("Maze generated successfully using exact dimensions.")
        except Exception as e:
            print(f"[WARNING] External maze generator failed ({e}).",
                  file=sys.stderr)
            self._create_dummy_grid()
        self._ensure_full_connectivity()
        self._place_items()

    def _ensure_full_connectivity(self) -> None:
        """
        Minimal connection: Only Pac-Man and the Ghosts are connected
        to the main area
        """
        start_x = self.width // 2
        start_y = self.height // 2

        # find principal zone
        self.reachable = self._get_reachable(start_x, start_y)

        # Ensure that the 4 (phantom) corners are connected to this zone.
        essential_points = [(1, 1), (self.width - 2, 1), (1, self.height - 2),
                            (self.width - 2, self.height - 2)]
        for ex, ey in essential_points:
            if (ex, ey) not in self.reachable:
                self._force_connection((ex, ey), (start_x, start_y))
                self.reachable = self._get_reachable(start_x, start_y)

    def _force_connection(self, start, end) -> None:
        """Dig a simple straight path until it connects. """
        cx, cy = start
        tx, ty = end
        while (cx, cy) not in self.reachable:
            # Simple logique de déplacement vers la cible
            dx = 1 if tx > cx else (-1 if tx < cx else 0)
            dy = 1 if ty > cy else (-1 if ty < cy else 0)
            # On casse le mur
            if dx != 0:
                wall_dir = 2 if dx > 0 else 8
                opp_dir = 8 if dx > 0 else 2
            else:
                wall_dir = 4 if dy > 0 else 1
                opp_dir = 1 if dy > 0 else 4

            self.grid[cy][cx] &= ~wall_dir
            cx += dx
            cy += dy
            if 0 <= cx < self.width and 0 <= cy < self.height:
                self.grid[cy][cx] &= ~opp_dir

    def _get_reachable(self, start_x: int, start_y: int) -> set:
        """
        Return all accessible case from (x, y).
        """
        reachable = set()
        queue = [(start_x, start_y)]
        reachable.add((start_x, start_y))
        while queue:
            cx, cy = queue.pop(0)
            for d in [Direction.UP, Direction.DOWN,
                      Direction.LEFT, Direction.RIGHT]:
                if self.can_move(cx, cy, d.name):
                    nx, ny = cx + d.value[0], cy + d.value[1]
                    if (0 <= nx < self.width and 0 <= ny < self.height
                            and (nx, ny) not in reachable):
                        reachable.add((nx, ny))
                        queue.append((nx, ny))
        return reachable

    def find_nearest_empty(self, cx: int, cy: int) -> tuple[int, int]:
        """find case (0) nearest to the center."""
        # On cherche dans un carré grandissant autour du centre
        for radius in range(0, max(self.width, self.height)):
            for y in range(cy - radius, cy + radius + 1):
                for x in range(cx - radius, cx + radius + 1):
                    if 0 <= x < self.width and 0 <= y < self.height:
                        # Si c'est un chemin (valeur 0)
                        if self.grid[y][x] == 0:
                            return (x, y)
        return (cx, cy)

    def _create_dummy_grid(self) -> None:
        """Fallback if package doesn't work"""
        self.grid = [[0 for _ in range(self.width)]
                     for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                cell = 0
                if y == 0:
                    cell += 1               # Mur Nord
                if x == self.width - 1:
                    cell += 2              # Mur Est
                if y == self.height - 1:
                    cell += 4               # Mur Sud
                if x == 0:
                    cell += 8               # Mur Ouest
                self.grid[y][x] = cell

    def _place_items(self) -> None:
        """Parcourt TOUTE la grille et place une Pac-Gum sur chaque chemin."""
        # clear
        self.items = [[0 for _ in range(self.width)]
                      for _ in range(self.height)]

        # On place Super-Pacgums
        corners = [(0, 0), (self.width - 1, 0), (0, self.height - 1),
                   (self.width - 1, self.height - 1)]
        for cx, cy in corners:
            self.items[cy][cx] = 3

        #  place Pac-Gum (2)
        for y in range(self.height):
            for x in range(self.width):
                # Si c'est un chemin (0) et pas déjà une Super-Pacgum (3)
                if self.grid[y][x] != 15 and self.items[y][x] == 0:
                    self.items[y][x] = 2

        # clear the center (spawn)
        cx, cy = self.width // 2, self.height // 2
        self.items[cy][cx] = 0
        count = sum(row.count(2) for row in self.items)
        print(f"DEBUG: J'ai placé {count} Pac-Gums sur la carte.")

    def can_move(self, x: int, y: int, direction: str) -> bool:
        """
        Checks if it is possible to leave cell (x, y) in a given direction.
        direction must be 'UP', 'RIGHT', 'DOWN', or 'LEFT'.
        """
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        cell = self.grid[y][x]
        if direction == 'UP' and not (cell & 1):
            return True
        if direction == 'RIGHT' and not (cell & 2):
            return True
        if direction == 'DOWN' and not (cell & 4):
            return True
        if direction == 'LEFT' and not (cell & 8):
            return True
        return False
