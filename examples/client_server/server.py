import socket
from time import sleep

from examples.client_server.message import MessageV1, MessageV2

if __name__ == "__main__":
    with socket.create_server(
        ("0.0.0.0", 8888),
        family=socket.AF_INET,
    ) as server_fd:
        print("Listening for client")
        client_fd, addr = server_fd.accept()
        print(f"Accepted client from {addr}")
        i = 0
        try:
            while True:
                print(f"Iteration {i}".center(80, "="))
                msg_v1 = client_fd.recv(64)
                if not msg_v1:
                    break
                print(f"Received message from client: {msg_v1}")
                from_client_v1 = MessageV1(msg_v1)
                print(from_client_v1)

                print("Sending msg v2 to client")
                to_client_v2 = MessageV2(msg_v1 + b"\x05world")
                print(to_client_v2)
                client_fd.sendall(to_client_v2.get_raw())
                print("=" * 80)
                i += 1

                sleep(3)
        except KeyboardInterrupt:
            print("Interrupted")
        finally:
            client_fd.close()
            print("Connection closed")
