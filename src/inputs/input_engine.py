
from inputs.input_process import InputProcesses
from inputs.input_sdl_engine import SDLCoreEngine


class InputEngine(InputProcesses, SDLCoreEngine):

    def process_game(self) -> None:
        """  """  # TODO
        try:
            self.process_core_while()
        except Exception:
            raise
        finally:
            self.free_all()
