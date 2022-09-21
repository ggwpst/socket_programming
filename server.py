import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 80

server.bind((host, port))

server.listen(5)
print("Listening on %s : %d " % (host, port))

people = {}
lock = threading.Lock()


class Tserver(threading.Thread):
    def __init__(self, socket, adr):  # thread初始化條件
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = adr

    def run(self):  # 讓thread知道要做甚麼
        global people
        print('Client %s:%s connected.' % self.address)
        password = self.socket.recv(1024).decode()
        while(password != "123"):
            self.socket.send("Wrong password".encode())
            password = self.socket.recv(1024).decode()
        self.socket.send("ACK!".encode())
        while True:
            try:
                lock.acquire()
                data = self.socket.recv(1024).decode()
                if(data == "close"):
                    break
                cont = data.split(":")
                name = cont[0]
                command = cont[1]

                if (people.__contains__(name) == False):
                    people[name] = 0
                    self.socket.send("No".encode())
                else:
                    self.socket.send("Yes".encode())
                    if command == "cb":
                        self.socket.send(str(people[name]).encode())
                    elif command == "dp":
                        money = self.socket.recv(1024).decode()
                        people[name] += int(money)
                        self.socket.send(str(people[name]).encode())
                    elif command == "wd":
                        self.socket.send(str(people[name]).encode())
                        if(people[name] == 0):
                            self.socket.send(
                                "You don't have any money *A*".encode())
                        else:
                            money = self.socket.recv(1024).decode()
                            if(int(money) <= int(people[name])):
                                people[name] -= int(money)
                                self.socket.send(str(people[name]).encode())
                            else:
                                self.socket.send(
                                    "You don't have enough money to withdraw".encode())
                lock.release()
            except socket.timeout:
                break
        self.socket.close()
        print('Client %s:%s disconnected.' % self.address)


if __name__ == "__main__":
    while True:
        (client, adr) = server.accept()
        Tserver(client, adr).start()
