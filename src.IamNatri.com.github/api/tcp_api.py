import socket
import sys
import time
from threading import Thread
import mmh3, time

from resp_parser import RespParser
from distributed_hash_table import DistributedHashTable


def connect(ip, port, routes, index):
    connected = False
    while connected is False:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((str(ip), int(port)))
            routes[index] = sock
            connected = True
        except Exception as e:
            print(e)
            time.sleep(2)


class DHTapi:
    def __init__(self, host, port, partitions):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.hash_table = DistributedHashTable()
        self.partitions = eval(partitions)
        self.routes = [None] * len(self.partitions)
        self.next = 0
        self.create_routes()

    def create_routes(self):
        for i in range(len(self.partitions)):
            ip, port = self.partitions[i].split(":")

            if (ip, port) != (self.host, self.port):
                my_thread = Thread(target=connect, args=(ip, port, self.routes, i))
                my_thread.daemon = True
                my_thread.start()

    def start(self):
        try:
            self.sock.bind((self.host, self.port))
            self.sock.listen(5)
            print(f"API TCP iniciada em {self.host}:{self.port}")

            while True:
                client_socket, client_address = self.sock.accept()
                print(f"Nova conexão de {client_address}")
                client_socket.send("Conectado".encode("utf-8"))

                # le os dados enviados pelo cliente
                data = client_socket.recv(1024)
                print(f"Recebido: {data}")

                # Parse de comando manual
                data = data.decode("utf-8").split(" ")
                print(f"Comando: {data}")

                # Parse de comando usando o RespParser
                # comand, _ = RespParser.parse_command(data)
                # print(f"Comando: {comand}")
                # Executa o comando na Hash Table
                response = self.execute_command(data)
                print(f"Resposta: {response}")

                # Envia a resposta para o cliente
                client_socket.send(response.encode("utf-8"))

                # close connection
                client_socket.close()
        except Exception as e:
            print(e)
        finally:
            self.sock.close()
            print("API TCP finalizada")

    def execute_command(self, command):
        # Execute command in Hash Table and return response
        try:
            print("comand 0")
            print(command[0])
            if command[0] == "PUT":
                key, value = command[1], command[2]
                key_hash = mmh3.hash(key, signed=False) % len(self.partitions)
                print(key_hash)
                print(self.routes)

                if self.routes[key_hash] is None:
                    self.hash_table.put(key, value)
                    return f"OK - {key} : {value}"
                else:
                    self.routes[key_hash].send(command.encode("utf-8"))
                    return self.routes[key_hash].recv(1024).decode("utf-8")

            elif command[0] == "GET":
                key = command[1]
                key_hash = mmh3.hash(key, signed=False) % len(self.partitions)

                if self.routes[key_hash] is None:
                    return self.hash_table.get(key)
                else:
                    self.routes[key_hash].send(command.encode("utf-8"))
                    return self.routes[key_hash].recv(1024).decode("utf-8")



            elif command[0] == "DELETE":
                key = command[1]
                self.hash_table.delete(key)
                return "OK"

            else:
                return "Invalid command"

        except Exception as e:
            return str(e)


if __name__ == "__main__":
    ip_address = str(sys.argv[1])
    port = int(sys.argv[2])
    partitions = sys.argv[3:]
    api = DHTapi(ip_address, port, partitions)
    api.start()
