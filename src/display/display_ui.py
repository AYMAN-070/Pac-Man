
import sdl2.ext.image as s2_img
import sdl2.sdlttf as s2_ttf
import sdl2 as s2
import ctypes
from typing import Any
import time
import random

from engine.engine import GameEngine
from engine.ghost import GhostState
from engine.player import Direction
from display.display_base import BaseDisplay

class DisplayUI(BaseDisplay):

    def draw_background(self) -> None:

        if self.midxy[0] / self.midxy[1] < 16 / 9:
            backh = int((self.midxy[1] + 1) * 2)
            backw = int((backh + 5) / 1080 * 1920)
        else:
            backw = int((self.midxy[0] + 1) * 2)
            backh = int((backw + 5) / 1920 * 1080)
        dst = s2.SDL_Rect(0, 0, backw, backh)
        s2.SDL_RenderCopy(self.renderer, self.t['background'], None, dst)
    
        backw = int(self.midxy[1] * 1.5)
        backh = int(backw / 1080 * 1179)
        dst = s2.SDL_Rect(int(self.midxy[0] * 1.5 - backw / 2), int(self.midxy[1] - backh / 2), backw, backh)

        rotasprit = (self.rotasprit **2) * 2 -1
        s2.SDL_RenderCopyEx(self.renderer, self.t['background_item'], None, dst, rotasprit * 11 * -1, None, s2.SDL_FLIP_NONE)
        self.rotasprit += self.rotadeath / 60
        if self.rotasprit >= 1:
            self.rotadeath = -0.1
        if self.rotasprit <= 0:
            self.rotadeath = 0.1


    def display_menu(self) -> None:
        """  """ #  TODO
        s2.SDL_RenderClear(self.renderer)

        jump = 350
        w = int(self.midxy[1] / 2)
        h = int(self.midxy[1] / 4)
        pading = int(w / 2)
        pos_w = int(self.midxy[0] -  (w/ 2))

        self.draw_background()

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

        self.draw_music_status()

        s2.SDL_RenderPresent(self.renderer)

    def draw_return_menu(self) -> None:

        scalex = int(self.midxy[0] / 10)
        scaley = int(self.midxy[1] / 10)
        dst = s2.SDL_Rect(scalex, scaley, 200, 100)
        s2.SDL_RenderCopy(self.renderer, self.t["return_menu"], None, dst)

    def draw_music_status(self) -> None:
        dst = s2.SDL_Rect(25, self.midxy[1] * 2 - 175, 150, 150)
        if self.s.music_off:
            s2.SDL_RenderCopy(self.renderer, self.t["music_off"], None, dst)
        else:
            s2.SDL_RenderCopy(self.renderer, self.t["music_on"], None, dst)


    def display_escape(self) -> None:
        
        s2.SDL_RenderClear(self.renderer)
        s2.SDL_SetTextureColorMod(self.t['sprit_ghost1'], 65, 50, 80)
        s2.SDL_SetTextureColorMod(self.t['return_menu'], 140, 120, 180)
        s2.SDL_SetTextureColorMod(self.t['music_on'], 140, 120, 180)
        s2.SDL_SetTextureColorMod(self.t['music_off'], 140, 120, 180)
        
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
        self.draw_music_status()

        s2.SDL_SetTextureColorMod(self.t['sprit_ghost1'], 255, 255, 255)
        s2.SDL_SetTextureColorMod(self.t['return_menu'], 255, 255, 255)
        s2.SDL_SetTextureColorMod(self.t['music_on'], 255, 255, 255)
        s2.SDL_SetTextureColorMod(self.t['music_off'], 255, 255, 255)


        s2.SDL_RenderPresent(self.renderer)

    def display_instructions(self) -> None:

        s2.SDL_RenderClear(self.renderer)
        self.draw_background()

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

    def display_scores(self) -> None:

        s2.SDL_RenderClear(self.renderer)
        self.draw_background()

        scalex = int(self.midxy[0] / 10)
        scaley = int(self.midxy[1] / 10)
        dst = s2.SDL_Rect(scalex, scaley, 200, 100)
        s2.SDL_RenderCopy(self.renderer, self.t["return_menu"], None, dst)

        jump = 100
        jumps = 0
        scale = self.midxy[1] / 1000

        x = int(self.midxy[0] - (500) / 2)
        dst = s2.SDL_Rect(x, 0, 500, 300)
        s2.SDL_RenderCopy(self.renderer, self.t['scores'], None, dst)

        i = 0
        random.seed(self.seed)
        for elem in self.engine.highscore_manager.scores:
            
            s_name = f"{elem['name'].upper()} :"
            s_score = f"{elem['score']}"
            ws =  int(len(s_score) * 40 * scale)
            w = int(len(s_name) * 40)


            x = int(self.midxy[0] - (w + ws) / 2)
            y = int(self.midxy[1] / 2 + jump * jumps * scale)
            h = int(100 * scale)
            dst = s2.SDL_Rect(x, y, w, int(h * 1.05))
            s2.SDL_RenderFillRect(self.renderer, dst)
            self.draw_text(s_name, x, y, w, h, self.font2, random.choice(self.colors))
            if i == 0:
                size = int(100 * scale)
                dst = s2.SDL_Rect(x, y - size, size, size)
                s2.SDL_RenderCopy(self.renderer, self.t['crown'], None, dst)

            h = int(80 * scale)
            dst = s2.SDL_Rect(int(x + w + 50), y, ws, int(h * 1.05))
            s2.SDL_RenderFillRect(self.renderer, dst)
            self.draw_text(s_score,int(x + w + 50), y, ws, h, self.font1, random.choice(self.colors))
            jumps += 1
            i += 1
        if i == 0:
            msg = "Nobody succeeded the challenge"
            self.draw_text(msg, int(self.midxy[0] - len(msg) * 40 / 2), self.midxy[1] - 40, len(msg) * 40, 40, self.font1, "black")

        s2.SDL_RenderPresent(self.renderer)

    def display_confirm_quit(self) -> None:

        s2.SDL_RenderClear(self.renderer)

        dst = s2.SDL_Rect(int(self.midxy[0] - 400), self.midxy[1] - 200, 800, 400)
        s2.SDL_RenderCopy(self.renderer, self.t['areyousure'], None, dst)

        s2.SDL_RenderPresent(self.renderer)

    def get_str_sizes(self, data: str) -> tuple[float, float]:

        s_data = f"{data}"
        if data:
            c_min_size = self.midxy[0] * 2 / len(s_data)
        c_size = 50
        w = len(s_data) * c_size
        if data and w > self.midxy[0] * 2:
            c_size = c_min_size
            w = len(s_data) * c_size
        return (int(w), int(c_size))


    def display_end(self) -> None:

        s2.SDL_RenderClear(self.renderer)
       
        w = 330
        h = 140
        dst = s2.SDL_Rect(int(self.midxy[0] - w / 2), 5, w, h)
        s2.SDL_RenderCopy(self.renderer, self.t["score"], None, dst)
        
        if self.i > self.engine.score:
            self.i = self.engine.score
        s_score = f"{self.i}"
        w, c_size = self.get_str_sizes(s_score)
        y = h + 20
        self.draw_text(s_score, int(self.midxy[0] - w / 2), y, w, c_size * 2, self.font1, "orange")

        if self.i != self.engine.score:
            if self.engine.score > 1000000000:
                self.i += 10000000
            if self.engine.score > 100000000:
                self.i += 1000000
            elif self.engine.score > 10000000:
                self.i += 100000
            elif self.engine.score > 1000000:
                self.i += 10000
            elif self.engine.score > 100000:
                self.i += 1000
            elif self.engine.score > 10000:
                self.i += 500
            elif self.engine.score > 1500:
                self.i += 100
            elif self.engine.score > 100:
                self.i += 10
            else:
                self.i += 1
            s2.SDL_RenderPresent(self.renderer)
            return

        y = y + c_size * 2 + 100
        msg = "ENTER YOUR NAME:"
        w, c_size = self.get_str_sizes(msg)
        self.draw_text(msg, int(self.midxy[0] - w / 2), y, w, c_size * 2, self.font2, "yellow")

        #frame = self.delta_time * 1000
        if self.rotasprit == 120:
            self.rotasprit = 0
        self.rotasprit += 1

        txt = self.text
        if len(txt) >= 19:
            self.text = self.text[:19]
            txt = self.text
        w, c_size = self.get_str_sizes(txt)
        y = y + c_size * 2 + 30
        if txt:
            self.draw_text(txt, int(self.midxy[0] - w / 2), y, w, c_size * 3, self.font3, "white")
        if self.rotasprit < 60:
            self.draw_text('_', int(self.midxy[0] - w / 2) + w, y, c_size, c_size * 3, self.font1, "yellow")
        if len(txt) > 10:
            msg = "PLAYER NAME CAN'T EXEED 10 CHARACTERS"
            w = len(msg) * 30
            self.draw_text(msg, int(self.midxy[0] - w / 2), y + 200, w, 40, self.font2, "red")
        elif txt and not txt.isalnum():
            msg = "ONLY ALPHANUMERIC CHARACTERS ARE ALLOWED"
            w = len(msg) * 30
            self.draw_text(msg, int(self.midxy[0] - w / 2), y + 200, w, 40, self.font2, "red")
        s2.SDL_RenderPresent(self.renderer)
