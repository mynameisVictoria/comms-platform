import socket
import time
import threading

#-------------SERVER----------#

port = 1111

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.settimeout(0.5)

my_socket.bind(("localhost", port))

accept_state = False

client_address_dict = {}

print("Welcome!")

my_socket.listen(5)

def send_receive_data(ip_address):
    while True:

        try:
            dict_client = client_address_dict[ip_address]

            data = dict_client.recv(1024)
            print("data received")
            if not data:         # if no data is received
                print(f"Client {ip_address} disconnected")
                client_address_dict.pop(ip_address)
                client_thread.join()
                break
            dict_client.send(b"hello from server")

            print(f"Received from {ip_address}: {data.decode()}")

        except socket.timeout:
            print(f"Socket timed out.")
        except Exception:
            pass

while True:
    time.sleep(0.5)
    try:
        client, address = my_socket.accept()
        client_address_dict.update({address: client})

        client_thread = threading.Thread(target=send_receive_data(address))
        client_thread.start()

    except Exception as e:
        print(f"Error: {e}")
