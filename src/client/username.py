from textual import events
from textual.app import App, ComposeResult
from textual.widgets import Input, Label


class Username(App):

    def compose(self) -> ComposeResult:
        yield Label("Return to Main Menu", id="main_menu")
        yield Label("Your username will appear here", id="username")
        yield Input(placeholder="Max 24 characters long", id="input")

test = Username()
test.run()

