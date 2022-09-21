import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 80
s.connect((host, port))

password = input("Please input password : ")
s.send(password.encode())
password_ACK = s.recv(1024).decode()
while(password_ACK == "Wrong password"):
    print("server send : %s " % (password_ACK))
    password = input("Please input password : ")
    s.send(password.encode())
    password_ACK = s.recv(1024).decode()
print("server send : %s " % (password_ACK))
while True:
    data = input("Please input msg : ")
    if(data == "close"):
        break
    s.send(data.encode())
    cont = data.split(":")
    Have_account = s.recv(1024).decode()
    if Have_account == "No":
        print(cont[0] + " has 0 dollars !!")
    elif Have_account == "Yes":
        if cont[1] == "cb":
            balance = s.recv(1024).decode()
            print(balance)
        elif cont[1] == "dp":
            money = input("How much do you want to deposit : ")
            s.send(money.encode())
            balance = s.recv(1024).decode()
            print("balance : " + balance)
        elif cont[1] == "wd":
            price = s.recv(1024).decode()
            print("balance : " + price)
            if(int(price) == 0):
                msg = s.recv(1024).decode()
                print(msg)
            else:
                money = input("How much do you want to withdraw : ")
                s.send(money.encode())
                balance = s.recv(1024).decode()
                print("balance : " + balance)
s.close()
