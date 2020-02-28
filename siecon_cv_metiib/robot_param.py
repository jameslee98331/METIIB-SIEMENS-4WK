# Echo client program
import socket
import time


def send():
    HOST = "192.168.0.10"  # The remote host
    PORT = 30000  # The same port as used by the server
    print("Starting Program")
    count = 0

    while (count < 1000):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))  # Bind to the port
        s.listen(5)  # Now wait for client connection.
        c, addr = s.accept()  # Establish connection with client.
        try:
            msg = c.recv(1024)
            print(msg)
            time.sleep(1)
            if msg == b"asking_for_data":
                count = count + 1
                print("The count is:", count)
                time.sleep(0.5)
                print("")
                time.sleep(0.5)
                c.send(b"(0.10,0.10,0.7)")
                print("Send 0.05,0.00,0.00")
        except socket.error as socketerror:
            print(count)
            c.close()
            s.close()

    print("Program finish")
