
import sdl2.ext.image as s2_img
import sdl2 as s2
import ctypes
from typing import Any
from pathlib import Path

class TextureError(Exception):
    """  """  # TODO
    pass

TEXTURES_PATH = [
        "images/menu_title.png",
        "images/menu_newgame.png",
        "images/menu_scores.png",
        "images/menu_instructions.png",
        "images/menu_exit.png",
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
            for path in TEXTURES_PATH:
                self.create_texture(path)
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
        self.all.update({name : texture})




