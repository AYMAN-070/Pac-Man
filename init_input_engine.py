

import sys
import ctypes
from enum import IntEnum
from typing import Callable, Any
try:
    import sdl2 as s2
    import sdl2.ext.image as s2_img
    import sdl2.sdlttf as s2_ttf
    import mazegenerator
except ImportError as e:
    print(f"Error : missing library ({e.name}).")
    print("Solution : lunch 'make run'.")
    sys.exit(1)
from engine import GameEngine
from textures import Textures
from display import Display


class D(IntEnum):  # DEFAULT
    """  """  # TODO

    w: int = 1600
    h: int = 1300

class InputError(Exception):
    """  """  # TODO
    pass

class InitInputEngine:
    """  """  # TODO

    def __init__(self, path: str) -> None:
        """  """  # TODO

        self.fps_limit = 16  # for 60 / 1000 for fps TODO
        self.midxy: list[int] = [int(D.w / 2), int(D.h / 2)]
        self.config_path = path
        self.engine = GameEngine(path)
        self.player = self.engine.player
        self.previous = ""

        if s2_ttf.TTF_Init() != 0:
            raise InputError("Error. Can't init SDL_TTF")
        try:
            self.font1 = s2_ttf.TTF_OpenFont(b"assets/MoonAndLatte-vn8LO.ttf", 24)
            if not self.font1:
                raise InputError("can't load font")
            self.font2 = s2_ttf.TTF_OpenFont(b"assets/Shirtsy-8Z2A.ttf", 50)
            if not self.font2:
                s2_ttf.TTF_CloseFont(self.font1)
                raise InputError("can't load font")
        except Exception:
            s2_ttf.TTF_Quit()
            raise

        check = s2.SDL_Init(s2.SDL_INIT_VIDEO)

        if check != 0:
            self.close_fonts()
            raise InputError("Error. Can't init SDL2")

        self.window = s2.SDL_CreateWindow(b"Pacman",
                                     s2.SDL_WINDOWPOS_CENTERED,
                                     s2.SDL_WINDOWPOS_CENTERED,
                                     D.w, D.h,
                                     s2.SDL_WINDOW_SHOWN | s2.SDL_WINDOW_RESIZABLE)
        if not self.window:
            self.close_fonts()
            raise InputError("Error. Can't init window")
        s2.SDL_SetWindowMinimumSize(self.window, D.w, D.h)

        try:
            self.renderer = s2.SDL_CreateRenderer(
                    self.window,
                    -1,
                    s2.SDL_RENDERER_ACCELERATED
            )
        except:
            print("can't load gpu, loading on cpu")
            self.renderer = s2.SDL_CreateRenderer(
                    self.window,
                    -1,
                    s2.SDL_RENDERER_SOFTWARE
            )
        if not self.renderer:
            self.close_fonts()
            s2.SDL_DestroyWindow(self.window)
            s2.SDL_Quit()
            raise In#putError("Error. Can't init renderer")
        s2.SDL_SetRenderDrawColor(self.renderer, 62, 98, 124, 255)

        try:
            self.textures = Textures(self.renderer)
            self.t = self.textures.load_textures()
            self.d = Display(self.engine, self.fps_limit,
                             self.renderer, self.t, self.font1, self.font2,
                             self.midxy)
            if D.w < D.h:
                self.d.cell = int((D.w - 250) / len(self.d.maze))
            else:
                self.d.cell = int((D.h - 250) / len(self.d.maze))
            if self.d.cell < 50:
                self.d.cell = 50
        except Exception:
            self.free_all()
            raise


    def free_all(self) -> None:
        self.close_fonts()
        self.textures.destroy_all()
        s2.SDL_DestroyRenderer(self.renderer)
        s2.SDL_DestroyWindow(self.window)
        s2.SDL_Quit()

    def close_fonts(self) -> None:
        s2_ttf.TTF_CloseFont(self.font1)
        s2_ttf.TTF_CloseFont(self.font2)
        s2_ttf.TTF_Quit()
