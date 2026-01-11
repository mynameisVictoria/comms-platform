from multiprocessing.reduction import recvfds

from prompt_toolkit.document import Document
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
                ("output-field", "bg:#000044 #0000ff"),
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

    def accept(self, buff):
        try:
            output = self.input_field.text
        except BaseException as e:
            output = f"\n\n{e}"

        new_text = self.output_field.text + output + "\n"

        with messages_to_be_sent_lock:
            messages_to_be_sent.append(new_text)


    def main(self):
        self.input_field.accept_handler = self.accept

        @self.kb.add("c-c")
        @self.kb.add("c-q")
        def _(event):
            event.app.exit()

        self.application.run()

    def network_main(self):
        app = get_app()
        while True:
            time.sleep(0.1)
            try:
                network = Network(DFLNVals.HOSTNAME, DFLNVals.PORT)
                network.tls_socket_creation()
                network.connect()

                recv_thread = threading.Thread(target=self.constant_receive, args=(network,))
                recv_thread.start()

                while True:
                    time.sleep(0.1)
                    with messages_to_be_sent_lock:
                        try:
                            if len(messages_to_be_sent) != 0:
                                to_be_sent = messages_to_be_sent.pop()
                                to_be_sent = to_be_sent.replace('\r', '').replace('\n', '')
                                network.socket_sendall(to_be_sent)

                            else:
                                continue

                        except socket.timeout:
                            continue

                        except (socket.error, OSError):
                            self.output_field.buffer.text += "it failed :("
                            app.invalidate()
                            #recv_thread.join()
                            break

            except socket.timeout:
                self.output_field.buffer.text += "it failed 2 :("
                app.invalidate()
                continue
            except Exception as e:
                self.output_field.buffer.text += str(e)
                app.invalidate()
                break

    def constant_receive(self, network_object):
        pass



if __name__ == "__main__":
    obj = Tui()
    network_thread = threading.Thread(target=obj.network_main, daemon=True)
    network_thread.start()
    obj.main()