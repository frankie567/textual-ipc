from multiprocessing import Process
import sys
from typing import Optional, Type
import uuid

from textual_ipc.ui import UI
from textual_ipc.worker import Worker


def run(
    ui_class: Type[UI], worker_class: Type[Worker], socket_addr: Optional[str] = None
) -> None:
    socket_addr = socket_addr or str(uuid.uuid4())

    p_worker = Process(target=worker_class.run, args=(socket_addr,))
    p_ui = Process(
        target=ui_class.run,
        kwargs={
            "log": "textual.log",
            "socket_addr": socket_addr,
            "in_fileno": sys.stdin.fileno(),
            "out_fileno": sys.stdout.fileno(),
        },
    )

    p_worker.start()
    p_ui.start()
