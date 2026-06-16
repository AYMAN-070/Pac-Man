from enum import Enum


class Direction(Enum):
    """
    Defines the 4 possible directions of movement
    """
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    NONE = (0, 0)


class Player:
    """
    Manage stats of pacman
    """
    def __init__(self, start_x: int, start_y: int,
                 starting_lives: int) -> None:
        """
        Initialise player with coordinates
        """
        # actual position
        self.x: int = start_x
        self.y: int = start_y
        self.xf: float = start_x + 0.5
        self.yf: float = start_y + 0.5
        self.destx: float = -1
        self.desty: float = 0
        # Player should reappears in the middle if he dies
        self.start_x: int = start_x
        self.start_y: int = start_y
        # Remaining lives
        self.lives: int = starting_lives
        # Directions
        self.current_direction: Direction = Direction.NONE
        self.next_direction: Direction = Direction.NONE

    def lose_life(self) -> None:
        """
        Handles the loss of a life and makes the player reappear
        at the starting point.
        """
        if self.lives > 0:
            self.lives -= 1
            self.respawn()

    def respawn(self) -> None:
        """
        Return the player to their initial position.
        """
        self.x = self.start_x
        self.y = self.start_y
        self.current_direction = Direction.NONE
        self.next_direction = Direction.NONE
