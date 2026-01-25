from tui import *
from menu import *
from username import *
import time


class Main:
    def __init__(self):
        self.MenuObject = Menu()
        self.menu_option_dict = {
            "1": "CHAT",
            "2": "NAME"
        }

    def main(self):
        self.MenuObject.run()
        menu_thread = threading.Thread(target=self.menu_signal_check())
        menu_thread.start()

    def menu_signal_check(self):
        while True:
            time.sleep(0.1)
            for i in range(1, 4):
                if i == self.MenuObject.signal:


if __name__ == "__main__":
    obj = Main()
    obj.main()