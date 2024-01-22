import sys, socket


class client:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port

    def start(self):
        try:
            # create a socket object
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # connection to hostname on the port.
            client_socket.connect((self.ip_address, self.port))

            # Receive no more than 1024 bytes
            msg = client_socket.recv(1024)

            print(msg.decode("utf-8"))

            while True:
                command = input("Digite um comando: ")
                if command == "exit":
                    break
                client_socket.send(command.encode())
                msg = client_socket.recv(1024)
                print(msg.decode("utf-8"))

            client_socket.close()
        except Exception as e:
            print(e)



if __name__ == "__main__":
    ip_address = sys.argv[1]
    port = int(sys.argv[2])
    client = client(ip_address, port)
    client.start()
