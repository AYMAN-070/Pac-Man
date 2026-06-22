
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

    def cheat_codes(self) -> str:
        match self.d.text:
            case "/cheat":
                self.text_mode = False
                self.engine.toggle_invincibility()
            case "/next":
                self.text_mode = False
                self.engine.cheat_next_level()
                return "reload"
        return ""

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
            case s2.SDLK_SLASH:
                self.text_mode = True
                self.d.text = ""
            case s2.SDLK_RETURN:
                res = self.cheat_codes()
                if res:
                    return res

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

        jump = 350
        w = int(self.midxy[1] / 2)
        h = int(self.midxy[1] / 4)
        pading = int(w / 2)
        pos_w = int(self.midxy[0] -  (w/ 2))

        x_lu = self.midxy[0] - w / 2  # left up
        x_rd = self.midxy[0] + w / 2  # right down

        y_lu = jump + pading
        y_rd = y_lu + h
        inside = {"lu": (x_lu, y_lu), "rd": (x_rd, y_rd)}
        data.update({"newgame": inside})

        y_lu = jump + pading * 2
        y_rd = y_lu + h
        inside = {"lu": (x_lu, y_lu), "rd": (x_rd, y_rd)}
        data.update({"scores": inside})

        y_lu = jump + pading * 3
        y_rd = y_lu + h
        inside = {"lu": (x_lu, y_lu), "rd": (x_rd, y_rd)}
        data.update({"instructions": inside})

        y_lu = jump + pading * 4
        y_rd = y_lu + h
        inside = {"lu": (x_lu, y_lu), "rd": (x_rd, y_rd)}
        data.update({"confirm_quit": inside})

        return data

    def check_button(self, x: int, y: int) -> str:
        button = self.get_menu_buttons()
        self.set_music_off(x, y)
        for option in button.keys():
            if button[option]['lu'][0] < x < button[option]['rd'][0]:
                if button[option]['lu'][1] < y < button[option]['rd'][1]:
                    return str(option)
        return ""
    
    def set_music_off(self, x: int, y: int) -> str:
        lux = 25
        luy = self.midxy[1] * 2 - 175
        size = 150
        if lux < x < lux + size:
            if luy < y < luy + (size):
                if self.s.music_off:
                    self.s.music_off_background_sound(False)
                else:
                    self.s.music_off_background_sound(True)


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
        self.set_music_off(event.button.x, event.button.y)
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
                if self.d.text and len(self.d.text) <= 10 and self.d.text.isalnum():
                    self.engine.highscore_manager.add_score(self.d.text, self.engine.score)
                    return "menu"
        return ""
