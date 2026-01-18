from multiprocessing.reduction import recvfds

from prompt_toolkit.document import Document
from prompt_toolkit.filters import app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import TextArea
from prompt_toolkit.application import Application, get_app
from client_funcs import *
import threading
import time
import dataclasses

@dataclasses.dataclass
class NVals:
    HOSTNAME: str
    PORT: int

DFLNVals = NVals("p9cx.org", 1111)

messages_to_be_sent = []
messages_to_be_sent_lock = threading.Lock()
received_message = []
received_message_lock = threading.Lock()

class Tui:
    def __init__(self):
        self.output_field = TextArea(style="class:output-field")
        self.input_field = TextArea(
            height=1,
            prompt=">>> ",
            style="class:input-field",
            multiline=False,
            wrap_lines=False,
        )

        self.container = HSplit(
            [
                self.output_field,
                Window(height=1, char="-", style="class:line"),
                self.input_field,
            ]
        )

        self.kb = KeyBindings()

        self.style = Style(
            [
                ("output-field", "bg:#000044 #ffffff"),
                ("input-field", "bg:#000000 #ffffff"),
                ("line", "#004400"),
            ]
        )

        self.application = Application(
            layout=Layout(self.container, focused_element=self.input_field),
            key_bindings=self.kb,
            style=self.style,
            mouse_support=True,
            full_screen=True,
        )
        self.app = get_app()


    def accept(self, buff):
        try:
            output = self.input_field.text
        except BaseException as e:
            output = f"\n\n{e}"
        with messages_to_be_sent_lock:
            messages_to_be_sent.append(output)


    def main(self):
        self.input_field.accept_handler = self.accept

        @self.kb.add("c-c")
        @self.kb.add("c-q")
        def _(event):
            event.app.exit()

        self.application.run()

    def network_main(self):
        while True:
            time.sleep(0.1)
            try:
                network = Network(DFLNVals.HOSTNAME, DFLNVals.PORT)
                network.tls_socket_creation()
                network.connect()

                threading.Thread(
                    target=self.recv_loop,
                    args=(network.socket,),
                    daemon=True).start()

                network.socket_sendall("client connected")

                while True:
                    time.sleep(0.1)
                    with messages_to_be_sent_lock:
                        try:
                            if len(messages_to_be_sent) != 0:
                                to_be_sent = messages_to_be_sent.pop()
                                to_be_sent = to_be_sent.replace('\r', '').replace('\n', '')
                                network.socket_sendall(to_be_sent)

                        except socket.timeout:
                            continue

                        except (socket.error, OSError):
                            self.output_field.buffer.text += "it failed :("
                            self.app.invalidate()
                            break

            except socket.timeout:
                self.output_field.buffer.text += "it failed 2 :("
                self.app.invalidate()
                continue
            except Exception as e:
                self.output_field.buffer.text += str(e)
                self.app.invalidate()
                break

    def recv_loop(self, sock):
        while True:
            try:
                data = sock.recv(4096)
                if not data:
                    break

                self.output_field.buffer.text += data.decode()
                self.output_field.buffer.cursor_position = len(self.output_field.text)
                self.app.invalidate()

            except socket.timeout:
                continue
            except OSError:
                break

if __name__ == "__main__":
    obj = Tui()
    network_thread = threading.Thread(target=obj.network_main, daemon=True)
    network_thread.start()
    obj.main()
