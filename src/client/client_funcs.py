#  Copyright (C) <2026>  <mynameisVictoria> and <Victoria2048>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
import queue
import socket
from datetime import datetime, timezone
import ssl
from time import sleep

class JsonStoring:
    def __init__(self, file_name):
        self.file_name = file_name

    def get_name(self):
        with open(self.file_name, "r", encoding="utf-8") as file:
            contents = file.read()
            dict_data = json.loads(contents)
            name = dict_data["name"]
            return name
    def write_name(self,name):
        with open(self.file_name,"r+", encoding="utf-8") as file:
            contents = file.read()
            file.seek(0)
            file.truncate()
            dict_data = json.loads(contents)
            dict_data["name"] = name
            file.write(json.dumps(dict_data))

    def check_name(self):
        with open(self.file_name, "r", encoding="utf-8") as file:
            contents = file.read()
            dict_data = json.loads(contents)
            if dict_data["name"] is None:
                return False
            else:
                return True

json_storing = JsonStoring("user_data.json")

class GeneralIO:
    @staticmethod
    def do_command(command):
        if command == "/name":
            new_name = input("Input new name: \n")
            json_storing.write_name(new_name)
        elif command == "/help":
            print("do /name to change name\n")

class NetworkIO:
    def __init__(self, sock):
        self.sock = sock
        self.PORT = 1111
        self.HOST = "p9cx.org"

    def try_connect(self):
        try:
            self.sock.connect((self.HOST, self.PORT))
            return True
        except socket.error:
            return False

    def socket_receive(self):
            try:
                return self.sock.recv(1024).decode("utf-8")
            except socket.timeout:
                return False
            except Exception:
                return False

    def socket_send(self, data):
        try:
            self.sock.sendall(data.encode("utf-8"))
        except Exception:
            return False

