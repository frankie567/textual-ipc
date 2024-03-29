import functools
from multiprocessing.connection import Client
import sys
from threading import Thread
from typing import TYPE_CHECKING, Any, Optional, Type, cast

from textual._context import active_app
from textual.app import App, WINDOWS
from textual.events import Event
from textual.driver import Driver

if TYPE_CHECKING:
    from textual._types import MessageTarget


class ConnectSocket(Event):
    pass


class SocketMessage(Event):
    def __init__(self, sender: "MessageTarget", message: Any) -> None:
        super().__init__(sender)
        self.message = message
        self.name = "socket_message"


class UI(App):
    def __init__(
        self,
        socket_addr: str,
        driver_class: Optional[Type[Driver]] = None,
        in_fileno: Optional[None] = None,
        out_fileno: Optional[None] = None,
    ) -> None:
        self.in_fileno = in_fileno if in_fileno is not None else sys.stdin.fileno()
        self.socket_addr = socket_addr
        self.out_fileno = out_fileno if out_fileno is not None else sys.stdout.fileno()
        super().__init__(driver_class)

    @classmethod
    def create_and_run(
        cls,
        socket_addr: str,
        driver_class: Optional[Type[Driver]] = None,
        in_fileno: Optional[None] = None,
        out_fileno: Optional[None] = None,
    ):
        app = cls(socket_addr, driver_class, in_fileno, out_fileno)
        return app.run()

    def get_driver_class(self) -> Type[Driver]:
        driver_class: functools.partial[Driver]
        if WINDOWS:
            from textual_ipc.drivers.windows_driver import WindowsFDDriver

            driver_class = functools.partial(
                WindowsFDDriver, self.in_fileno, self.out_fileno
            )
        else:
            from textual_ipc.drivers.linux_driver import LinuxFDDriver

            driver_class = functools.partial(LinuxFDDriver, self.in_fileno)
        return cast(Type[Driver], driver_class)

    async def _process_messages(self) -> None:
        active_app.set(self)
        connect_socket_event = ConnectSocket(sender=self)
        await self.post_message(connect_socket_event)
        await super()._process_messages()

    async def shutdown(self):
        await super().shutdown()
        self.send_socket_message("QUIT")
        self.conn.close()

    async def on_connect_socket(self, event: ConnectSocket) -> None:
        self.conn = Client(self.socket_addr)
        self.listen_socket_thread = Thread(target=self.listen_socket)
        self.listen_socket_thread.start()

    def listen_socket(self) -> None:
        try:
            while message := self.conn.recv():
                socket_message_event = SocketMessage(self, message)
                self.post_message_no_wait(socket_message_event)
        except (EOFError, OSError):
            pass

    async def send_socket_message(self, message: str) -> None:
        self.conn.send(message)
