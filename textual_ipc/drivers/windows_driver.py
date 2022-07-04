from typing import TYPE_CHECKING

from textual.drivers.windows_driver import WindowsDriver

if TYPE_CHECKING:
    from rich.console import Console
    from textual._types import MessageTarget


class WindowsFDDriver(WindowsDriver):
    def __init__(
        self, in_fileno: int, out_fileno: int, console: "Console", target: "MessageTarget"
    ) -> None:
        super().__init__(console, target)
        self.in_fileno = in_fileno
        self.out_fileno = out_fileno
