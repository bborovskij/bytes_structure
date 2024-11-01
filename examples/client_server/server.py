# MIT License
#
# Copyright (c) 2024 Bohdan Borovskyi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import socket
from time import sleep

from message import MessageV1, MessageV2

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
