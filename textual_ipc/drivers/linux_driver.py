from typing import TYPE_CHECKING

from textual.drivers.linux_driver import LinuxDriver

if TYPE_CHECKING:
    from rich.console import Console
    from textual._types import MessageTarget


class LinuxFDDriver(LinuxDriver):
    def __init__(self, in_fileno: int, console: "Console", target: "MessageTarget") -> None:
        super().__init__(console, target)
        self.fileno = in_fileno
