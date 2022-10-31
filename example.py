from datetime import datetime

from textual.widgets import Header, Button, Footer, Static
from textual.containers import Container

from textual.app import ComposeResult

from textual_ipc.ui import SocketMessage, UI
from textual_ipc.worker import Worker
from textual_ipc.app import run


class ExampleUI(UI):

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield Container(
            Static("Nothing yet. Click on the \"Update time\" button to get current time."),
            Button("Update time", id="update_time"),
        )

    async def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "update_time":
            await self.send_socket_message("UPDATE_TIME")

    async def on_socket_message(self, event: SocketMessage) -> None:
        static = self.query_one(Static)
        static.update(event.message)


class ExampleWorker(Worker):
    def on_message(self, message: str) -> None:
        if message == "QUIT":
            self.conn.close()
        elif message == "UPDATE_TIME":
            self.conn.send(datetime.now().strftime("%X"))


if __name__ == "__main__":
    run(ExampleUI, ExampleWorker)
