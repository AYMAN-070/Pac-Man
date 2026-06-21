
import sdl2.ext.image as s2_img
import sdl2.sdlttf as s2_ttf
import sdl2.sdlmixer as s2_mix
import sdl2 as s2
import ctypes
from typing import Any
import time
import random

from engine import GameEngine
from ghost import GhostState
from player import Direction
from display_base import BaseDisplay

class DisplayGame(BaseDisplay):

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
            case Direction.DOWN:
                row = 1
            case _:
                w, h = 250, 250
                src = s2.SDL_Rect(2 * w, 3 * h, w, h)
                dst = s2.SDL_Rect(int(self.player.xf * self.cell + padx), int(self.player.yf * self.cell + pady), self.cell, self.cell)
                s2.SDL_RenderCopy(self.renderer, self.t["sprit_pacman"], src, dst)
                return
        col = self.rotasprit
        w, h = 250, 250
        src = s2.SDL_Rect(col * w, row * h, w, h)
        dst = s2.SDL_Rect(int(self.player.xf * self.cell + padx), int(self.player.yf * self.cell + pady), self.cell, self.cell)
        s2.SDL_RenderCopy(self.renderer, self.t["sprit_pacman"], src, dst)

    def draw_ghosts(self, padx: int, pady: int) -> None:
        """  """ #  TODO

        for i, ghost in enumerate(self.ghosts):
            if not ghost.state == GhostState.DEAD:
                color = self.ghost_color[ghost.color_id]
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
                    s2.SDL_SetTextureColorMod(self.t[color], 110, 80, 220)
                else:
                    s2.SDL_SetTextureColorMod(self.t[color], 255, 255, 255)

                col = ghost.rotasprit
                w, h = 250, 250
                src = s2.SDL_Rect(col * w, row * h, w, h)
                dst = s2.SDL_Rect(int(ghost.xf * self.cell + padx), int(ghost.yf * self.cell + pady), self.cell, self.cell)
                s2.SDL_RenderCopy(self.renderer, self.t[color], src, dst)

    def draw_infos(self) -> None:
        """  """ #  TODO

        s_score = f"{self.engine.score}"
        self.draw_text(s_score, self.midxy[0] - 20, 15, len(s_score) * 20, 50, self.font1, "orange")

        dst = s2.SDL_Rect(self.midxy[0] - 200, 5, 165, 70)        
        s2.SDL_RenderCopy(self.renderer, self.t["score"], None, dst)

        dst = s2.SDL_Rect(int(self.midxy[0] / 6 - 100), 150, 160, 70)        
        s2.SDL_RenderCopy(self.renderer, self.t["lives"], None, dst)
        
        dst = s2.SDL_Rect(int(self.midxy[0] / 3 ), -10, 130, 100)        
        s2.SDL_RenderCopy(self.renderer, self.t["level"], None, dst)
        s_level = f"{self.engine.current_level}"
        self.draw_text(s_level, int(self.midxy[0] / 3) + 140, 0, len(s_level) * 50, 80, self.font2, "blue")

        dst = s2.SDL_Rect(self.midxy[0] - 400, self.midxy[1] * 2 - 150, 420, 140)        
        s2.SDL_RenderCopy(self.renderer, self.t["time"], None, dst)
        s_time = f"{round(self.engine.time_left, 2)}"
        self.draw_text(s_time, self.midxy[0] + 30, self.midxy[1] * 2 - 105, len(s_time) * 20, 50, self.font1, "white")

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

    def game_over_process(self, padx: int, pady: int) -> str:

        self.sprits_rate -= 0.5
        if self.rotadeath < 6.1:
            self.rotadeath += 0.1
            row = int(self.rotadeath)
        else:
            row = 7
        
        w, h = 600, 250
        src = s2.SDL_Rect(0, row * h, w, h)
        dst = s2.SDL_Rect(int(self.player.xf * self.cell + padx), int(self.player.yf * self.cell + pady), round(self.cell / 250 * 600), self.cell)
        s2.SDL_RenderCopy(self.renderer, self.t["sprit_pacman_death"], src, dst)

        msg = "GAME   OVER"
        w = int(110 * len(msg))
        h = 500
        x = int(self.midxy[0] - w / 2)
        y = int(self.midxy[1] - h / 2)
        self.draw_text(msg, x, y, w, h, self.font2, "black")

        if not self.end:
            self.s.set_background_sound("death_sound", 0)
            self.end = True
            self.time = time.time()
        now = time.time()
        if now - self.time > 5:
            return "end"
        return ""

    def game_win_process(self, padx: int, pady: int) -> str:

        self.sprits_rate -= 0.5
        if self.rotadeath < 4.1:
            self.rotadeath += 0.1
            col = int(self.rotadeath)
        else:
            col = 5
        
        w, h = 250, 250
        src = s2.SDL_Rect(col * w, 2 * h, w, h)
        dst = s2.SDL_Rect(int(self.player.xf * self.cell + padx), int((self.player.yf - self.rotadeath * 2 / 10) * self.cell + pady), self.cell, self.cell)
        s2.SDL_RenderCopyEx(self.renderer, self.t["sprit_pacman"], src, dst, self.rotadeath * 2, None, s2.SDL_FLIP_NONE)

        # src = s2.SDL_Rect(col * w, row * h, w, h)
        # dst = s2.SDL_Rect(int(self.player.xf * self.cell + padx), int(self.player.yf * self.cell + pady), self.cell, self.cell)

        msg = "YOU   WIN"
        w = int(110 * len(msg))
        h = 500
        x = int(self.midxy[0] - w / 2)
        y = int(self.midxy[1] - h / 2)
        self.draw_text(msg, x, y, w, h, self.font2, "green")

        if not self.end:
            self.s.set_background_sound("win_sound", 0)
            self.end = True
            self.time = time.time()
        now = time.time()
        if now - self.time > 5:
            return "end"
        return ""

    def display_and_compute_game(self) -> str:
        """  """ #  TODO

        s2.SDL_RenderClear(self.renderer)
        if self.score_trace != self.engine.score:
            channel = s2_mix.Mix_PlayChannel(-1, self.sounds[random.choice(self.eat_sounds)], 0)
            if channel == -1:
                print("cant play sound, verifie a audio device is available", file=sys.stderr)
        self.score_trace = self.engine.score
        
        lives = self.player.lives
        level = self.engine.current_level
        if self.player.next_direction != Direction.NONE:
            self.engine.update(self.delta_time)
        if self.player.lives != lives:
            channel = s2_mix.Mix_PlayChannel(-1, self.sounds["left_life_sound"], 0)
        player_distx_0 = (self.cell * self.player.xf + self.cell / 2)
        player_disty_0 = (self.cell * self.player.yf + self.cell / 2)

        if self.pov_rpg:
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
                    case 3:  # SUPERPACGUM
                        self.draw_cell("megapacgum", posx, posy)
                posx += self.cell
            posy += self.cell
  
        padx = startx - self.cell / 2
        pady = starty - self.cell / 2
        self.draw_ghosts(padx, pady)
        if self.engine.is_game_over or self.engine.is_victory:
            if self.engine.is_victory:
                end = self.game_win_process(padx, pady)
            else:
                end = self.game_over_process(padx, pady)
            if end:
                self.draw_infos()
                self.rotate_all_sprits()
                s2.SDL_RenderPresent(self.renderer)
                return end
        else:
            self.draw_pacman(padx, pady)
        self.draw_infos()
        self.rotate_all_sprits()
        s2.SDL_RenderPresent(self.renderer)
        
        if level != self.engine.current_level:
            self.init_engine()


