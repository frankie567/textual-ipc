from datetime import datetime

from textual.widgets import Header, ScrollView, Button, ButtonPressed

from textual_ipc.ui import SocketMessage, UI
from textual_ipc.worker import Worker
from textual_ipc.app import run


class ExampleUI(UI):
    async def on_mount(self) -> None:
        await self.view.dock(Header(), edge="top")
        await self.view.dock(
            Button("Update time", name="update_time"), edge="bottom", size=10
        )
        self.body = ScrollView(
            'Nothing yet. Click on the "Update time" button to get current time.',
            gutter=1,
        )
        await self.view.dock(self.body, edge="right")

    async def handle_button_pressed(self, event: ButtonPressed):
        assert isinstance(event.sender, Button)
        if event.sender.name == "update_time":
            await self.send_socket_message("UPDATE_TIME")

    async def on_socket_message(self, event: SocketMessage) -> None:
        await self.body.update(event.message)


class ExampleWorker(Worker):
    def on_message(self, message: str) -> None:
        if message == "QUIT":
            self.conn.close()
        elif message == "UPDATE_TIME":
            self.conn.send(datetime.now().strftime("%X"))


if __name__ == "__main__":
    run(ExampleUI, ExampleWorker)
