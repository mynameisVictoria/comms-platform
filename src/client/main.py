import socket
import errno
import time

#-----------------CLIENT-------------------------#
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 1111


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
            try:

                my_socket.sendall(b"test from CLIENT ONE 11111")
                data = my_socket.recv(1024)
                print(data.decode())
            except Exception as err:
                print(err)



main()
