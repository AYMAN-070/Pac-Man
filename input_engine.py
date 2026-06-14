
import sdl2.ext.image as s2_img
import sdl2 as s2
import ctypes
from enum import IntEnum
import sys

from textures import Textures

class D(IntEnum):  # DEFAULT
    """  """  # TODO

    w: int = 1600
    h: int = 1200

class InputError(Exception):
    """  """  # TODO
    pass

class InputEngine:
    """  """  # TODO

    def __init__(self) -> None:
        """  """  # TODO

        self.fps_limit = int(1000 / 60)  # = 16 for 60 fps
        self.hmid:int = int(D.h / 2)
        self.wmid:int = int(D.w / 2)

        check = s2.SDL_Init(s2.SDL_INIT_EVERYTHING)
        if check != 0:
            raise InputError("Error. Can't init SDL2")
        
        # self.mode = s2.SDL_DisplayMode()

        self.window = s2.SDL_CreateWindow(b"Pacman",
                                     s2.SDL_WINDOWPOS_CENTERED,
                                     s2.SDL_WINDOWPOS_CENTERED,
                                     D.w, D.h,
                                     s2.SDL_WINDOW_SHOWN | s2.SDL_WINDOW_RESIZABLE)
        if not self.window:
            s2.SDL_Quit()
            raise InputError("Error. Can't init window")

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
            s2.SDL_DestroyWindow(self.window)
            s2.SDL_Quit()
            raise InputError("Error. Can't init renderer")
        s2.SDL_SetRenderDrawColor(self.renderer, 12, 15, 50, 255)

        try:
            self.textures = Textures(self.renderer)
            self.t = self.textures.load_textures()
            self.process()
        except Exception:
            raise
        finally:
            self.textures.destroy_all()
            s2.SDL_DestroyRenderer(self.renderer)
            s2.SDL_DestroyWindow(self.window)
            s2.SDL_Quit()

    def limit_fps(self, limit: int) -> None:
        ticks = s2.SDL_GetTicks()
       
        if limit + self.fps_limit > ticks:
            # TOO EARLY
            s2.SDL_Delay(limit + self.fps_limit - ticks)

    def process(self) -> None:
        """  """ #  TODO

        program = True

        while program:
            start_frame = s2.SDL_GetTicks()
            
            self.display_menu()

            event = s2.SDL_Event()
            while s2.SDL_PollEvent(event):
                match event.type:
                    case s2.SDL_QUIT:
                        program = False
                    case s2.SDL_WINDOWEVENT:
                        if event.window.event == s2.SDL_WINDOWEVENT_RESIZED:
                            self.wmid = int(event.window.data1 / 2)
                            self.hmid = int(event.window.data2 / 2)

            self.limit_fps(start_frame)


    def display_menu(self) -> None:
        """  """ #  TODO
        s2.SDL_RenderClear(self.renderer)

        jump = 200
        pading = 200

        w = 400
        h = 200
        pos_w = int(self.wmid -  (w/ 2))

        dst = s2.SDL_Rect(int(self.wmid -  (800 / 2)), -50, 800, 500)
        s2.SDL_RenderCopy(self.renderer, self.t['menu_title'], None, dst)

        dst = s2.SDL_Rect(pos_w, jump + pading, w, h)
        s2.SDL_RenderCopy(self.renderer, self.t['menu_newgame'], None, dst)

        dst = s2.SDL_Rect(pos_w, jump + pading * 2, w, h)
        s2.SDL_RenderCopy(self.renderer, self.t['menu_scores'], None, dst)

        dst = s2.SDL_Rect(pos_w, jump + pading * 3, w, h)
        s2.SDL_RenderCopy(self.renderer, self.t['menu_instructions'], None, dst)

        dst = s2.SDL_Rect(int(self.wmid -  ((w - 100)/ 2)), jump + pading * 4, w - 100, h - 80)
        s2.SDL_RenderCopy(self.renderer, self.t['menu_exit'], None, dst)

        s2.SDL_RenderPresent(self.renderer)

    def display_game(self) -> None:
        """  """ #  TODO

    def test(self) -> None:
        """  """ #  TODO

        windowsurface = s2.SDL_GetWindowSurface(self.window)
        image = s2_img.load_img(b"Untitled.png")
        if not image:
            raise DiplayError("image asset corupted")
        s2.SDL_BlitSurface(image, None, windowsurface, None)

        s2.SDL_UpdateWindowSurface(self.window)
        s2.SDL_FreeSurface(image)


def testing() -> None:  # TODO
    i_e = InputEngine()
    print("created")


testing()
