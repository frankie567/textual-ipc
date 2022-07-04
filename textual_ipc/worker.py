from datetime import datetime
from multiprocessing.connection import Listener
import time


class Worker:
    def __init__(self, socket_addr: str) -> None:
        self.socket_addr = socket_addr

    @classmethod
    def run(cls, socket_addr: str) -> None:
        worker = cls(socket_addr)
        worker.listen_socket()

    def listen_socket(self) -> None:
        with Listener(self.socket_addr) as listener:
            with listener.accept() as conn:
                self.conn = conn
                try:
                    while message := self.conn.recv():
                        self.on_message(message)
                except EOFError:
                    pass

    def on_message(self, message) -> None:
        pass
