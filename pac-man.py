
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
from player import Direction
from init_input_engine import InitInputEngine



def limit_fps(start_frame: int, limit: int) -> None:
    ticks = s2.SDL_GetTicks()
   
    if start_frame + limit > ticks:
        # TOO EARLY
        s2.SDL_Delay(start_frame + limit - ticks)


class InputEngine(InitInputEngine):
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

        mouse_event = self.menu_mouse
        key_event = lambda *args: None
        display = self.d.display_menu
        while game:
            self.d.printed = False
            res = self.core_while(
                    mouse_event,
                    key_event,
                    display
                    )
            match res:
                case "exit":
                    return
                case "menu":
                    mouse_event = self.menu_mouse
                    key_event = lambda *args: None
                    display = self.d.display_menu
                case "newgame":
                    mouse_event = lambda *args: None
                    key_event = self.newgame_keys
                    display = self.d.display_and_compute_game
                    self.engine = GameEngine(self.config_path)
                    self.player = self.engine.player
                    self.d.engine = self.engine
                    self.d.init_engine()
                case "escape":
                    mouse_event = self.escape_mouse
                    key_event = lambda *args: None
                    display = self.d.display_escape
                case "instructions":
                    mouse_event = self.instructions_mouse
                    key_event = lambda *args: None
                    display = self.d.display_instructions
                case "scores":
                    mouse_event = self.instructions_mouse
                    key_event = lambda *args: None
                    display = self.d.display_scores


    def core_while(
                self,
                mousebuttonup: Callable[..., str],
                keydown: Callable[..., str],
                display:  Callable[..., str]
                ) -> str:
        """  """ #  TODO

        game = True

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
                            if w < h:
                                self.d.cell = int((w - 250) / len(self.d.maze))
                            else:
                                self.d.cell = int((h - 250) / len(self.d.maze))
                            self.d.printed = False

                    case s2.SDL_MOUSEBUTTONUP:
                        res = mousebuttonup(event)
                        if res:
                            return res
                    case s2.SDL_KEYDOWN:
                        res = keydown(event)
                        if res:
                            return res
            display()
            limit_fps(start_frame, fps_limit)

    def newgame_keys(self, event) -> str:
        """  """ #  TODO

        match event.key.keysym.sym:
            case s2.SDLK_UP | s2.SDLK_w:
                self.player.next_direction = Direction.UP
            case s2.SDLK_RIGHT | s2.SDLK_d:
                self.player.next_direction = Direction.RIGHT
            case s2.SDLK_DOWN | s2.SDLK_s:
                self.player.next_direction = Direction.DOWN
            case s2.SDLK_LEFT | s2.SDLK_a:
                self.player.next_direction = Direction.LEFT
            case s2.SDLK_ESCAPE:
                return "escape"
        return ""


    def menu_mouse(self, event) -> str:
        """  """ #  TODO

        if event.button.button == s2.SDL_BUTTON_LEFT:
            act = self.check_button(
                                    event.button.x,
                                    event.button.y)
            if act:
                return act

    def get_menu_buttons(self) -> dict[str, Any]:
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


    def check_button(self, x: int, y: int) -> str:
        button = self.get_menu_buttons()
        for option in button.keys():
            if button[option]['lu'][0] < x < button[option]['rd'][0]:
                if button[option]['lu'][1] < y < button[option]['rd'][1]:
                    return str(option)
        return ""
    
    def return_menu(self, event: Any) -> str:

        size = 190
        ypad = 90
        lux = int(self.midxy[0] / 10)
        luy = int(self.midxy[1] / 10)
        if lux < event.button.x < lux + size:
            if luy < event.button.y < luy + (size - ypad):
                return "menu"
        return ""
    
    def escape_mouse(self, event: Any) -> str:
        
        if event.button.button == s2.SDL_BUTTON_LEFT:
            size = 600
            ypad = 300
            lux = int(self.midxy[0] - size / 2)
            luy = int(self.midxy[1] - (size - ypad + 100) / 2)
            if lux < event.button.x < lux + size:
                if luy < event.button.y < luy + (size - ypad):
                    return "newgame"

            ret = self.return_menu(event)
            if ret:
                return ret
            return ""

    def instructions_mouse(self, event: Any) -> str:

        if event.button.button == s2.SDL_BUTTON_LEFT:
            ret = self.return_menu(event)
            if ret:
                return ret
        return ""

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error. Usage : python3 pac-man.py config.json")
        sys.exit(1)
    app = InputEngine(sys.argv[1])
