# Echo client program
import socket
import time


def send(x_offset: float, z_offset: float, rotation: float) -> None:
    send_string = f'({x_offset}, {z_offset}, {rotation})'.encode('utf-8')

    # The remote host
    host = "192.168.0.10"
    # The same port as used by the server
    port = 30000

    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Bind to the port
            s.bind((host, port))

            # Now wait for client connection.
            s.listen(5)

            # Establish connection with client.
            c, addr = s.accept()

        except OSError:
            print('Retry Connection')
            continue

        try:
            msg = c.recv(1024)
            time.sleep(1)
            if msg == b"asking_for_data":
                print(msg)
                time.sleep(0.5)
                c.send(send_string)
                print(f'Send {x_offset}, {z_offset}, {rotation}')
        except:
            with socket.error as socket_error:
                print(socket_error)
                print('Retry Send')
                c.close()
                s.close()
                continue
