import keyboard
import json
import os
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 50505

key_inputs = [
    "w",
    "a",
    "s",
    "d",
]


class SocketConn:
    def __init__(self, sock) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def put_packet(self, packet):
        msg_bytes = bytes(json.dumps(packet), "utf-8")
        self.sock.sendto(msg_bytes, (UDP_IP, UDP_PORT))

    def on_input(self, key_input):
        key_input = ["KEY_INPUT", key_input]
        self.put_packet(key_input)


def main():
    conn = SocketConn()
    pid = os.getppid()
    conn.put_packet(["PIDs", pid])

    for key in key_inputs:
        keyboard.add_hotkey(key, lambda: conn.on_input(key))

    keyboard.wait()


if __name__ == "__main__":
    main()
