
import socket
import errno

#-----------------CLIENT-------------------------#
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

port = 1111


def main():
    connected = False

    while True:

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
            my_socket.sendall(b"test from client")
            print(my_socket.recv(1024))


main()
