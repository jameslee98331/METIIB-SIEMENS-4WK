# Echo client program
import socket
import time


def send(offset: tuple):
    x_lin_off = str(offset[0])
    z_lin_off = str(offset[1])
    y_rot_off = str(offset[2])
    send_string = f'({x_lin_off}, {z_lin_off}, {y_rot_off})'.encode('utf-8')

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
            continue

        try:
            msg = c.recv(1024)
            time.sleep(1)
            if msg == b"asking_for_data":
                print(msg)
                time.sleep(0.5)
                c.send(send_string)
                print(f'Send {x_lin_off}, {z_lin_off}, {y_rot_off}')
        except:
            with socket.error as socketerror:
                print(socketerror)
                c.close()
                s.close()
                continue
