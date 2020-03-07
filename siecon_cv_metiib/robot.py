# Echo client program
import socket
import time


def send(x_offset_lin: float, z_offset_lin: float, rotation: float) -> None:
    send_string = f'({x_offset_lin}, {z_offset_lin}, {rotation})'.encode('utf-8')

    host = "192.168.0.10"  # The remote host
    port = 30000  # The same port as used by the server

    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))  # Bind to the port
            s.listen(5)  # Now wait for client connection.
            c, addr = s.accept()  # Establish connection with client.
        except OSError:
            print('retry connection')
            continue

        try:
            msg = c.recv(1024)
            time.sleep(1)
            if msg == b"asking_for_data":
                print(msg)
                time.sleep(0.5)
                c.send(send_string)
                print(f'Send {x_offset_lin}, {z_offset_lin}, {rotation}')
        except:
            with socket.error as socketerror:
                print(socketerror)
                print('retry send')
                c.close()
                s.close()
                continue
