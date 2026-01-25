from textual import events
from textual.app import App, ComposeResult
from textual.widgets import Footer, Label

class Menu(App[None]):
    signal = ""
    BINDINGS = [
        ("[Tab]", "change", "Changes menu option",),
        ("ctrl+q", "quit", "Quit"),
        ("enter", "enter", "Selects menu option")
    ]

    currently_selected = 0

    options_dict = {
        "1": "Enter Chatroom",
        "2": "Change Name",
        "3": "About",
    }

    CSS = """
        Screen {
            align: center middle;
        }"""
    def compose(self) -> ComposeResult:
        yield Label(self.options_dict["1"], id="i1")
        yield Label(self.options_dict["2"], id="i2")
        yield Label(self.options_dict["3"], id="i3")
        yield Footer()

    def on_key(self, event: events.Key) -> None:
        if event.key == "tab":
            self.currently_selected += 1
            if self.currently_selected > 3:
                self.currently_selected = 1

            for i in range(1, 4):
                label = self.query_one(f"#i{i}", Label)
                if i == self.currently_selected:
                    label.update(f"> {self.options_dict[str(i)]}")
                else:
                    label.update(self.options_dict[str(i)])

        elif event.key == "enter":
            self.signal = self.currently_selected


