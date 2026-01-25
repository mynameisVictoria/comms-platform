from textual import events
from textual.app import App, ComposeResult
from textual.widgets import Input, Label


class Username(App):

    selected = False
    signal = False

    CSS = """
        Screen {
            align: center middle;
            }
        Input {
            margin: 1 0;
            padding: 0 1;
            border: none;
            background: $surface;
            width: 40;
        }
        Label {
        text-align: justify;
        }
        
        """
    def compose(self) -> ComposeResult:
        yield Label("Return to Main Menu", id="main_menu")
        yield Label("Your username will appear here", id="username")
        yield Input(placeholder="Max 24 characters long", id="input")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        label = self.query_one(f"#username", Label)
        username = event.value
        if len(username) > 24:
            label.update("Username is too long.")
        else:
            label.update("Successfully added.")

    def on_key(self, event: events.Key) -> None:
        if event.key == "tab":
            label = self.query_one(f"#main_menu", Label)
            if not self.selected:
                self.selected = True
                label.update("Return to Main Menu")
            elif self.selected:
                self.selected = False
                label.update("> Return to Main Menu")
        elif event.key == "enter":
            if self.selected:
                self.signal = True
            elif not self.selected:
                self.signal = False



#if __name__ == "__main__":
#    app = Username()
#    app.run()
