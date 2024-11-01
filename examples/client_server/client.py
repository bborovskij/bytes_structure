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
    BUFF_SIZE = 128

    with socket.create_connection(("127.0.0.1", 8888)) as client_sock:
        print("Connected to server")
        i = 0
        try:
            while True:
                print(f"Iteration {i}".center(80, "="))
                msg_v1 = MessageV1(
                    fields_map=dict(ver=1, msg_id=100, data_len=5, data=b"hello")
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
