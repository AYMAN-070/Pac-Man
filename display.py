
import sdl2.ext.image as s2_img
import sdl2.sdlttf as s2_ttf
import sdl2 as s2
import ctypes
from typing import Any
import time

from engine import GameEngine
from ghost import GhostState

CELL = 50

class DiplayError(Exception):
    """  """ # TODO
    pass


class Display:
    """  """ # TODO

    def __init__(self, engine: GameEngine, fps_limit: int,
                 renderer: Any, textures: dict[str, Any],
                 font: Any, midxy: list[int]) -> None:
        """  """ # TODO
        self.engine = engine
        self.maze = self.engine.maze.grid
        self.player = self.engine.player
        self.ghosts = self.engine.ghosts

    
        self.delta_time = fps_limit / 1000
        self.renderer = renderer
        self.t = textures
        self.font = font
        self.midxy = midxy

        self.txt_color = s2.SDL_Color(255, 255, 255, 255)

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

        dst = s2.SDL_Rect(x, y, CELL, CELL)
        s2.SDL_RenderCopy(self.renderer, self.t[cell], None, dst)

    def draw_pacman(self, padx: int, pady: int) -> None:
        """  """ #  TODO
        
        dst = s2.SDL_Rect(self.player.x * CELL + padx, self.player.y * CELL + pady, CELL, CELL)
        s2.SDL_RenderCopy(self.renderer, self.t["pacman1"], None, dst)

    def draw_ghosts(self, padx: int, pady: int) -> None:
        """  """ #  TODO

        for ghost in self.ghosts:
            if not ghost.state == GhostState.DEAD:
                dst = s2.SDL_Rect(ghost.x * CELL + padx, ghost.y * CELL + pady, CELL, CELL)
                s2.SDL_RenderCopy(self.renderer, self.t["fantom"], None, dst)

    def draw_text(self, string: str,
                  x: int, y: int,
                  w: int, h: int) -> None:

        surface = s2_ttf.TTF_RenderText_Solid(self.font, string.encode(), self.txt_color)
        texture = s2.SDL_CreateTextureFromSurface(self.renderer, surface)
        s2.SDL_FreeSurface(surface)
        dst = s2.SDL_Rect(x, y, w, h)        
        s2.SDL_RenderCopy(self.renderer, texture, None, dst)
        s2.SDL_DestroyTexture(texture)

    def draw_infos(self) -> None:
        """  """ #  TODO

        s_score = f"{self.engine.score}"
        self.draw_text(s_score, self.midxy[0] - 20, 15, len(s_score) * 20, 50)

        dst = s2.SDL_Rect(self.midxy[0] - 200, 5, 160, 70)        
        s2.SDL_RenderCopy(self.renderer, self.t["score"], None, dst)

        dst = s2.SDL_Rect(int(self.midxy[0] / 6 - 100), 150, 160, 70)        
        s2.SDL_RenderCopy(self.renderer, self.t["lives"], None, dst)
        
        dst = s2.SDL_Rect(int(self.midxy[0] / 3 ), -10, 130, 100)        
        s2.SDL_RenderCopy(self.renderer, self.t["level"], None, dst)

        dst = s2.SDL_Rect(self.midxy[0] - 400, self.midxy[1] * 2 - 150, 420, 140)        
        s2.SDL_RenderCopy(self.renderer, self.t["time"], None, dst)

        s_time = f"{round(self.engine.time_left, 2)}"
        self.draw_text(s_time, self.midxy[0] + 30, self.midxy[1] * 2 - 100, len(s_time) * 20, 50)

        col = self.player.lives - 1
        row = 0
        w, h = 150, 300
        src = s2.SDL_Rect(col * w, row * h, w, h)
        dst = s2.SDL_Rect(int(self.midxy[0] / 6) + 40, 135, 100, 130)
        s2.SDL_RenderCopy(self.renderer, self.t['sprit_lifes'], src, dst)

    def display_game(self) -> None:
        """  """ #  TODO

        s2.SDL_RenderClear(self.renderer)
        
        self.engine.update(self.delta_time)

        player_distx_0 = (CELL * self.player.x + CELL / 2)
        player_disty_0 = (CELL * self.player.y + CELL / 2)

        if False:
            startx = int(self.midxy[0] - player_distx_0)
            starty = int(self.midxy[1] - player_disty_0)
            posy = starty
        else:
            startx = int(self.midxy[0] - CELL * len(self.maze) / 2)
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
                posx += CELL
            posy += CELL
    
        self.draw_ghosts(startx, starty)
        self.draw_pacman(startx, starty) 
        self.draw_infos()

        s2.SDL_RenderPresent(self.renderer)

