import socket
import time
import threading

#-------------SERVER----------#

port = 1111

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

my_socket.bind(("0.0.0.0", port))

accept_state = False

print("Welcome!")

my_socket.listen(5)

def send_receive_data(thread_client, thread_address):
    while True:
        try:
            thread_client.settimeout(0.1)
            data = thread_client.recv(1024)
            print("data received")
            if not data:         # if no data is received
                print(f"Client {thread_address} disconnected")
                break
            thread_client.send(b"hello from server")

            print(f"Received from {thread_address}: {data.decode()}")

        except socket.timeout:
            pass
        except Exception as err:
            print(f"{err}")


while True:
    time.sleep(0.1)
    try:
        client, address = my_socket.accept()
        client_thread = threading.Thread(
            target=send_receive_data,
            args=(client, address),
            daemon=True    )
        print("thread started")
        client_thread.start()

    except Exception:
        pass
