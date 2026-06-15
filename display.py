
import sdl2.ext.image as s2_img
import sdl2 as s2
import ctypes
from typing import Any


class DiplayError(Exception):
    """  """ # TODO
    pass


class Display:
    """  """ # TODO

    def __init__(self, renderer: Any, textures: dict[str, Any]) -> None:
        """  """ # TODO
        self.renderer = renderer
        self.t = textures

    def display_menu(self, wmid: int) -> None:
        """  """ #  TODO
        s2.SDL_RenderClear(self.renderer)

        jump = 200
        pading = 200
        w = 400
        h = 200
        pos_w = int(wmid -  (w/ 2))

        dst = s2.SDL_Rect(int(wmid -  (800 / 2)), -50, 800, 500)
        s2.SDL_RenderCopy(self.renderer, self.t['menu_title'], None, dst)

        dst = s2.SDL_Rect(pos_w, jump + pading, w, h)
        s2.SDL_RenderCopy(self.renderer, self.t['menu_newgame'], None, dst)

        dst = s2.SDL_Rect(pos_w, jump + pading * 2, w, h)
        s2.SDL_RenderCopy(self.renderer, self.t['menu_scores'], None, dst)

        dst = s2.SDL_Rect(pos_w, jump + pading * 3, w, h)
        s2.SDL_RenderCopy(self.renderer, self.t['menu_instructions'], None, dst)

        dst = s2.SDL_Rect(int(wmid -  ((w - 100)/ 2)), jump + pading * 4, w - 100, h - 80)
        s2.SDL_RenderCopy(self.renderer, self.t['menu_exit'], None, dst)

        s2.SDL_RenderPresent(self.renderer)

    def get_buttons(self, wmid) -> dict[str, Any]:
        """  """ #  TODO
        data = dict()

        jump = 210
        pading = 200
        w = 400
        h = 200
        pos_w = int(wmid -  (w/ 2))

        w_lu = wmid - 155  # left up
        w_rd = wmid + 155  # right down

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

    def display_game(self) -> None:
        """  """ #  TODO
