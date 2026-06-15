
import sdl2.ext.image as s2_img
import sdl2 as s2
import ctypes
from enum import IntEnum
import sys
from typing import Callable

from textures import Textures
from display import Display

def limit_fps(start_frame: int, limit: int) -> None:
    ticks = s2.SDL_GetTicks()
   
    if start_frame + limit > ticks:
        # TOO EARLY
        s2.SDL_Delay(start_frame + limit - ticks)

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

        self.window = s2.SDL_CreateWindow(b"Pacman",
                                     s2.SDL_WINDOWPOS_CENTERED,
                                     s2.SDL_WINDOWPOS_CENTERED,
                                     D.w, D.h,
                                     s2.SDL_WINDOW_SHOWN | s2.SDL_WINDOW_RESIZABLE)
        if not self.window:
            s2.SDL_Quit()
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
            s2.SDL_DestroyWindow(self.window)
            s2.SDL_Quit()
            raise InputError("Error. Can't init renderer")
        s2.SDL_SetRenderDrawColor(self.renderer, 12, 15, 50, 255)

        try:
            self.textures = Textures(self.renderer)
            self.t = self.textures.load_textures()
            self.d = Display(self.renderer, self.t)
            self.process()
        except Exception:
            raise
        finally:
            self.textures.destroy_all()
            s2.SDL_DestroyRenderer(self.renderer)
            s2.SDL_DestroyWindow(self.window)
            s2.SDL_Quit()


    def process(self) -> None:
        """  """ #  TODO
        game = True

        mouse_event = self.menu_mouse
        key_event = lambda *args: None
        display = self.d.display_menu
        while game:
            res = self.core_while(
                    mouse_event,
                    key_event,
                    display
                    )
            match res:
                case "quit":
                    return
                case "menu":
                    mouse_event = self.menu_mouse
                    key_event = lambda *args: None
                case "newgame":
                    print("ng")
                    mouse_event = lambda *args: None
                    key_event = self.newgame_keys


    def core_while(
                self,
                mousebuttonup: Callable[..., str],
                keydown: Callable[..., str],
                display:  Callable[..., str]
                ) -> str:
        """  """ #  TODO

        game = True

        fps_limit = self.fps_limit
        wmid = self.wmid
        hmid = self.hmid
        while game:
            start_frame = s2.SDL_GetTicks()

            event = s2.SDL_Event()
            while s2.SDL_PollEvent(event):
                match event.type:
                    case s2.SDL_QUIT:
                        return "quit"
                    case s2.SDL_WINDOWEVENT:
                        if event.window.event == s2.SDL_WINDOWEVENT_RESIZED:
                            wmid = int(event.window.data1 / 2)
                            hmid = int(event.window.data2 / 2)
                    case s2.SDL_MOUSEBUTTONUP:
                        res = mousebuttonup(event, wmid)
                        if res:
                            return res
                    case s2.SDL_KEYDOWN:
                        res = keydown(event)
                        if res:
                            return res

            display(wmid)
            limit_fps(start_frame, fps_limit)

    def newgame_keys(self, event) -> str:
        """  """ #  TODO
        print("NEW GAME")
        return ""

    def menu_mouse(self, event, wmid) -> str:
        """  """ #  TODO

        if event.button.button == s2.SDL_BUTTON_LEFT:
            act = self.check_button(
                                    wmid, event.button.x,
                                    event.button.y)
            if act:
                return act

    def check_button(self, wmid: int, x: int, y: int) -> str:
        button = self.d.get_buttons(wmid)
        for option in button.keys():
            if button[option]['lu'][0] < x < button[option]['rd'][0]:
                if button[option]['lu'][1] < y < button[option]['rd'][1]:
                    return str(option)
        return ""

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
