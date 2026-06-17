
import sdl2.ext.image as s2_img
import sdl2.sdlttf as s2_ttf
import sdl2 as s2
import ctypes
from typing import Any
import time
import random

from engine import GameEngine
from ghost import GhostState
from player import Direction

class DiplayError(Exception):
    """  """ # TODO
    pass


class Display:
    """  """ # TODO

    def __init__(self, engine: GameEngine, fps_limit: int,
                 renderer: Any, textures: dict[str, Any],
                 font1: Any, font2: Any, midxy: list[int]) -> None:
        """  """ # TODO
        self.engine = engine
        self.init_engine()

        self.rotasprit = 3
        self.n_rotasprit = 4
        self.sprits_rate = 0
    
        self.p_direction = ""
        self.delta_time = fps_limit / 1000
        self.renderer = renderer
        self.t = textures
        self.font1 = font1
        self.font2 = font2
        self.midxy = midxy
        self.cell = 0

        self.txt_color = s2.SDL_Color(255, 255, 255, 255)

    def init_engine(self):
        """  """ #  TODO

        self.maze = self.engine.maze.grid
        self.player = self.engine.player
        self.ghosts = self.engine.ghosts
        for ghost in self.ghosts:
            ghost.rotasprit = random.randint(0, 4)

    def display_menu(self) -> None:
        """  """ #  TODO
        s2.SDL_RenderClear(self.renderer)

        jump = 200
        pading = 200
        w = 400
        h = 200
        pos_w = int(self.midxy[0] -  (w/ 2))

        dst = s2.SDL_Rect(int(self.midxy[0] -  (800 / 2)), -50, 800, 500)
        s2.SDL_RenderCopy(self.renderer, self.t['menu_title'], None, dst)

        dst = s2.SDL_Rect(pos_w, jump + pading, w, h)
        s2.SDL_RenderCopy(self.renderer, self.t['menu_newgame'], None, dst)

        dst = s2.SDL_Rect(pos_w, jump + pading * 2, w, h)
        s2.SDL_RenderCopy(self.renderer, self.t['menu_scores'], None, dst)

        dst = s2.SDL_Rect(pos_w, jump + pading * 3, w, h)
        s2.SDL_RenderCopy(self.renderer, self.t['menu_instructions'], None, dst)

        dst = s2.SDL_Rect(int(self.midxy[0] -  ((w - 100)/ 2)), jump + pading * 4, w - 100, h - 80)
        s2.SDL_RenderCopy(self.renderer, self.t['menu_exit'], None, dst)

        s2.SDL_RenderPresent(self.renderer)

    def get_buttons(self) -> dict[str, Any]:
        """  """ #  TODO
        data = dict()

        jump = 210
        pading = 200
        w = 400
        h = 200
        pos_w = int(self.midxy[0] -  (w/ 2))

        w_lu = self.midxy[0] - 155  # left up
        w_rd = self.midxy[0] + 155  # right down

        h_lu = jump + pading
        h_rd = h_lu + 180
        inside = {"lu": (w_lu, h_lu), "rd": (w_rd, h_rd)}
        data.update({"newgame": inside})

        h_lu = jump + pading * 2
        h_rd = h_lu + 180
        inside = {"lu": (w_lu, h_lu), "rd": (w_rd, h_rd)}
        data.update({"scores": inside})

        h_lu = jump + pading * 3
        h_rd = h_lu + 180
        inside = {"lu": (w_lu, h_lu), "rd": (w_rd, h_rd)}
        data.update({"instructions": inside})

        h_lu = jump + pading * 4
        h_rd = h_lu + 110
        inside = {"lu": (w_lu, h_lu), "rd": (w_rd, h_rd)}
        data.update({"exit": inside})

        return data

    def draw_cell(self, cell: str, x, y) -> None:
        """  """ #  TODO

        dst = s2.SDL_Rect(x, y, self.cell, self.cell)
        s2.SDL_RenderCopy(self.renderer, self.t[cell], None, dst)

    def draw_pacman(self, padx: int, pady: int) -> None:
        """  """ #  TODO
        match self.player.next_direction:
            case Direction.UP:
                row = 0
            case Direction.LEFT:
                row = 2
            case Direction.RIGHT:
                row = 3
            case _:
                row = 1
        col = self.rotasprit
        w, h = 250, 250
        src = s2.SDL_Rect(col * w, row * h, w, h)
        
        dst = s2.SDL_Rect(int(self.player.xf * self.cell + padx), int(self.player.yf * self.cell + pady), self.cell, self.cell)
        s2.SDL_RenderCopy(self.renderer, self.t["sprit_pacman"], src, dst)

    def draw_ghosts(self, padx: int, pady: int) -> None:
        """  """ #  TODO

        for i, ghost in enumerate(self.ghosts):
            if not ghost.state == GhostState.DEAD:
                match ghost.direction:
                    case "UP":
                        row = 0
                    case "LEFT":
                        row = 2
                    case "RIGHT":
                        row = 3
                    case _:
                        row = 1
                if ghost.state == GhostState.EDIBLE:
                    s2.SDL_SetTextureColorMod(self.t['sprit_ghost1'], 100, 150, 255)
                else:
                    s2.SDL_SetTextureColorMod(self.t['sprit_ghost1'], 255, 255, 255)

                col = ghost.rotasprit
                w, h = 250, 250
                src = s2.SDL_Rect(col * w, row * h, w, h)
                dst = s2.SDL_Rect(int(ghost.xf * self.cell + padx), int(ghost.yf * self.cell + pady), self.cell, self.cell)
                s2.SDL_RenderCopy(self.renderer, self.t['sprit_ghost1'], src, dst)

    def draw_text(self, string: str,
                  x: int, y: int,
                  w: int, h: int,
                  font: Any) -> None:

        surface = s2_ttf.TTF_RenderText_Solid(font, string.encode(), self.txt_color)
        texture = s2.SDL_CreateTextureFromSurface(self.renderer, surface)
        s2.SDL_FreeSurface(surface)
        dst = s2.SDL_Rect(x, y, w, h)        
        s2.SDL_RenderCopy(self.renderer, texture, None, dst)
        s2.SDL_DestroyTexture(texture)

    def draw_infos(self) -> None:
        """  """ #  TODO

        s_score = f"{self.engine.score}"
        self.draw_text(s_score, self.midxy[0] - 20, 15, len(s_score) * 20, 50, self.font1)

        dst = s2.SDL_Rect(self.midxy[0] - 200, 5, 165, 70)        
        s2.SDL_RenderCopy(self.renderer, self.t["score"], None, dst)

        dst = s2.SDL_Rect(int(self.midxy[0] / 6 - 100), 150, 160, 70)        
        s2.SDL_RenderCopy(self.renderer, self.t["lives"], None, dst)
        
        dst = s2.SDL_Rect(int(self.midxy[0] / 3 ), -10, 130, 100)        
        s2.SDL_RenderCopy(self.renderer, self.t["level"], None, dst)
        s_level = f"{self.engine.current_level}"
        self.draw_text(s_level, int(self.midxy[0] / 3) + 140, 0, len(s_level) * 50, 80, self.font2)

        dst = s2.SDL_Rect(self.midxy[0] - 400, self.midxy[1] * 2 - 150, 420, 140)        
        s2.SDL_RenderCopy(self.renderer, self.t["time"], None, dst)
        s_time = f"{round(self.engine.time_left, 2)}"
        self.draw_text(s_time, self.midxy[0] + 30, self.midxy[1] * 2 - 105, len(s_time) * 20, 50, self.font1)

        col = self.player.lives - 1
        row = 0
        w, h = 150, 300
        src = s2.SDL_Rect(col * w, row * h, w, h)
        dst = s2.SDL_Rect(int(self.midxy[0] / 6) + 40, 135, 100, 130)
        s2.SDL_RenderCopy(self.renderer, self.t['sprit_lives'], src, dst)

    def rotate_all_sprits(self) -> None:
        if self.sprits_rate == 0:
            for ghost in self.ghosts:
                ghost.rotasprit = (ghost.rotasprit + 1) % 5
            self.n_rotasprit -= 1
            if self.n_rotasprit == -6:
                self.n_rotasprit = 4
            self.rotasprit = abs(self.n_rotasprit)

        self.sprits_rate = (self.sprits_rate + 1) % 5

    def display_game(self) -> None:
        """  """ #  TODO

        s2.SDL_RenderClear(self.renderer)
        level = self.engine.current_level
        self.engine.update(self.delta_time)

        player_distx_0 = (self.cell * self.player.xf + self.cell / 2)
        player_disty_0 = (self.cell * self.player.yf + self.cell / 2)

        if True:
            startx = int(self.midxy[0] - player_distx_0)
            starty = int(self.midxy[1] - player_disty_0)
            posy = starty
        else:
            startx = int(self.midxy[0] - self.cell * len(self.maze) / 2)
            starty = 90
            posy = starty

        for lane in self.maze:
            posx = startx
            for case in lane:
                match case:
                    case 0:  # NOTHING
                        pass
                    case 1:  # WALL
                        self.draw_cell("wall", posx, posy)
                    case 2:  # PACGUM
                        self.draw_cell("pacgum", posx, posy)
                        pass
                    case 3:  # SUPERPACGUM
                        self.draw_cell("megapacgum", posx, posy)
                        pass
                posx += self.cell
            posy += self.cell
  
        padx = startx - self.cell / 2
        pady = starty - self.cell / 2
        self.draw_ghosts(padx, pady)
        self.draw_pacman(padx, pady) 
        self.draw_infos()
        
        self.rotate_all_sprits()
        s2.SDL_RenderPresent(self.renderer)

        if level != self.engine.current_level:
            self.init_engine()

    def draw_return_menu(self) -> None:

        scalex = int(self.midxy[0] / 10)
        scaley = int(self.midxy[1] / 10)
        dst = s2.SDL_Rect(scalex, scaley, 200, 100)
        s2.SDL_RenderCopy(self.renderer, self.t["return_menu"], None, dst)

    def display_escape(self) -> None:
        
        s2.SDL_RenderClear(self.renderer)
        s2.SDL_SetTextureColorMod(self.t['sprit_ghost1'], 65, 50, 80)
        s2.SDL_SetTextureColorMod(self.t['return_menu'], 140, 120, 180)
        
        size = 50

        size_cell = self.cell * size
        w, h = 250, 250
        src = s2.SDL_Rect(0 * w, 1 * h, w, h)

        dst = s2.SDL_Rect(int(self.midxy[0] - size_cell / 2), int(self.midxy[1] - size_cell / 2), size_cell, size_cell)
        s2.SDL_RenderCopy(self.renderer, self.t['sprit_ghost1'], src, dst)

        size = 1000
        dst = s2.SDL_Rect(int(self.midxy[0] - size / 2), int(self.midxy[1] - size / 2), size, size)
        s2.SDL_RenderCopy(self.renderer, self.t["resume"], None, dst)

        
        self.draw_return_menu() 

        s2.SDL_SetTextureColorMod(self.t['sprit_ghost1'], 255, 255, 255)
        s2.SDL_SetTextureColorMod(self.t['return_menu'], 255, 255, 255)
        s2.SDL_RenderPresent(self.renderer)

        
    def display_instructions(self) -> None:

        s2.SDL_RenderClear(self.renderer)

        scalex = int(self.midxy[0] / 10)
        scaley = int(self.midxy[1] / 10)
        dst = s2.SDL_Rect(scalex, scaley, 200, 100)
        s2.SDL_RenderCopy(self.renderer, self.t["return_menu"], None, dst)

        mlp = self.midxy[1] / 1000
        w = 1000 * mlp
        h = 1600 * mlp

        x = self.midxy[0] - w / 2
        y = self.midxy[1] - h / 2

        dst = s2.SDL_Rect(int(x), int(y), int(w), int(h))
        s2.SDL_RenderCopy(self.renderer, self.t["instructions"], None, dst)

        s2.SDL_RenderPresent(self.renderer)
