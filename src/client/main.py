import socket
import errno
import time
import threading
from queue import Queue
import sys

#-----------------CLIENT-------------------------#
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.settimeout(0.5)

port = 1111

send_info_queue = Queue(maxsize=10)

def handle_input():
    while True:
        send_info_input = input("send info: \n")
        if send_info_input == "exit":
            sys.exit()
        send_info_queue.put(send_info_input)

def main():
    connected = False

    while True:
        time.sleep(0.5)
        if not connected:
            try:
                my_socket.connect(("localhost", port))
                print("socket connected")
                connected = True
            except OSError as e:
                if e.errno in (errno.EISCONN, 56):
                    print("ERROR")
                    connected = True
                else:
                    connected = False

        elif connected:
            if send_info_queue.empty():
                continue
            elif not send_info_queue.empty():
                try:
                    my_socket.sendall(send_info_queue.get().encode("utf-8"))
                    print("sent")
                except Exception as err:
                    print(err)
            try:
                print(my_socket.recv(1024))
            except socket.timeout:
                pass

input_thread = threading.Thread(target=handle_input)
input_thread.start()

main()
input_thread.join()
