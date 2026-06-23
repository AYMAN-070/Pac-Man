
import sdl2.ext.image as s2_img
import sdl2 as s2
from typing import Any
from pathlib import Path


class TextureError(Exception):
    """  """  # TODO
    pass


TEXTURES_PATH = [
        "assets/",
        "menu_title.png",
        "menu_newgame.png",
        "menu_scores.png",
        "menu_instructions.png",
        "menu_exit.png",

        "wall.png",
        "pacgum.png",
        "megapacgum.png",

        "background.png",
        "background_item.png",

        "level.png",
        "score.png",
        "lives.png",
        "time.png",
        "resume.png",
        "return_menu.png",
        "instructions.png",
        "scores.png",
        "crown.png",
        "areyousure.png",
        "music_on.png",
        "music_off.png",

        "sprit_lives.png",
        "sprit_ghost1.png",
        "sprit_ghost2.png",
        "sprit_ghost3.png",
        "sprit_ghost4.png",
        "sprit_pacman.png",
        "sprit_pacman_cheat.png",
        "sprit_pacman_death.png",
]


class Textures:
    """  """  # TODO

    def __init__(self, renderer: Any) -> None:
        """  """  # TODO
        self.all = dict()
        self.renderer = renderer

    def load_textures(self) -> None:
        """  """  # TODO
        try:
            for path in TEXTURES_PATH[1:]:
                self.create_texture(TEXTURES_PATH[0] + path)
        except Exception:
            self.destroy_all()
            raise
        return self.all

    def destroy_all(self) -> None:
        """  """  # TODO
        for key, elem in self.all.items():
            s2.SDL_DestroyTexture(elem)

    def create_texture(self, path: str):
        """  """  # TODO
        image = s2_img.load_img(path)
        if not image:
            raise TextureError(f"can't load : {path}")
        texture = s2.SDL_CreateTextureFromSurface(self.renderer, image)
        if not texture:
            s2.SDL_FreeSurface(image)
            raise TextureError(f"can't create texture from : {path}")

        s2.SDL_FreeSurface(image)

        name = Path(path).name.removesuffix(".png")
        self.all.update({name: texture})
