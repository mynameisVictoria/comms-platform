from textual import events
from textual.widgets import Footer, Label
from chat import *

class Main(App):

    CSS = """
        Screen {
            align: center middle;
        }"""

    def on_mount(self) -> None:
        self.install_screen(Menu(), "menu")
        self.push_screen("menu")

class Menu(Screen):

    currently_selected = 0

    BINDINGS = [
        ("[Tab]", "change", "Changes menu option",),
        ("ctrl+q", "quit", "Quit"),
        ("enter", "enter", "Selects menu option")
    ]

    options_dict = {
        "1": "Enter Chatroom",
        "2": "Change Penis",
        "3": "Quit the penis",
    }

    def compose(self) -> ComposeResult:
        yield Label(self.options_dict["1"], id="l1")
        yield Label(self.options_dict["2"], id="l2")
        yield Label(self.options_dict["3"], id="l3")
        yield Footer()

    def on_key(self, event: events.Key) -> None:
        if event.key == "tab":
            self.currently_selected += 1
            if self.currently_selected > 3:
                self.currently_selected = 0

            else:
                for i in range(1,4):

                    label = self.query_one(f"#l{i}", Label)

                    if i == self.currently_selected:
                        label.update(f"> {self.options_dict[str(i)]}")
                    else:
                        label.update(self.options_dict[str(i)])

        elif event.key == "enter":
            if self.currently_selected == 1:
                self.app.pop_screen()
                self.app.install_screen(InputApp, "chat")
                self.app.push_screen("chat")


if __name__ == "__main__":
    app = Main()
    app.run()
