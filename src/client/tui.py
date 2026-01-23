import dataclasses
import threading
import time
from textual.app import App, ComposeResult
from textual.widgets import Input, Log
from client_funcs import *


@dataclasses.dataclass
class NVals:
    HOSTNAME: str
    PORT: int

DFLNVals = NVals("p9cx.org", 1111)

typed_message = []
recevied_message = []
recevied_message_lock = threading.Lock()
typed_message_lock = threading.Lock()

class InputApp(App):

    CSS_PATH = "client_tcss.tcss"

    def compose(self) -> ComposeResult:
        yield Log(id="history")
        yield Input(placeholder="lorem ipsum i forgot the rest", id="user_name")

    def on_input_submitted(self, event: Input.Submitted) -> None:

        with typed_message_lock:
            typed_message.append(event.value)
        event.input.value = ""

    def network_main(self):
        while True:
            time.sleep(0.1)
            try:

                network = Network(DFLNVals.HOSTNAME, DFLNVals.PORT)
                network.tls_socket_creation()
                network.connect()
                network.socket_sendall("username")

                threading.Thread(
                    target=self.recv_loop,
                    args=(network.socket,),
                    daemon=True).start()

                while True:
                    time.sleep(0.1)
                    with typed_message_lock:
                        try:
                            if len(typed_message) != 0:
                                to_be_sent = typed_message.pop()
                                network.socket_sendall(to_be_sent)

                        except socket.timeout:
                            continue

                        except (socket.error, OSError):
                            break

            except socket.timeout:
                continue

            except Exception:
                break

    def recv_loop(self, sock):
        while True:
            try:
                data = sock.recv(4096)
                if not data:
                    break

                text = data.decode(errors="ignore")
                self.call_from_thread(
                    self.query_one("#history").write, text
                )

            except socket.timeout:
                continue
            except OSError:
                break

    def on_mount(self):
        threading.Thread(target=self.network_main, daemon=True).start()


if __name__ == "__main__":
    app = InputApp()
    app.run()
