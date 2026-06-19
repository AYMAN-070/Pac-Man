
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
    print(f"Error : missing library ({e.name}).", file=sys.stderr)
    print("Solution : lunch 'make run'.", file=sys.stderr)
    sys.exit(1)
from engine import GameEngine
from textures import Textures
from display import Display
from player import Direction
from init_input_engine import InitInputEngine
from input_sdl_engine import SDLCoreEngine


class InputEngine(SDLCoreEngine):

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

        jump = 310
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
        data.update({"confirm_quit": inside})

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
                return "confirm_quit"
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

    def confirm_quit_mouse(self, event: Any) -> str:

        if event.button.button == s2.SDL_BUTTON_LEFT:

            sizex = 800
            sizey = 400
            gapx = 30
            gapy = 60
            lux = self.midxy[0] - 400
            luy = self.midxy[1] - 170

            if lux + gapx < event.button.x < lux + sizex - gapx:
                if luy + gapy < event.button.y < luy + sizey - gapy:
                    if event.button.x < self.midxy[0] - 110:
                        return self.previous
                    if event.button.x > self.midxy[0] + 110:
                        if self.previous == "menu":
                            return "exit"
                        else:
                            return "menu"
        return ""

    def end_mouse(self, event: Any) -> str:
        return ""

    def end_keys(self, event: Any) -> str:

        match event.key.keysym.sym:
            case s2.SDLK_BACKSPACE:
                self.d.text = self.d.text[:-1]
            case s2.SDLK_RETURN:
                if len(self.d.text) <= 10:
                    self.engine.highscore_manager.scores.append({"name": self.d.text, "score": self.engine.score}) # TODO DATA NOTE SAVED ONLY FOR TEST
                    # TODO write this name and score somewhere
                    return "menu"
        return ""
