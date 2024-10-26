import socket
from time import sleep

from examples.client_server.message import MessageV1, MessageV2

if __name__ == "__main__":
    BUFF_SIZE = 128

    with socket.create_connection(("127.0.0.1", 8888)) as client_sock:
        print("Connected to server")
        i = 0
        try:
            while True:
                print(f"Iteration {i}".center(80, "="))
                msg_v1 = MessageV1(
                    parsed_fields_map=dict(ver=1, msg_id=100, data_len=5, data=b"hello")
                )
                print(f"Sending msg v1 to server {msg_v1}")
                client_sock.sendall(msg_v1.get_raw())

                data = client_sock.recv(64)
                if not data:
                    break
                print(f"Received raw data from server {data}")
                msg_v2 = MessageV2(data)
                print(msg_v2)
                print("=" * 80)
                i += 1

                sleep(3)
        except KeyboardInterrupt:
            print("Interrupted")
        finally:
            client_sock.close()
            print("Connection closed")
