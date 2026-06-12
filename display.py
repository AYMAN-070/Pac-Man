
import sdl2.ext.image as s2_img
import sdl2 as s2
import ctypes

class DiplayError(Exception):
    """  """ # TODO
    pass

class Display:
    """  """ # TODO

    def __init__(self) -> None:
        """  """ # TODO
        s2.SDL_Init(s2.SDL_INIT_VIDEO)
        self.window = s2.SDL_CreateWindow(b"HELLO GUYS",
                                     s2.SDL_WINDOWPOS_CENTERED,
                                     s2.SDL_WINDOWPOS_CENTERED,
                                     592, 460, s2.SDL_WINDOW_SHOWN)
        try:
            self.process()
        except Exception:
            raise
        finally:
            s2.SDL_DestroyWindow(self.window)
            s2.SDL_Quit()

    def process(self) -> None:
        """  """ # TODO

        windowsurface = s2.SDL_GetWindowSurface(self.window)
        image = s2_img.load_img(b"Untitled.png")
        if not image:
            raise DiplayError("wrong image")
        s2.SDL_BlitSurface(image, None, windowsurface, None)

        s2.SDL_UpdateWindowSurface(self.window)
        s2.SDL_FreeSurface(image)

        runing = True
        event = s2.SDL_Event()
        while  runing:
            while s2.SDL_PollEvent(ctypes.byref(event)) != 0:
                if event.type == s2.SDL_QUIT:
                    runing = False
                    break




def test() -> None:
    disp = Display()
    print("created")

test()
