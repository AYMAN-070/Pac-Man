
import sys
import ctypes
from enum import IntEnum
from typing import Callable, Any
import random
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
from player import Direction
from init_input_engine import InitInputEngine


def limit_fps(start_frame: int, limit: int) -> None:
    ticks = s2.SDL_GetTicks()
   
    if start_frame + limit > ticks:
        # TOO EARLY
        s2.SDL_Delay(start_frame + limit - ticks)


class SDLCoreEngine(InitInputEngine):
    """  """  # TODO

    def __init__(self, path: str) -> None:
        """  """  # TODO
        super().__init__(path)
        try:
            self.process()
        except:
            raise
        finally:
            self.free_all()


    def process(self) -> None:
        """  """ #  TODO
        game = True

        res = "menu"
        mouse_event = self.menu_mouse
        key_event = lambda *args: None
        display = self.d.display_menu
        self.s.set_background_sound("menu_sound")
        while game:
            if res != "confirm_quit":
                self.previous = res
            res = self.core_while(
                    mouse_event,
                    key_event,
                    display
                    )
            if res == "confirm_quit":
                if self.previous not in {"menu", "escape"}:
                    res = "menu"

            self.text_mode = False
            self.d.text = ""
            match res:
                case "exit":
                    return
                case "menu":
                    self.s.set_background_sound("menu_sound")
                    if self.previous not in {"instructions", "scores", "menu"}:
                        self.d.rotasprit = 1
                        self.d.rotadeath = -0.1
                    mouse_event = self.menu_mouse
                    key_event = lambda *args: None
                    display = self.d.display_menu
                case "newgame" | "reload":
                    self.s.set_background_sound("game_sound")
                    mouse_event = lambda *args: None
                    key_event = self.newgame_keys
                    display = self.d.display_and_compute_game
                    if self.previous != "escape":
                        if res != "reload":
                            self.engine = GameEngine(self.config_path)
                        self.player = self.engine.player
                        self.d.engine = self.engine
                        self.d.init_engine(self.engine.current_level)
                        self.set_cell_size(self.midxy[0] * 2, self.midxy[1] * 2)
                case "escape":
                    self.s.halt_background_sound()
                    mouse_event = self.escape_mouse
                    key_event = lambda *args: None
                    display = self.d.display_escape
                case "instructions":
                    mouse_event = self.instructions_mouse
                    key_event = lambda *args: None
                    display = self.d.display_instructions
                case "scores":
                    self.d.seed = random.randint(0, 10000)
                    mouse_event = self.instructions_mouse
                    key_event = lambda *args: None
                    display = self.d.display_scores
                case "confirm_quit":
                    mouse_event = self.confirm_quit_mouse
                    key_event = lambda *args: None
                    display = self.d.display_confirm_quit
                case "end":
                    self.d.i = 0
                    self.d.text = ""
                    self.text_mode = True
                    mouse_event = self.end_mouse
                    key_event = self.end_keys
                    display = self.d.display_end

    def core_while(
                self,
                mousebuttonup: Callable[..., str],
                keydown: Callable[..., str],
                display:  Callable[..., str]
                ) -> str:
        """  """ #  TODO

        game = True
        text = ""

        fps_limit = self.fps_limit
        while game:
            start_frame = s2.SDL_GetTicks()

            event = s2.SDL_Event()
            while s2.SDL_PollEvent(event):
                match event.type:
                    case s2.SDL_QUIT:
                        return "exit"
                    case s2.SDL_WINDOWEVENT:
                        if event.window.event == s2.SDL_WINDOWEVENT_RESIZED:
                            w = event.window.data1
                            h = event.window.data2
                            self.midxy[0] = int(w / 2)
                            self.midxy[1] = int(h / 2)
                            self.set_cell_size(w, h)

                    case s2.SDL_MOUSEBUTTONUP:
                        res = mousebuttonup(event)
                        if res:
                            return res
                    case s2.SDL_KEYDOWN:
                        res = keydown(event)
                        if res:
                            return res
                    case s2.SDL_TEXTINPUT:
                        if self.text_mode:
                            self.d.text += event.text.text.decode()
                            if len(self.d.text) > 25:
                                self.d.text = ""
                                self.text_mode = False

            res = display()
            if res:
                return res
            limit_fps(start_frame, fps_limit)



