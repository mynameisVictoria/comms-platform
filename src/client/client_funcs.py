import json
from time import sleep
import sys
import socket
from datetime import datetime, timezone

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

class GeneralIO:
    def __init__(self):
        pass
    @staticmethod
    def get_input():
        while True:
            sleep(0.1)
            send_info_input = input("")
            if not send_info_input.strip() == "":
                return send_info_input
            elif send_info_input == "exit":
                sys.exit()

    @staticmethod
    def format_message(username, message):
        timestamp = datetime.now(timezone.utc).strftime('%H:%M:%S')
        return f"[{timestamp} ] | {username}: {message}"

